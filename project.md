# LexiconPrep — 项目总览

> 考研备考平台 | 暗黑终端风格 | WebGL 矩阵背景 | 逐字解密动画

---

## 1. 项目简介

**LexiconPrep** 是一款面向考研学子的学情管理与备考平台。采用暗黑打字机/终端美学设计，WebGL 矩阵雨背景 + 自定义十字光标 + 逐字解密标题动画，营造沉浸式学习氛围。

核心功能：智能题库、错题本（间隔重复）、闪卡复习、番茄钟专注、社区互动、管理后台。

---

## 2. 技术栈

### 前端

| 分类 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 框架 | Vue.js | 3.5+ | Composition API + TypeScript |
| 构建 | Vite | 6.x | 开发服务器 + 生产构建 |
| UI 框架 | Element Plus | 2.9+ | 深度暗色主题定制 |
| 状态管理 | Pinia | 2.3+ | authStore + uiStore |
| 路由 | Vue Router | 4.5+ | 15 条路由 + 守卫 |
| 图表 | Chart.js | 4.4+ | 折线/柱状/雷达/环形图 |
| 样式 | Tailwind CSS | 3.4+ | xAI 暗色设计 token |
| 动画 | GSAP | 3.15+ | 页面过渡与微交互 |
| WebGL | ogl | 1.0+ | 终端矩阵背景特效 |
| HTTP | Axios | 1.16+ | JWT 自动注入 + 401 拦截 + Token 刷新队列 |

### 后端

| 分类 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 语言 | Python | 3.12+ | 类型注解 + async/await |
| 框架 | FastAPI | 0.115+ | 自动 API 文档 + 高性能 |
| ORM | SQLAlchemy | 2.0+ | 异步 ORM + mapped_column |
| 数据库 | PostgreSQL | 16+ | 生产环境（开发可用 SQLite） |
| 缓存 | Redis | 7.x | 已配置但未深度集成 |
| 认证 | python-jose + passlib | - | JWT + bcrypt |
| 限流 | slowapi | - | 登录 5 次/分钟 + 全局 60 次/分钟 |
| 迁移 | Alembic | 1.14+ | 目录已创建，待初始化迁移脚本 |

---

## 3. 项目结构

