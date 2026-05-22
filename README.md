# LexiconPrep — 考研备考平台

专注极简的考研学情管理与备考平台。暗黑打字机风格，WebGL 终端矩阵背景，逐字解密动画。

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Vue 3 + TypeScript + Vite + Pinia + Vue Router |
| UI | Tailwind CSS + Element Plus（深度暗色定制） |
| 图表 | Chart.js |
| 动画 | GSAP + WebGL (ogl) |
| 后端 | Python FastAPI + SQLAlchemy 2.0 async |
| 数据库 | PostgreSQL 16（生产）/ SQLite（开发） |
| 缓存 | Redis 7 |
| 字体 | Courier Prime + Geist Mono + JetBrains Mono |

## 快速启动

```bash
# 1. 安装依赖
npm install
cd backend && pip install -r requirements.txt

# 2a. 开发模式（SQLite，零外部依赖）
cd backend
python init_db.py
python seed.py
uvicorn app.main:app --port 8000 --reload

# 2b. 生产模式（PostgreSQL + Redis）
docker compose up -d
cd backend
# 编辑 .env: DATABASE_URL=postgresql+asyncpg://lexicon:lexicon123@localhost:5432/lexiconprep
python init_db.py && python seed.py
uvicorn app.main:app --port 8000 --reload

# 3. 启动前端（新终端）
npx vite --port 3000
```

访问 `http://localhost:3000`

## 测试账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 普通用户 | test@lexiconprep.com | test123 |
| 管理员 | admin@lexiconprep.com | admin123 |

## 功能

- **首页**：WebGL 矩阵背景 + 逐字解密标题动画 + 自定义十字光标
- **认证**：JWT 登录/注册，密码修改（复杂度校验），Token 自动刷新
- **个人主页**：日历打卡（后端化）、头像上传（base64 ≤500KB）、个人信息编辑
- **资源库**：搜索/筛选学习资料，错题本（间隔重复 1→3→7→14→30→60 天）
- **做题**：学科选择 → 即时判分 + 解析 → 答题卡可视化 → 自动录入错题
- **闪卡**：创建/翻转/间隔重复复习
- **社区**：发帖/点赞（防重复）/删除/排行榜（7 日做题量）
- **番茄钟**：悬浮小窗 + 独立全屏页面，自定义时长
- **管理后台**：题目 CRUD（级联删除）、用户管理（角色自保护）、系统统计

## 项目结构

```
├── index.html
├── src/
│   ├── main.ts                # 入口
│   ├── App.vue                # 根组件（布局切换）
│   ├── router/index.ts        # 路由 + 守卫（15 条）
│   ├── stores/                # Pinia（auth, ui）
│   ├── api/client.ts          # Axios + JWT 自动续期 + 刷新队列
│   ├── styles/                # Tailwind + xAI 暗色主题
│   ├── components/            # NavBar, AppShell, FaultyTerminal, TargetCursor 等
│   └── views/                 # 页面（11 活跃 + 2 废弃重定向）
│       ├── LandingPage.vue
│       ├── LoginPage.vue / RegisterPage.vue
│       ├── ProfilePage.vue
│       ├── LibraryPage.vue
│       ├── ExamPage.vue
│       ├── FlashcardsPage.vue
│       ├── CommunityPage.vue
│       ├── PomodoroPage.vue
│       ├── ProgressPage.vue
│       └── admin/             # 管理后台
├── backend/
│   ├── app/main.py            # FastAPI 入口（CORS + 限流 + 日志）
│   ├── app/api/v1/            # REST API（9 个模块）
│   ├── app/models/            # SQLAlchemy 模型（8 个）
│   ├── app/schemas/           # Pydantic 模型
│   ├── app/core/              # 配置/数据库/安全/工具
│   ├── init_db.py             # 建表
│   ├── seed.py                # 种子数据
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml         # PostgreSQL 16 + Redis 7
├── Dockerfile.frontend
├── project.md                 # 项目总览
├── list.md                    # 功能清单
├── design.md                  # 技术设计文档
└── problems.md                # 问题清单
```

## API 文档

启动后端后访问：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- 健康检查: `http://localhost:8000/health`
