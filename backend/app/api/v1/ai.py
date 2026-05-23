import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Integer

from app.core.config import settings
from app.core.database import get_db
from app.core.llm import chat_completion, chat_completion_json, get_llm_client
from app.models.user import User
from app.models.question import Question
from app.models.mistake import Mistake
from app.models.study_log import StudyLog
from app.api.deps import get_current_user, get_admin_user
from app.schemas.ai import (
    GenerateQuestionsRequest,
    GenerateQuestionsResponse,
    GeneratedQuestion,
    DiagnosisResponse,
    StudyPlanRequest,
    StudyPlanResponse,
    DayPlan,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])


GENERATE_SYSTEM_PROMPT = """你是一个考研出题专家。根据用户指定的学科、章节和难度，生成高质量的考研选择题。

严格规则：
1. 题目必须符合考研大纲，内容准确无误
2. 干扰项必须有迷惑性，不能明显错误
3. 解析要引用具体知识点，帮助理解
4. 多选题答案至少包含2个正确选项
5. 选项数量固定为4个

输出格式：返回一个JSON对象，包含一个"questions"数组，每个元素格式如下：
{
  "type": "SINGLE 或 MULTIPLE",
  "content": "题干",
  "options": ["选项A", "选项B", "选项C", "选项D"],
  "answer": ["正确答案文本"],
  "analysis": "详细解析",
  "difficulty": 数字1-5,
  "subject": "学科",
  "chapter": "章节"
}

注意：answer 字段必须填入选项的完整文本，不是字母。"""


DIAGNOSIS_SYSTEM_PROMPT = """你是一位资深考研辅导老师，擅长根据学生的学习数据分析薄弱环节并给出针对性建议。

你的诊断报告需要包含以下部分，使用 Markdown 格式：
1. **整体评估**：用2-3句话概括当前学习状态
2. **薄弱章节 Top3**：列出错误最多的章节，分析原因
3. **知识盲区**：分析答对但耗时长的题目暗示的潜在问题
4. **提分建议**：给出未来7天的具体学习建议
5. **预估提升空间**：如果修复薄弱点，正确率能提升多少

语气：专业但亲切，像一位关心学生的老师。"""