```
├── index.html                  # 入口 HTML（SEO meta + 字体 CDN）
├── env.d.ts                    # TypeScript 环境类型声明
├── tsconfig.json               # TS 严格模式（strict + noUnused）
├── package.json                # 前端依赖
├── docker-compose.yml          # PostgreSQL + Redis 编排
├── Dockerfile.frontend         # 前端容器
├── src/
│   ├── main.ts                 # Vue 入口
│   ├── App.vue                 # 根组件（布局切换：营销页/管理后台/应用内页）
│   ├── router/index.ts         # 15 条路由 + 认证守卫 + 管理员守卫
│   ├── stores/
│   │   ├── auth.ts             # 认证状态（login/register/logout/initFromStorage）
│   │   └── ui.ts               # Toast 通知系统
│   ├── api/client.ts           # Axios 实例（JWT 注入 + Token 刷新队列 + 错误 Toast）
│   ├── styles/                 # Tailwind + xAI 暗色主题变量
│   ├── components/
│   │   ├── NavBar.vue          # 顶部导航栏（营销页）
│   │   ├── AppShell.vue        # 应用内页布局（侧边栏 + 主内容）
│   │   ├── AdminShell.vue      # 管理后台布局
│   │   ├── FaultyTerminal.vue  # WebGL 终端矩阵背景
│   │   ├── TargetCursor.vue    # 自定义十字光标
│   │   ├── DecryptedText.vue   # 逐字解密动画
│   │   ├── ToastContainer.vue  # 全局 Toast 通知
│   │   ├── ErrorBoundary.vue   # 错误边界
│   │   ├── SkeletonLoader.vue  # 骨架屏
│   │   └── PomodoroTimer.vue   # 番茄钟悬浮组件
│   └── views/
│       ├── LandingPage.vue     # 首页（Hero + Bento Grid）
│       ├── LoginPage.vue       # 登录
│       ├── RegisterPage.vue    # 注册
│       ├── ProfilePage.vue     # 个人主页（日历打卡 + 信息编辑）
│       ├── LibraryPage.vue     # 资源库 + 错题本
│       ├── ExamPage.vue        # 做题模式
│       ├── FlashcardsPage.vue  # 闪卡复习
│       ├── ProgressPage.vue    # 学习进度
│       ├── CommunityPage.vue   # 社区
│       ├── PomodoroPage.vue    # 番茄钟全屏
│       ├── DashboardPage.vue   # [已废弃] 重定向到 /profile
│       ├── SettingsPage.vue    # [已废弃] 重定向到 /profile
│       └── admin/
│           ├── AdminOverviewPage.vue   # 管理概览
│           ├── AdminQuestionsPage.vue  # 题目 CRUD
│           └── AdminUsersPage.vue      # 用户管理
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI 入口（CORS + 限流 + 日志中间件）
│   │   ├── core/
│   │   │   ├── config.py       # Settings（pydantic-settings + .env）
│   │   │   ├── database.py     # 异步引擎 + 连接池 + 会话管理
│   │   │   ├── security.py     # JWT + bcrypt
│   │   │   └── utils.py        # escape_search（防通配符注入）
│   │   ├── api/
│   │   │   ├── deps.py         # get_current_user + get_admin_user
│   │   │   └── v1/
│   │   │       ├── router.py   # API 路由汇总
│   │   │       ├── auth.py     # 注册/登录/刷新 Token
│   │   │       ├── users.py    # 用户信息/密码修改/打卡
│   │   │       ├── questions.py # 题目列表/答题/自动录入错题
│   │   │       ├── mistakes.py  # 错题列表/删除/复习
│   │   │       ├── flashcards.py # 闪卡 CRUD + 复习
│   │   │       ├── resources.py # 资源列表/详情
│   │   │       ├── stats.py    # 学习统计（实时 DB 查询）
│   │   │       ├── community.py # 发帖/点赞/删除/排行榜
│   │   │       └── admin.py    # 管理后台（题目 CRUD + 用户管理 + 统计）
│   │   ├── models/             # 8 个模型
│   │   │   ├── user.py         # User（含 role 字段）
│   │   │   ├── question.py     # Question（含 subject 索引）
│   │   │   ├── mistake.py      # Mistake（含 mastered 字段）
│   │   │   ├── flashcard.py    # Flashcard
│   │   │   ├── resource.py     # Resource
│   │   │   ├── study_log.py    # StudyLog
│   │   │   ├── community.py    # CommunityPost
│   │   │   └── post_like.py    # PostLike（联合唯一约束）
│   │   └── schemas/            # Pydantic 模型
│   │       ├── user.py         # 含 PasswordChange 复杂度校验
│   │       ├── question.py     # 含 QuestionCreate/Update
│   │       ├── community.py    # 含 max_length=2000
│   │       ├── mistake.py
│   │       ├── flashcard.py
│   │       └── resource.py
│   ├── init_db.py              # 建表脚本
│   ├── seed.py                 # 种子数据（30 题 + 12 资源 + 2 用户 + 4 帖子）
│   ├── Dockerfile              # 后端容器
│   ├── .env.example            # 环境变量模板
│   └── requirements.txt        # Python 依赖
├── project.md                  # 本文档
├── list.md                     # 功能清单
├── design.md                   # 技术设计文档
├── problems.md                 # 问题清单
└── README.md                   # 快速启动指南
```

---

## 4. 数据库模型

### 4.1 ER 关系

```
User 1──N StudyLog       User 1──N Mistake        User 1──N Flashcard
User 1──N CommunityPost  User 1──N PostLike

Question 1──N StudyLog   Question 1──N Mistake

CommunityPost 1──N PostLike
```

### 4.2 表结构

#### users

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 用户唯一标识 |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 邮箱 |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 加密 |
| nickname | VARCHAR(50) | NOT NULL | 昵称 |
| avatar | TEXT | NULL | base64 头像（≤500KB） |
| role | VARCHAR(20) | DEFAULT 'user' | 角色（user/admin） |
| streak_days | INT | DEFAULT 0 | 连续打卡天数 |
| total_knowledge_points | INT | DEFAULT 0 | 已掌握知识点（去重计数） |
| created_at | TIMESTAMP | DEFAULT now() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT now() | 更新时间 |

