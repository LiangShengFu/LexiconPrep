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
| 数据库 | PostgreSQL 18 |
| 字体 | Courier Prime |

## 快速启动

```bash
# 1. 安装依赖
npm install
cd backend && pip install -r requirements.txt

# 2. 启动 PostgreSQL（需先安装）
brew services start postgresql@18
/opt/homebrew/opt/postgresql@18/bin/createdb lexiconprep

# 3. 初始化数据库
cd backend
python init_db.py
python seed.py

# 4. 启动后端（终端1）
cd backend && uvicorn app.main:app --port 8000 --reload

# 5. 启动前端（终端2）
npx vite --port 3000
```

访问 `http://localhost:3000`

## 测试账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 普通用户 | test@lexiconprep.com | test123 |
| 管理员 | admin@lexiconprep.com | admin123 |

## 功能

- 首页：WebGL 矩阵背景 + 逐字解密标题动画 + 自定义十字光标
- 认证：JWT 登录/注册，密码修改，密码强度检测
- 个人主页：日历打卡、头像上传、个人信息编辑
- 资源库：搜索/筛选/下载学习资料，错题本（SM-2 间隔重复）
- 做题：学科选择 → 即时判分 + 解析 → 答题卡可视化
- 闪卡：创建/翻转/间隔重复复习
- 社区：发帖/点赞/排行榜（从学习数据实时计算）
- 番茄钟：悬浮小窗 + 独立全屏页面，自定义时长
- 管理后台：题目 CRUD、用户管理、系统概览

## 项目结构

```
├── index.html
├── src/
│   ├── main.ts                # 入口
│   ├── App.vue                # 根组件（布局切换）
│   ├── router/index.ts        # 路由 + 守卫
│   ├── stores/                # Pinia（auth, ui）
│   ├── api/client.ts          # Axios + JWT 自动续期
│   ├── styles/                # Tailwind + xAI 暗色主题
│   ├── components/            # NavBar, AppShell, 动画组件等
│   └── views/                 # 页面
│       ├── LandingPage.vue
│       ├── LoginPage.vue / RegisterPage.vue
│       ├── ProfilePage.vue
│       ├── LibraryPage.vue
│       ├── ExamPage.vue
│       ├── FlashcardsPage.vue
│       ├── CommunityPage.vue
│       ├── PomodoroPage.vue
│       └── admin/             # 管理后台
├── backend/
│   ├── app/main.py            # FastAPI 入口
│   ├── app/api/v1/            # REST API
│   ├── app/models/            # SQLAlchemy 模型
│   └── app/schemas/           # Pydantic 模型
└── design-systems/            # 71 品牌设计参考（不追踪）
```