@router.post("/generate-questions", response_model=GenerateQuestionsResponse)
async def generate_questions(
    data: GenerateQuestionsRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    if not settings.DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY 未配置")

    type_label = "多选" if data.type == "MULTIPLE" else "单选"
    chapter_info = f"\n章节：{data.chapter}" if data.chapter else ""
    difficulty_desc = {1: "基础", 2: "中等", 3: "较难", 4: "困难", 5: "极难"}

    user_prompt = f"""请生成 {data.count} 道考研{data.subject}{type_label}题。

要求：
- 学科：{data.subject}{chapter_info}
- 题型：{type_label}题
- 难度：{data.difficulty}（{difficulty_desc.get(data.difficulty, '中等')}）
- 数量：{data.count} 道

请确保题目之间不重复，且覆盖不同的知识点。"""

    try:
        result = await chat_completion_json(
            system_prompt=GENERATE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.7,
        )
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise HTTPException(status_code=502, detail=f"AI 服务调用失败: {str(e)}")

    questions_raw = result.get("questions", []) if isinstance(result, dict) else result
    if not isinstance(questions_raw, list):
        questions_raw = [questions_raw]

    saved: list[GeneratedQuestion] = []
    for q_data in questions_raw:
        try:
            options = q_data.get("options", [])
            answer = q_data.get("answer", [])
            if not options or not answer:
                continue

            question = Question(
                type=q_data.get("type", data.type),
                content=q_data.get("content", ""),
                options=options,
                answer=answer,
                analysis=q_data.get("analysis"),
                difficulty=q_data.get("difficulty", data.difficulty),
                subject=q_data.get("subject", data.subject),
                chapter=q_data.get("chapter", data.chapter),
            )
            db.add(question)
            saved.append(GeneratedQuestion(
                type=question.type,
                content=question.content,
                options=question.options,
                answer=question.answer,
                analysis=question.analysis,
                difficulty=question.difficulty,
                subject=question.subject,
                chapter=question.chapter,
            ))
        except Exception as e:
            logger.warning(f"Skipping invalid question: {e}")
            continue

    if saved:
        await db.commit()

    return GenerateQuestionsResponse(generated=len(saved), questions=saved)


@router.get("/diagnosis", response_model=DiagnosisResponse)
async def get_diagnosis(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not settings.DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY 未配置")

    total_result = await db.execute(
        select(func.count(StudyLog.id)).where(StudyLog.user_id == current_user.id)
    )
    total = total_result.scalar() or 0

    if total == 0:
        return DiagnosisResponse(diagnosis="## 暂无学习数据\n\n你还没有开始做题，完成一些题目后再来获取 AI 诊断报告吧！")

    correct_result = await db.execute(
        select(func.count(StudyLog.id)).where(
            StudyLog.user_id == current_user.id, StudyLog.is_correct == True
        )
    )
    correct = correct_result.scalar() or 0

    total_seconds_result = await db.execute(
        select(func.coalesce(func.sum(StudyLog.time_spent), 0)).where(
            StudyLog.user_id == current_user.id
        )
    )
    total_seconds = total_seconds.scalar() or 0

    wrong_by_chapter_result = await db.execute(
        select(Question.chapter, func.count(Mistake.id))
        .join(Question, Mistake.question_id == Question.id)
        .where(Mistake.user_id == current_user.id, Mistake.mastered == False)
        .group_by(Question.chapter)
        .order_by(func.count(Mistake.id).desc())
        .limit(5)
    )
    wrong_by_chapter = {row[0] or "未分类": row[1] for row in wrong_by_chapter_result.all()}

    wrong_by_subject_result = await db.execute(
        select(Question.subject, func.count(Mistake.id))
        .join(Question, Mistake.question_id == Question.id)
        .where(Mistake.user_id == current_user.id, Mistake.mastered == False)
        .group_by(Question.subject)
    )
    wrong_by_subject = {row[0]: row[1] for row in wrong_by_subject_result.all()}

    accuracy_by_subject_result = await db.execute(
        select(
            Question.subject,
            func.count(StudyLog.id).label("total"),
            func.sum(func.cast(StudyLog.is_correct, Integer)).label("correct"),
        )
        .join(Question, StudyLog.question_id == Question.id)
        .where(StudyLog.user_id == current_user.id)
        .group_by(Question.subject)
    )
    accuracy_by_subject = {}
    for row in accuracy_by_subject_result.all():
        t = row[1] or 0
        c = row[2] or 0
        accuracy_by_subject[row[0]] = {"total": t, "correct": c, "accuracy": round(c / t * 100, 1) if t > 0 else 0}

    slow_questions_result = await db.execute(
        select(Question.content, StudyLog.time_spent, Question.subject)
        .join(Question, StudyLog.question_id == Question.id)
        .where(
            StudyLog.user_id == current_user.id,
            StudyLog.is_correct == True,
            StudyLog.time_spent > 60,
        )
        .order_by(StudyLog.time_spent.desc())
        .limit(5)
    )
    slow_questions = [
        {"content": row[0][:50], "time_spent": row[1], "subject": row[2]}
        for row in slow_questions_result.all()
    ]

    data_summary = {
        "total_questions_answered": total,
        "correct_count": correct,
        "average_accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "total_study_minutes": total_seconds // 60,
        "streak_days": current_user.streak_days,
        "wrong_by_chapter": wrong_by_chapter,
        "wrong_by_subject": wrong_by_subject,
        "accuracy_by_subject": accuracy_by_subject,
        "slow_but_correct_questions": slow_questions,
    }

    user_prompt = f"""基于以下学习数据，生成个性化诊断报告：

{json.dumps(data_summary, ensure_ascii=False, indent=2)}

请用中文输出 Markdown 格式的诊断报告。"""

    try:
        diagnosis = await chat_completion(
            system_prompt=DIAGNOSIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=2048,
        )
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise HTTPException(status_code=502, detail=f"AI 服务调用失败: {str(e)}")

    return DiagnosisResponse(diagnosis=diagnosis)


STUDY_PLAN_SYSTEM_PROMPT = """你是一位考研学习规划专家。根据学生的学习数据和目标，制定科学、可执行的学习计划。

严格规则：
1. 计划必须基于学生的实际薄弱点，不能泛泛而谈
2. 每天的任务必须具体到章节和知识点
3. 遵循艾宾浩斯遗忘曲线安排复习
4. 合理分配新学知识和复习的时间比例（建议3:7到5:5）
5. 考虑学习疲劳，每天安排适当休息

输出格式：返回一个JSON对象，包含以下字段：
{
  "plan": [
    {
      "day": 1,
      "focus": "当天学习重点（一句话概括）",
      "tasks": ["具体任务1", "具体任务2", ...],
      "duration_minutes": 建议学习分钟数,
      "review_topics": ["需要复习的知识点1", ...]
    }
  ],
  "summary": "整体规划概述（2-3句话）",
  "estimated_accuracy_gain": "预估正确率提升幅度，如 5%-10%"
}"""


@router.post("/study-plan", response_model=StudyPlanResponse)
async def generate_study_plan(
    data: StudyPlanRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not settings.DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY 未配置")

    total_result = await db.execute(
        select(func.count(StudyLog.id)).where(StudyLog.user_id == current_user.id)
    )
    total = total_result.scalar() or 0

    if total == 0:
        default_plan = [
            DayPlan(
                day=i,
                focus=f"第{i}天：基础入门",
                tasks=[f"完成 {data.daily_minutes // 3} 分钟基础题目练习", "阅读核心知识点", "整理笔记"],
                duration_minutes=data.daily_minutes,
                review_topics=["回顾前一天内容"] if i > 1 else [],
            )
            for i in range(1, data.days + 1)
        ]
        return StudyPlanResponse(
            plan=default_plan,
            summary="你还没有学习记录，已为你生成入门级学习计划。完成一些题目后，AI 将基于你的数据生成更精准的计划。",
            estimated_accuracy_gain="N/A（暂无基线数据）",
        )

    correct_result = await db.execute(
        select(func.count(StudyLog.id)).where(
            StudyLog.user_id == current_user.id, StudyLog.is_correct == True
        )
    )
    correct = correct_result.scalar() or 0

    total_seconds_result = await db.execute(
        select(func.coalesce(func.sum(StudyLog.time_spent), 0)).where(
            StudyLog.user_id == current_user.id
        )
    )
    total_seconds = total_seconds_result.scalar() or 0

    wrong_by_chapter_result = await db.execute(
        select(Question.chapter, func.count(Mistake.id))
        .join(Question, Mistake.question_id == Question.id)
        .where(Mistake.user_id == current_user.id, Mistake.mastered == False)
        .group_by(Question.chapter)
        .order_by(func.count(Mistake.id).desc())
        .limit(8)
    )
    weak_chapters = {row[0] or "未分类": row[1] for row in wrong_by_chapter_result.all()}

    wrong_by_subject_result = await db.execute(
        select(Question.subject, func.count(Mistake.id))
        .join(Question, Mistake.question_id == Question.id)
        .where(Mistake.user_id == current_user.id, Mistake.mastered == False)
        .group_by(Question.subject)
        .order_by(func.count(Mistake.id).desc())
    )
    weak_subjects = {row[0]: row[1] for row in wrong_by_subject_result.all()}

    accuracy_by_subject_result = await db.execute(
        select(
            Question.subject,
            func.count(StudyLog.id).label("total"),
            func.sum(func.cast(StudyLog.is_correct, Integer)).label("correct"),
        )
        .join(Question, StudyLog.question_id == Question.id)
        .where(StudyLog.user_id == current_user.id)
        .group_by(Question.subject)
    )
    accuracy_by_subject = {}
    for row in accuracy_by_subject_result.all():
        t = row[1] or 0
        c = row[2] or 0
        accuracy_by_subject[row[0]] = {"total": t, "correct": c, "accuracy": round(c / t * 100, 1) if t > 0 else 0}

    mastered_result = await db.execute(
        select(func.count(Mistake.id)).where(
            Mistake.user_id == current_user.id, Mistake.mastered == True
        )
    )
    mastered_count = mastered_result.scalar() or 0

    unmastered_result = await db.execute(
        select(func.count(Mistake.id)).where(
            Mistake.user_id == current_user.id, Mistake.mastered == False
        )
    )
    unmastered_count = unmastered_result.scalar() or 0

    recent_7d_result = await db.execute(
        select(func.count(StudyLog.id)).where(
            StudyLog.user_id == current_user.id,
            StudyLog.timestamp >= func.now() - func.cast("7 days", type_=None),
        )
    )

    data_summary = {
        "total_questions_answered": total,
        "correct_count": correct,
        "average_accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "total_study_minutes": total_seconds // 60,
        "streak_days": current_user.streak_days,
        "weak_chapters": weak_chapters,
        "weak_subjects": weak_subjects,
        "accuracy_by_subject": accuracy_by_subject,
        "mastered_mistakes": mastered_count,
        "unmastered_mistakes": unmastered_count,
    }

    target_info = ""
    if data.target_subjects:
        target_info = f"\n重点攻克学科：{', '.join(data.target_subjects)}"

    user_prompt = f"""基于以下学习数据，制定一份 {data.days} 天的考研学习计划：

{json.dumps(data_summary, ensure_ascii=False, indent=2)}

要求：
- 计划天数：{data.days} 天
- 每日可用学习时间：{data.daily_minutes} 分钟{target_info}
- 优先安排薄弱章节的强化训练
- 每天必须包含错题复习环节
- 任务描述要具体到章节和知识点

请生成详细的学习计划。"""

    try:
        result = await chat_completion_json(
            system_prompt=STUDY_PLAN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=4096,
        )
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise HTTPException(status_code=502, detail=f"AI 服务调用失败: {str(e)}")

    try:
        plan_data = result.get("plan", []) if isinstance(result, dict) else result
        if not isinstance(plan_data, list):
            plan_data = [plan_data]

        day_plans = []
        for i, item in enumerate(plan_data[:data.days]):
            day_plans.append(DayPlan(
                day=item.get("day", i + 1),
                focus=item.get("focus", ""),
                tasks=item.get("tasks", []),
                duration_minutes=item.get("duration_minutes", data.daily_minutes),
                review_topics=item.get("review_topics", []),
            ))

        summary = result.get("summary", "") if isinstance(result, dict) else ""
        gain = result.get("estimated_accuracy_gain", "") if isinstance(result, dict) else ""

        return StudyPlanResponse(plan=day_plans, summary=summary, estimated_accuracy_gain=gain)
    except Exception as e:
        logger.error(f"Failed to parse study plan: {e}")
        raise HTTPException(status_code=502, detail="AI 返回的学习计划格式异常，请重试")