#### questions

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 题目唯一标识 |
| type | VARCHAR(20) | NOT NULL | SINGLE/MULTIPLE/JUDGE |
| content | TEXT | NOT NULL | 题目内容 |
| options | JSONB | NOT NULL | 选项（list[str]） |
| answer | JSONB | NOT NULL | 正确答案（list[str]） |
| analysis | TEXT | NULL | 答案解析 |
| difficulty | INT | DEFAULT 1 | 难度 1-5 |
| subject | VARCHAR(50) | NOT NULL, INDEX | 学科分类 |
| chapter | VARCHAR(100) | NULL | 章节 |
| created_at | TIMESTAMP | DEFAULT now() | 创建时间 |

#### study_logs

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 记录唯一标识 |
| user_id | UUID | FK → users, INDEX | 用户 ID |
| question_id | UUID | FK → questions | 题目 ID |
| user_answer | VARCHAR(500) | NOT NULL | 用户答案（逗号分隔排序） |
| is_correct | BOOLEAN | NOT NULL | 是否正确 |
| time_spent | INT | DEFAULT 0 | 答题耗时（秒） |
| timestamp | TIMESTAMP | DEFAULT now() | 答题时间 |

#### mistakes

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 记录唯一标识 |
| user_id | UUID | FK → users, INDEX | 用户 ID |
| question_id | UUID | FK → questions | 题目 ID |
| wrong_count | INT | DEFAULT 1 | 错误次数 |
| review_count | INT | DEFAULT 0 | 复习次数 |
| mastered | BOOLEAN | DEFAULT FALSE | 是否已掌握 |
| last_review_at | TIMESTAMP | NULL | 最后复习时间 |
| next_review_at | TIMESTAMP | NOT NULL | 下次复习时间 |
| created_at | TIMESTAMP | DEFAULT now() | 创建时间 |

#### flashcards

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 闪卡唯一标识 |
| user_id | UUID | FK → users | 用户 ID |
| front | TEXT | NOT NULL | 正面内容 |
| back | TEXT | NOT NULL | 背面内容 |
| subject | VARCHAR(50) | NULL | 学科分类 |
| difficulty | INT | DEFAULT 1 | 难度 1-5 |
| review_count | INT | DEFAULT 0 | 复习次数 |
| next_review_at | TIMESTAMP | NOT NULL | 下次复习时间 |
| created_at | TIMESTAMP | DEFAULT now() | 创建时间 |

#### resources

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 资源唯一标识 |
| title | VARCHAR(255) | NOT NULL | 资源标题 |
| description | TEXT | NULL | 资源描述 |
| type | VARCHAR(20) | NOT NULL | PDF/DOC/VIDEO |
| file_url | VARCHAR(500) | NOT NULL | 文件 URL |
| size | BIGINT | NOT NULL | 文件大小（字节） |
| subject | VARCHAR(50) | NOT NULL | 学科分类 |
| year | INT | NULL | 年份 |
| downloads | INT | DEFAULT 0 | 下载次数 |
| created_at | TIMESTAMP | DEFAULT now() | 创建时间 |

#### community_posts

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 帖子唯一标识 |
| user_id | UUID | FK → users, INDEX | 作者 ID |
| content | TEXT | NOT NULL | 帖子内容 |
| subject | VARCHAR(50) | NULL | 学科标签 |
| likes | INT | DEFAULT 0 | 点赞数 |
| created_at | TIMESTAMP | DEFAULT now() | 创建时间 |

#### post_likes

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 记录唯一标识 |
| user_id | UUID | FK → users | 用户 ID |
| post_id | UUID | FK → community_posts | 帖子 ID |

联合唯一约束：`uq_post_like(user_id, post_id)`

---

## 5. API 接口一览

基础路径：`/api/v1`

### 认证

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| POST | `/auth/register` | 注册（邮箱+昵称唯一性校验） | 无 |
| POST | `/auth/login` | 登录（限流 5 次/分钟） | 无 |
| POST | `/auth/refresh` | 刷新 Token（验证 type=refresh） | 无 |

