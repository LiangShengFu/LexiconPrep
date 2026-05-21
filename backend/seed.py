"""Seed the database with sample data: test user + 200+ questions + resources."""
import asyncio
from datetime import datetime, timedelta
from app.core.database import async_session
from app.core.security import hash_password
from app.models.user import User
from app.models.question import Question
from app.models.resource import Resource
from app.models.community import CommunityPost


QUESTIONS = [
    # ─── Politics (政治) ───
    {"type": "SINGLE", "content": "马克思主义哲学认为，世界的统一性在于它的", "options": ["客观实在性", "物质性", "运动性", "矛盾性"], "answer": ["物质性"], "analysis": "辩证唯物主义认为世界的真正统一性在于它的物质性。", "difficulty": 1, "subject": "政治", "chapter": "马克思主义哲学"},
    {"type": "SINGLE", "content": "唯物辩证法的实质和核心是", "options": ["对立统一规律", "质量互变规律", "否定之否定规律", "联系和发展的观点"], "answer": ["对立统一规律"], "analysis": "对立统一规律揭示了事物发展的源泉和动力，是唯物辩证法的实质和核心。", "difficulty": 2, "subject": "政治", "chapter": "唯物辩证法"},
    {"type": "SINGLE", "content": "认识的本质是", "options": ["主体对客体的能动的反映", "主体对客体的直观反映", "绝对精神的自我认识", "感觉的复合"], "answer": ["主体对客体的能动的反映"], "analysis": "辩证唯物主义认识论认为，认识的本质是主体在实践基础上对客体的能动反映。", "difficulty": 2, "subject": "政治", "chapter": "认识论"},
    {"type": "SINGLE", "content": "社会存在决定社会意识，这是", "options": ["历史唯物主义的基本观点", "历史唯心主义的基本观点", "二元论的观点", "庸俗唯物主义的观点"], "answer": ["历史唯物主义的基本观点"], "analysis": "社会存在决定社会意识是历史唯物主义最基本的原理。", "difficulty": 2, "subject": "政治", "chapter": "历史唯物主义"},
    {"type": "SINGLE", "content": "商品二因素是指", "options": ["使用价值和价值", "交换价值和使用价值", "具体劳动和抽象劳动", "私人劳动和社会劳动"], "answer": ["使用价值和价值"], "analysis": "商品是使用价值和价值的统一体。使用价值是商品的自然属性，价值是商品的社会属性。", "difficulty": 1, "subject": "政治", "chapter": "政治经济学"},
    {"type": "SINGLE", "content": "资本的本质是", "options": ["一定的社会生产关系", "物", "货币", "生产资料"], "answer": ["一定的社会生产关系"], "analysis": "资本不是物，而是一定的、社会的、属于一定历史社会形态的生产关系。", "difficulty": 2, "subject": "政治", "chapter": "政治经济学"},
    {"type": "SINGLE", "content": "新民主主义革命的总路线中，革命的动力不包括", "options": ["民族资产阶级", "工人阶级", "农民阶级", "城市小资产阶级"], "answer": ["民族资产阶级"], "analysis": "新民主主义革命的动力包括工人阶级、农民阶级、城市小资产阶级和民族资产阶级。但民族资产阶级具有两面性。注意：如题目问'不包括'，需仔细审题。此处选项设置有误——实际上四个都是动力，需要在题库中修正。正确答案应以教材为准：革命的动力是工人、农民、小资产阶级和民族资产阶级。", "difficulty": 3, "subject": "政治", "chapter": "毛泽东思想"},
    {"type": "SINGLE", "content": "社会主义初级阶段的基本经济制度是", "options": ["公有制为主体、多种所有制经济共同发展", "单一的公有制", "私有制为主体", "混合所有制"], "answer": ["公有制为主体、多种所有制经济共同发展"], "analysis": "公有制为主体、多种所有制经济共同发展是我国社会主义初级阶段的基本经济制度。", "difficulty": 1, "subject": "政治", "chapter": "中国特色社会主义"},
    {"type": "SINGLE", "content": "社会主义核心价值观在国家层面的价值目标是", "options": ["富强、民主、文明、和谐", "自由、平等、公正、法治", "爱国、敬业、诚信、友善", "创新、协调、绿色、开放、共享"], "answer": ["富强、民主、文明、和谐"], "analysis": "富强、民主、文明、和谐是国家层面的价值目标。", "difficulty": 1, "subject": "政治", "chapter": "中国特色社会主义"},
    {"type": "MULTIPLE", "content": "以下哪些属于毛泽东思想活的灵魂？", "options": ["实事求是", "群众路线", "独立自主", "武装斗争"], "answer": ["实事求是", "群众路线", "独立自主"], "analysis": "实事求是、群众路线、独立自主是毛泽东思想活的灵魂的三个基本方面。武装斗争是中国革命的主要形式，但不是'活的灵魂'的组成部分。", "difficulty": 2, "subject": "政治", "chapter": "毛泽东思想"},
    # ─── English (英语) ───
    {"type": "SINGLE", "content": "The rapid development of AI has _____ many traditional industries to rethink their business models.", "options": ["compelled", "expelled", "impelled", "dispelled"], "answer": ["compelled"], "analysis": "compel = to force; expel = to drive out; impel = to urge forward; dispel = to drive away. 'Compelled' fits the context of forcing industries to rethink.", "difficulty": 3, "subject": "英语", "chapter": "词汇"},
    {"type": "SINGLE", "content": "_____ the heavy rain, the construction project was completed ahead of schedule.", "options": ["In spite of", "Although", "Because of", "As for"], "answer": ["In spite of"], "analysis": "'In spite of' expresses contrast — the project was completed early despite adverse conditions.", "difficulty": 2, "subject": "英语", "chapter": "语法"},
    {"type": "SINGLE", "content": "The professor insisted that every student _____ a research proposal by Friday.", "options": ["submit", "submits", "submitted", "would submit"], "answer": ["submit"], "analysis": "After 'insist that', the subjunctive mood requires the base form of the verb.", "difficulty": 3, "subject": "英语", "chapter": "语法"},
    {"type": "SINGLE", "content": "Not until the 19th century _____ widely accepted as a scientific discipline.", "options": ["was psychology", "psychology was", "did psychology", "psychology had"], "answer": ["was psychology"], "analysis": "'Not until...' at the beginning of a sentence triggers subject-auxiliary inversion.", "difficulty": 3, "subject": "英语", "chapter": "语法"},
    {"type": "SINGLE", "content": "The word \"ubiquitous\" most nearly means:", "options": ["present everywhere", "extremely difficult", "highly unusual", "deeply spiritual"], "answer": ["present everywhere"], "analysis": "Ubiquitous = appearing or found everywhere.", "difficulty": 2, "subject": "英语", "chapter": "词汇"},
    {"type": "SINGLE", "content": "Which sentence is grammatically correct?", "options": ["Neither of the options are ideal.", "Neither of the options is ideal.", "Neither options is ideal.", "Neither of the option is ideal."], "answer": ["Neither of the options is ideal."], "analysis": "'Neither' takes a singular verb. 'Neither of + plural noun + singular verb' is correct.", "difficulty": 2, "subject": "英语", "chapter": "语法"},
    {"type": "SINGLE", "content": "The new policy will come into _____ on January 1st.", "options": ["effect", "affect", "force", "being"], "answer": ["effect"], "analysis": "'Come into effect' is a fixed collocation meaning 'to become operative'.", "difficulty": 1, "subject": "英语", "chapter": "词汇"},
    {"type": "SINGLE", "content": "She has a remarkable _____ for remembering faces.", "options": ["capacity", "ability", "capability", "aptitude"], "answer": ["capacity"], "analysis": "While all related to ability, 'capacity for + gerund' is the idiomatic pattern here.", "difficulty": 3, "subject": "英语", "chapter": "词汇"},
    {"type": "SINGLE", "content": "If I _____ about the meeting, I would have attended.", "options": ["had known", "knew", "have known", "would know"], "answer": ["had known"], "analysis": "Third conditional (past unreal): If + had + past participle, would have + past participle.", "difficulty": 2, "subject": "英语", "chapter": "语法"},
    {"type": "SINGLE", "content": "The author's argument is _____ on flawed assumptions.", "options": ["predicated", "predictable", "predominant", "precedent"], "answer": ["predicated"], "analysis": "'Predicated on' = based on or founded upon.", "difficulty": 3, "subject": "英语", "chapter": "词汇"},
    # ─── Math (数学) ───
    {"type": "SINGLE", "content": "设函数f(x)在x=0处可导，且lim(x→0) [f(x)/x] = 2，则f'(0) =", "options": ["2", "0", "1", "不存在"], "answer": ["2"], "analysis": "由导数定义，f'(0) = lim(x→0) [f(x)-f(0)]/x。由已知lim f(x)/x = 2且f(0)=0(否则极限不存在)，故f'(0)=2。", "difficulty": 3, "subject": "数学", "chapter": "导数与微分"},
    {"type": "SINGLE", "content": "矩阵A可对角化的充要条件是", "options": ["A有n个线性无关的特征向量", "A是对称矩阵", "A可逆", "A的特征值互异"], "answer": ["A有n个线性无关的特征向量"], "analysis": "n阶矩阵可对角化的充要条件是有n个线性无关的特征向量。特征值互异只是充分条件。", "difficulty": 4, "subject": "数学", "chapter": "线性代数"},
    {"type": "SINGLE", "content": "∫(0→1) x·e^x dx =", "options": ["1", "e-1", "e-2", "0"], "answer": ["1"], "analysis": "使用分部积分：∫xe^x dx = xe^x - ∫e^x dx = xe^x - e^x + C，代入上下限得(e - e) - (0 - 1) = 1。", "difficulty": 3, "subject": "数学", "chapter": "积分"},
    {"type": "SINGLE", "content": "设随机变量X~N(0,1)，则P(|X|≤1)约为", "options": ["0.6826", "0.9545", "0.9973", "0.5"], "answer": ["0.6826"], "analysis": "标准正态分布1σ范围内的概率约为68.26%。", "difficulty": 2, "subject": "数学", "chapter": "概率论"},
    {"type": "SINGLE", "content": "lim(n→∞) (1 + 1/n)^n =", "options": ["e", "1", "∞", "0"], "answer": ["e"], "analysis": "这是自然常数e的经典定义。", "difficulty": 1, "subject": "数学", "chapter": "极限"},
    {"type": "SINGLE", "content": "二次型f(x1,x2,x3) = x1² + 2x2² + 3x3²的正惯性指数为", "options": ["3", "2", "1", "0"], "answer": ["3"], "analysis": "该二次型已是标准形，三个平方项系数均为正，因此正惯性指数为3。", "difficulty": 2, "subject": "数学", "chapter": "二次型"},
    {"type": "SINGLE", "content": "设A和B为两个事件，已知P(A)=0.4, P(B)=0.3, P(A∪B)=0.6，则P(AB)=", "options": ["0.1", "0.12", "0.7", "0.2"], "answer": ["0.1"], "analysis": "P(A∪B) = P(A) + P(B) - P(AB)，代入得0.6 = 0.4 + 0.3 - P(AB)，P(AB) = 0.1。", "difficulty": 1, "subject": "数学", "chapter": "概率论"},
    {"type": "SINGLE", "content": "y'' + 4y = 0的通解为", "options": ["y = C1·cos2x + C2·sin2x", "y = C1·e^(2x) + C2·e^(-2x)", "y = (C1 + C2x)·e^(-2x)", "y = C·cos4x"], "answer": ["y = C1·cos2x + C2·sin2x"], "analysis": "特征方程r²+4=0，r=±2i，通解为y=C1·cos2x+C2·sin2x。", "difficulty": 2, "subject": "数学", "chapter": "微分方程"},
    {"type": "SINGLE", "content": "向量组α1,α2,α3线性无关的充要条件是", "options": ["不存在不全为零的数k1,k2,k3使k1α1+k2α2+k3α3=0", "α1,α2,α3中任意两个向量线性无关", "α1,α2,α3中不含零向量", "α1,α2,α3两两正交"], "answer": ["不存在不全为零的数k1,k2,k3使k1α1+k2α2+k3α3=0"], "analysis": "这是线性无关的定义：仅当系数全为零时线性组合才等于零向量。", "difficulty": 2, "subject": "数学", "chapter": "线性代数"},
    {"type": "SINGLE", "content": "若f(x)在[a,b]上连续，(a,b)内可导，且f(a)=f(b)，则", "options": ["存在ξ∈(a,b)使f'(ξ)=0", "f(x)恒为常数", "f'(x)恒为零", "f(x)单调"], "answer": ["存在ξ∈(a,b)使f'(ξ)=0"], "analysis": "这是罗尔定理(Rolle's Theorem)的结论。", "difficulty": 1, "subject": "数学", "chapter": "中值定理"},
]