### 用户

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/users/me` | 获取当前用户信息 | JWT |
| PUT | `/users/me` | 更新昵称/头像（≤500KB, base64） | JWT |
| PUT | `/users/me/password` | 修改密码（复杂度校验） | JWT |
| POST | `/users/me/checkin` | 打卡（后端化，更新 streak_days） | JWT |

### 题目

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/questions/subjects` | 获取学科列表 | 无 |
| GET | `/questions` | 题目列表（学科/难度筛选 + 分页） | JWT |
| GET | `/questions/{id}` | 单题详情 | JWT |
| POST | `/questions/{id}/answer` | 提交答案 → 判对错 + 写 study_log + 自动录入/标记错题 | JWT |

### 错题本

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/mistakes` | 错题列表（仅未掌握，按下次复习日排序） | JWT |
| DELETE | `/mistakes/{id}` | 删除错题 | JWT |
| POST | `/mistakes/{id}/review` | 复习错题（remembered→标记已掌握，否则 wrong_count+1） | JWT |

### 闪卡

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/flashcards` | 闪卡列表（学科筛选 + 分页） | JWT |
| POST | `/flashcards` | 创建闪卡 | JWT |
| PUT | `/flashcards/{id}` | 更新闪卡 | JWT |
| DELETE | `/flashcards/{id}` | 删除闪卡 | JWT |
| POST | `/flashcards/{id}/review` | 复习闪卡（间隔：1→3→7→14→30→60 天） | JWT |

### 资源

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/resources` | 资源列表（学科/类型/搜索 + 分页） | JWT |
| GET | `/resources/{id}` | 资源详情 | JWT |

### 统计

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/stats/overview` | KPI 概览（实时 DB 聚合） | JWT |
| GET | `/stats/progress` | 10 周趋势 + 科目分布 | JWT |
| GET | `/stats/trend` | 7 日每日做题量 | JWT |

### 社区

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/community/posts` | 帖子列表 | JWT |
| POST | `/community/posts` | 发帖（≤2000 字） | JWT |
| POST | `/community/posts/{id}/like` | 点赞（防重复） | JWT |
| DELETE | `/community/posts/{id}` | 删除帖子（仅作者） | JWT |
| GET | `/community/leaderboard` | 7 日排行榜 | JWT |

### 管理后台

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/admin/questions` | 题目列表（搜索 + 分页） | Admin |
| POST | `/admin/questions` | 创建题目 | Admin |
| PUT | `/admin/questions/{id}` | 更新题目 | Admin |
| DELETE | `/admin/questions/{id}` | 删除题目（级联删除 mistakes + study_logs） | Admin |
| GET | `/admin/users` | 用户列表 | Admin |
| PUT | `/admin/users/{id}/role` | 修改用户角色（自保护） | Admin |
| GET | `/admin/stats` | 系统统计 | Admin |

### 健康检查

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | `/health` | 服务健康检查 | 无 |

---

## 6. 核心业务逻辑

### 6.1 答题流程

```
用户选择答案 → POST /questions/{id}/answer
  → 比对答案（排序后字符串比较）
  → 写入 study_logs
  → 答对：检查是否首次答对 → 更新 total_knowledge_points（去重）
  → 答对：检查是否在错题本 → 标记 mastered=True
  → 答错：检查是否已有错题 → 有则 wrong_count+1, mastered=False → 无则新建
  → 返回判对错 + 解析
```

### 6.2 间隔重复

错题复习和闪卡复习采用固定间隔序列（非 SM-2 算法）：

| 复习次数 | 间隔天数 |
|---------|---------|
| 第 1 次 | 1 天 |
| 第 2 次 | 3 天 |
| 第 3 次 | 7 天 |
| 第 4 次 | 14 天 |
| 第 5 次 | 30 天 |
| 第 6 次+ | 60 天 |

忘记时重置为 1 天间隔。

### 6.3 打卡系统

- 后端化：`POST /users/me/checkin`
- 同一天重复打卡返回 `already_checked_in`
- 连续打卡：昨天有打卡 → streak_days + 1；否则重置为 1

### 6.4 认证流程

```
注册/登录 → 返回 access_token (15min) + refresh_token (7day)
前端存储到 localStorage → Axios 拦截器自动注入 Authorization
access_token 过期 → 自动调用 /auth/refresh → 请求队列等待刷新完成
刷新失败 → 清除认证信息 → 跳转登录页
```

---

## 7. 安全措施

| 措施 | 状态 | 说明 |
|------|------|------|
| JWT 认证 | ✅ 已实现 | access 15min + refresh 7day |
| bcrypt 密码加密 | ✅ 已实现 | passlib CryptContext |
| 登录限流 | ✅ 已实现 | slowapi 5 次/分钟 |
| 全局限流 | ✅ 已实现 | slowapi 60 次/分钟（可配置） |
| CORS 动态配置 | ✅ 已实现 | 从 ALLOWED_ORIGINS 环境变量读取 |
| 搜索注入防护 | ✅ 已实现 | escape_search 转义 % 和 _ |
| 点赞防刷 | ✅ 已实现 | PostLike 联合唯一约束 |
| 头像大小校验 | ✅ 已实现 | ≤500KB + MIME 类型检查 |
| 密码复杂度校验 | ✅ 已实现 | ≥8位 + 大写 + 小写 + 数字 |
| 帖子长度限制 | ✅ 已实现 | max_length=2000 |
| 昵称唯一性 | ✅ 已实现 | 注册时校验 |
| 管理员自保护 | ✅ 已实现 | 不允许修改自己角色 |
| 级联删除 | ✅ 已实现 | 删除题目时清理关联 mistakes + study_logs |
| HTTPS | ⚠️ 待配置 | 生产环境必须 |
| HttpOnly Cookie | ⚠️ 待实现 | refresh_token 当前存 localStorage |

---

## 8. 部署架构

### 开发环境

```bash
# 前端
npm install && npx vite --port 3000

# 后端（SQLite 零依赖模式）
cd backend && pip install -r requirements.txt
python init_db.py && python seed.py
uvicorn app.main:app --port 8000 --reload
```

### 生产环境

```bash
# 启动 PostgreSQL + Redis
docker compose up -d

# 后端
cd backend
# 修改 .env: DATABASE_URL=postgresql+asyncpg://lexicon:lexicon123@localhost:5432/lexiconprep
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 前端
npm run build
# 使用 nginx 托管 dist/
```

### Docker Compose

当前编排：PostgreSQL 16 + Redis 7。前端/后端服务需手动启动或扩展 docker-compose.yml。

---

## 9. 环境变量

### 后端 `.env`

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DATABASE_URL | `postgresql+asyncpg://...` | 数据库连接串 |
| REDIS_URL | 空 | Redis 连接串 |
| JWT_SECRET_KEY | ⚠️ 需更换 | JWT 签名密钥 |
| JWT_ALGORITHM | HS256 | JWT 算法 |
| ACCESS_TOKEN_EXPIRE_MINUTES | 15 | Access Token 有效期 |
| REFRESH_TOKEN_EXPIRE_DAYS | 7 | Refresh Token 有效期 |
| RATE_LIMIT_PER_MINUTE | 60 | 全局限流 |
| ALLOWED_ORIGINS | 空 | CORS 允许的源（逗号分隔） |
| DEBUG | false | 调试模式 |

### 前端

| 变量 | 说明 |
|------|------|
| VITE_API_BASE_URL | API 基础 URL（已声明类型，待替换硬编码值） |

---

## 10. 已知问题与待办

详见 [problems.md](./problems.md)，当前统计：

| 优先级 | 数量 | 说明 |
|--------|------|------|
| P0 安全 | 3 | JWT 密钥硬编码、Refresh Token 存 localStorage、路由守卫可绕过 |
| P1 功能 | 7 | 资源文件空壳、多选题未实现、无密码重置、无 404 页面等 |
| P2 质量 | 18 | 错误处理不完善、baseURL 硬编码等 |
| P3 性能 | 8 | 构建体积大、Chart 未销毁、无懒加载等 |
| P4 规范 | 8 | 无测试、无 CI/CD、无 Alembic 迁移等 |

---

## 11. 测试账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 普通用户 | test@lexiconprep.com | test123 |
| 管理员 | admin@lexiconprep.com | admin123 |

---

**适用项目**: LexiconPrep 考研备考平台