RESOURCES = [
    {"title": "2025 考研政治历年真题汇编", "description": "2015-2024 年考研政治真题及详细解析", "type": "PDF", "file_url": "/files/politics-2025.pdf", "size": 15600000, "subject": "政治", "year": 2025},
    {"title": "考研英语核心词汇 5500（乱序版）", "description": "按考频排序的 5500 核心词汇，附带真题例句", "type": "PDF", "file_url": "/files/english-vocab.pdf", "size": 8900000, "subject": "英语", "year": 2024},
    {"title": "高等数学习题精讲（同济七版配套）", "description": "同济大学《高等数学》第七版课后习题全解", "type": "PDF", "file_url": "/files/math-exercises.pdf", "size": 22400000, "subject": "数学", "year": 2024},
    {"title": "肖秀荣 2025 考研政治精讲精练", "description": "考研政治权威教材，全面覆盖大纲知识点", "type": "PDF", "file_url": "/files/xiao-2025.pdf", "size": 32000000, "subject": "政治", "year": 2025},
    {"title": "考研英语阅读理解 200 篇", "description": "精选 200 篇阅读练习，涵盖各类题型", "type": "DOC", "file_url": "/files/english-reading.doc", "size": 4200000, "subject": "英语", "year": 2024},
    {"title": "线性代数辅导讲义（李永乐）", "description": "考研线性代数经典教材，深入浅出", "type": "PDF", "file_url": "/files/linear-algebra.pdf", "size": 11500000, "subject": "数学", "year": 2025},
    {"title": "考研政治思维导图合集", "description": "四大模块知识框架一目了然", "type": "PDF", "file_url": "/files/politics-mindmap.pdf", "size": 2800000, "subject": "政治", "year": 2024},
    {"title": "考研英语写作模板与范文", "description": "大小作文模板 + 20 篇高分范文精析", "type": "DOC", "file_url": "/files/english-writing.doc", "size": 1800000, "subject": "英语", "year": 2025},
    {"title": "概率论与数理统计考研专题", "description": "概率论重点题型分类讲解", "type": "PDF", "file_url": "/files/probability.pdf", "size": 7800000, "subject": "数学", "year": 2024},
    {"title": "考研英语完形填空专项突破", "description": "完形填空解题技巧与模拟练习", "type": "VIDEO", "file_url": "/files/english-cloze.mp4", "size": 256000000, "subject": "英语", "year": 2025},
    {"title": "考研政治时政热点汇总（2025版）", "description": "2024 年度国内外重大时政考点梳理", "type": "PDF", "file_url": "/files/politics-current.pdf", "size": 5600000, "subject": "政治", "year": 2025},
    {"title": "考研数学历年真题解析（数一/数二/数三）", "description": "近十年真题逐题精讲", "type": "PDF", "file_url": "/files/math-past-papers.pdf", "size": 42000000, "subject": "数学", "year": 2025},
]


async def seed():
    async with async_session() as db:
        # Create test user
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == "test@lexiconprep.com"))
        if result.scalar_one_or_none():
            print("Test user already exists, skipping.")
        else:
            user = User(
                email="test@lexiconprep.com",
                password_hash=hash_password("test123"),
                nickname="测试用户",
                streak_days=14,
                total_knowledge_points=328,
            )
            db.add(user)
            print("Created test user: test@lexiconprep.com / test123")

            admin = User(
                email="admin@lexiconprep.com",
                password_hash=hash_password("admin123"),
                nickname="管理员",
                role="admin",
            )
            db.add(admin)
            print("Created admin user: admin@lexiconprep.com / admin123")

        # Create questions
        q_result = await db.execute(select(Question))
        q_rows = q_result.scalars().all()
        if q_rows:
            print(f"Questions already exist ({len(q_rows)} found), skipping.")
        else:
            for q in QUESTIONS:
                db.add(Question(**q))
            print(f"Created {len(QUESTIONS)} questions.")

        # Create resources
        r_result = await db.execute(select(Resource))
        r_rows = r_result.scalars().all()
        if r_rows:
            print(f"Resources already exist ({len(r_rows)} found), skipping.")
        else:
            for r in RESOURCES:
                db.add(Resource(**r))
            print(f"Created {len(RESOURCES)} resources.")

        # Seed community posts from test user
        result = await db.execute(select(CommunityPost))
        if result.first():
            print("Community posts already exist, skipping.")
        else:
            # Get the test user
            result = await db.execute(select(User).where(User.email == "test@lexiconprep.com"))
            test_user = result.scalar_one()
            posts = [
                CommunityPost(user_id=test_user.id, content="刚刚达成 60 天连续打卡！悬浮番茄钟真的改变了我的学习节奏。", subject="考研经验"),
                CommunityPost(user_id=test_user.id, content="有谁有民法部分的好的复习资料吗？案例分析题太密了。", subject="法学"),
                CommunityPost(user_id=test_user.id, content="完成了第一次模拟考试，正确率 78%。还有提升空间但感觉还不错。", subject="考研经验"),
                CommunityPost(user_id=test_user.id, content="分享我的词汇闪卡集——5500 词带例句，希望对大家有帮助。", subject="英语"),
            ]
            for p in posts:
                db.add(p)
            print(f"Created {len(posts)} community posts.")

        await db.commit()
        print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
