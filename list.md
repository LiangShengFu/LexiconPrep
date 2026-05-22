# LexiconPrep 功能清单

> 最后更新：2026-05-22 | 基于代码实际状态审查

---

## 已完成功能

### 前端 — 13 个页面（11 活跃 + 2 废弃重定向）

| 页面 | 路由 | 功能 | 认证 |
|------|------|------|------|
| 首页 | `/` | WebGL 矩阵背景 + 逐字解密标题 + Hero 大标题 + 学科 Bento Grid + 三大特性卡片 + Footer | 无 |
| 登录 | `/login` | 邮箱密码登录，对接 JWT API，错误提示，未登录自动跳转 | 无 |
| 注册 | `/register` | 昵称+邮箱+密码注册，对接注册 API，邮箱+昵称唯一性校验 | 无 |
| 个人主页 | `/profile` | 日历打卡（后端化）、头像上传（base64 ≤500KB）、个人信息编辑、密码修改（复杂度校验） | JWT |
| 资源库 | `/library` | 双 Tab（资源库/错题本）、搜索防抖、学科/类型筛选、资源卡片、错题列表+删除 | JWT |
| 做题 | `/exam` | 学科选择 → 加载题目 → 选项即提交 → 即时判对错+显示解析 → 答题卡（颜色区分正确/错误/未答）→ 计时器 → 得分页 | JWT |
| 闪卡 | `/flashcards` | 学科筛选、翻转卡片、记住/再复习间隔重复、创建闪卡弹窗、删除 | JWT |
| 学习进度 | `/progress` | 4 统计卡片、柱状图（每周趋势）、环形图（科目分布）— 全部 API 实时数据 | JWT |
| 社区 | `/community` | 发帖、点赞（防重复）、删除帖子（仅作者）、排行榜（7日做题量）— 数据库持久化 | JWT |
| 番茄钟 | `/pomodoro` | 悬浮小窗 + 独立全屏页面，自定义时长，SVG 圆环进度 | 无 |
| 管理概览 | `/admin` | 系统统计（用户数/题目数/答题数/学科分布） | Admin |
| 管理题目 | `/admin/questions` | 题目 CRUD（创建/编辑/删除），学科/搜索筛选 | Admin |
| 管理用户 | `/admin/users` | 用户列表、角色切换（自保护：不可修改自己） | Admin |
| ~~仪表盘~~ | `/dashboard` | **已废弃**，重定向到 `/profile` | - |
| ~~设置~~ | `/settings` | **已废弃**，重定向到 `/profile` | - |

### 前端 — 架构

| 功能 | 状态 | 说明 |
|------|------|------|
| Vue 3 + Composition API + TypeScript | ✅ 已完成 | 严格模式（strict + noUnusedLocals + noUnusedParameters） |
| Vite 6 开发服务器 | ✅ 已完成 | |
| Vue Router（15 条路由 + 认证守卫 + 管理员守卫） | ✅ 已完成 | `next()` 回调模式 |
| Pinia（authStore + uiStore） | ✅ 已完成 | |
| Axios HTTP 客户端 | ✅ 已完成 | JWT 注入 + 401 拦截 + Token 刷新队列 + 422/500 错误 Toast |
| Element Plus（xAI 暗色主题深度定制） | ✅ 已完成 | |
| Tailwind CSS（xAI 暗色设计 token 全量配置） | ✅ 已完成 | |
| Chart.js（折线/柱状/雷达/环形图） | ✅ 已完成 | |
| Toast 全局通知（成功/错误/提示，4 秒自动消失） | ✅ 已完成 | |
| Skeleton 骨架屏组件 | ✅ 已完成 | |
| ErrorBoundary 错误边界 | ✅ 已完成 | 包裹所有 router-view |
| WebGL 终端矩阵背景（FaultyTerminal） | ✅ 已完成 | 细粒度 watch + SSR 守卫 |
| 自定义十字光标（TargetCursor） | ✅ 已完成 | 全局事件监听正确清理 |
| 逐字解密动画（DecryptedText） | ✅ 已完成 | |
| 番茄钟悬浮组件（PomodoroTimer） | ✅ 已完成 | |

### 后端 — 9 个 API 模块

| 模块 | 端点 | 功能 |
|------|------|------|
| Auth | `POST /auth/register` | 注册，bcrypt 加密密码，邮箱+昵称唯一性校验 |
| Auth | `POST /auth/login` | 登录，返回 access_token + refresh_token + user，限流 5 次/分钟 |
| Auth | `POST /auth/refresh` | 刷新 Token（验证 type=refresh），返回新 token pair |
| Users | `GET /users/me` | 获取当前用户信息（JWT 认证） |
| Users | `PUT /users/me` | 更新昵称/头像（≤500KB, base64, MIME 校验） |
| Users | `PUT /users/me/password` | 修改密码（复杂度：≥8位+大写+小写+数字） |
| Users | `POST /users/me/checkin` | 打卡（后端化，更新 streak_days，防重复打卡） |
| Questions | `GET /questions/subjects` | 获取学科列表 |
| Questions | `GET /questions` | 题目列表（学科/难度筛选 + 分页） |
| Questions | `GET /questions/{id}` | 单题详情 |
| Questions | `POST /questions/{id}/answer` | 提交答案 → 判对错 + 写 study_log + 自动录入/标记错题（去重计分） |
| Mistakes | `GET /mistakes` | 错题列表（仅未掌握，JOIN 题目内容，按下次复习日排序） |
| Mistakes | `DELETE /mistakes/{id}` | 删除单条错题 |
| Mistakes | `POST /mistakes/{id}/review` | 复习错题（remembered→标记已掌握+延长间隔，忘记→wrong_count+1+重置1天） |
| Flashcards | `GET /flashcards` | 闪卡列表（学科筛选 + 分页） |
| Flashcards | `POST /flashcards` | 创建闪卡（自动设置首次复习日） |
| Flashcards | `PUT /flashcards/{id}` | 更新闪卡内容 |
| Flashcards | `DELETE /flashcards/{id}` | 删除闪卡 |
| Flashcards | `POST /flashcards/{id}/review` | 复习闪卡（间隔：1→3→7→14→30→60天） |
| Resources | `GET /resources` | 资源列表（学科/类型/搜索 + 分页，搜索注入防护） |
| Resources | `GET /resources/{id}` | 资源详情 |
| Stats | `GET /stats/overview` | 用户 KPI 概览（实时 DB 聚合查询） |
| Stats | `GET /stats/progress` | 10 周趋势 + 科目分布（单次 GROUP BY 查询） |
| Stats | `GET /stats/trend` | 7 日每日做题量（单次 GROUP BY DATE 查询） |
| Community | `GET /community/posts` | 帖子列表（JOIN 用户昵称） |
| Community | `POST /community/posts` | 发帖（≤2000 字） |
| Community | `POST /community/posts/{id}/like` | 点赞（PostLike 联合唯一约束防重复） |
| Community | `DELETE /community/posts/{id}` | 删除帖子（仅作者可删） |
| Community | `GET /community/leaderboard` | 7 日做题量排行榜 |
| Admin | `GET /admin/questions` | 题目列表（搜索 + 分页） |
| Admin | `POST /admin/questions` | 创建题目 |
| Admin | `PUT /admin/questions/{id}` | 更新题目 |
| Admin | `DELETE /admin/questions/{id}` | 删除题目（级联删除 mistakes + study_logs） |
| Admin | `GET /admin/users` | 用户列表 |
| Admin | `PUT /admin/users/{id}/role` | 修改用户角色（自保护：不可修改自己） |
| Admin | `GET /admin/stats` | 系统统计 |
| Health | `GET /health` | 服务健康检查 |

### 后端 — 架构

| 功能 | 状态 | 说明 |
|------|------|------|
| FastAPI + async | ✅ 已完成 | |
| SQLAlchemy 2.0 async ORM | ✅ 已完成 | mapped_column + 连接池（pool_size=10, max_overflow=20） |
| PostgreSQL 16（生产）/ SQLite（开发） | ✅ 已完成 | 通过 DATABASE_URL 切换 |
| JWT 认证（access 15min + refresh 7day） | ✅ 已完成 | |
| bcrypt 密码加密 | ✅ 已完成 | passlib CryptContext |
| CORS 动态配置 | ✅ 已完成 | 从 ALLOWED_ORIGINS 环境变量读取 |
| 请求限流 | ✅ 已完成 | slowapi：登录 5 次/分钟 + 全局 60 次/分钟 |
| 日志中间件 | ✅ 已完成 | ≥400 状态码记录警告 |
| Swagger UI 自动文档（`/docs`） | ✅ 已完成 | |
| 搜索注入防护 | ✅ 已完成 | escape_search 转义 % 和 _ |
| 种子数据（30 道题 + 12 个资源 + 2 用户 + 4 帖子） | ✅ 已完成 | |
| 固定间隔重复算法 | ✅ 已完成 | 1→3→7→14→30→60 天（非 SM-2） |
| Dockerfile + docker-compose.yml | ✅ 已完成 | PostgreSQL 16 + Redis 7 |
| 会话异常回滚 | ✅ 已完成 | get_db 添加 try/except/finally |
| 连接池配置 | ✅ 已完成 | pool_size=10, max_overflow=20, pool_pre_ping=True |

---

## 未完成功能

### 高优先级

| 功能 | 说明 | 现状 |
|------|------|------|
| **资源文件为空壳** | 12 个资源的 `file_url` 指向 `/files/xxx.pdf`，实际文件不存在 | 需实现文件上传端点或准备真实文件 |
| **资源下载端点** | `GET /resources/{id}/download` 在 project.md 中规划但未实现 | 需实现下载端点 + downloads 计数 |
| **多选题前端** | 后端已支持 `user_answer: list[str]`，但前端 ExamPage 始终传单选项 | 需实现 checkbox 多选 UI |
| **答题耗时** | `time_spent` 始终传 `0` | 需记录每题开始时间 |
| **无 404 页面** | 未匹配路由时白屏 | 需添加 catchAll 路由 |
| **错题复习前端** | 后端有 `POST /mistakes/{id}/review`，前端仅有删除 | 需添加"已掌握"/"再复习"按钮 |
| **普通用户题目搜索** | `/questions` 端点无 `search` 参数（仅 admin 有） | 需添加搜索参数 |

### 中优先级

| 功能 | 说明 |
|------|------|
| **社区评论** | 仅支持发帖和点赞，无评论/回复功能 |
| **密码重置** | 无邮箱验证、无忘记密码功能 |
| **文件上传** | 资源库无真实文件上传和下载计数 |
| **用户头像文件上传** | 当前为 base64 存储，应改为文件上传 + CDN |
| **学科列表动态化** | 前端 ExamPage 和 LibraryPage 学科列表硬编码 |
| **DashboardPage / SettingsPage 清理** | 组件文件仍存在但已废弃重定向 |

### 低优先级

| 功能 | 说明 |
|------|------|
| **国际化 i18n** | 无多语言支持 |
| **暗色/浅色切换** | 项目为纯暗色设计，浅色需完整设计 |
| **PWA 离线支持** | 无 Service Worker |
| **E2E 测试** | 无 Cypress/Playwright 测试 |
| **CI/CD** | GitHub Actions 流水线未配置 |
| **Alembic 迁移** | 目录存在但无迁移脚本 |

---

## 扩展功能（未来版本）

| 功能 | 说明 |
|------|------|
| **AI 智能推荐** | 根据错题分析薄弱知识点，推荐针对性练习 |
| **AI 闪卡生成** | 输入知识点 → LLM 自动生成闪卡 |
| **实时视频课程** | 直播 + 录播课程 |
| **在线支付** | 订阅制付费 |
| **学习提醒推送** | Web Push / 微信小程序推送 |
| **移动端 App** | React Native / Flutter |
| **多人对战模式** | 实时 PK 做题 |
| **语音朗读** | 英语单词/文章 TTS |
| **OCR 导入** | 拍照导入纸质错题 |

---

## 需要人工准备的事项

### 内容准备

- [ ] **题库数据** — 当前 30 道种子题（10政治+10英语+10数学），需准备至少 500+ 道真实考研真题
- [ ] **资源文件** — 12 个资源为元数据占位，`file_url` 指向 `/files/` 但实际文件不存在
- [ ] **闪卡内容** — 需准备各学科高频考点闪卡数据
- [ ] **种子题修正** — 第 7 题 analysis 承认"选项设置有误"，需修正

### 环境配置

- [ ] **JWT 密钥** — `backend/.env` 中 `JWT_SECRET_KEY` 需更换为随机密钥
- [ ] **数据库密码** — 切换到 PostgreSQL 后需配置强密码（当前 docker-compose 为 lexicon123）
- [ ] **HTTPS 证书** — 生产环境必须启用 TLS
- [ ] **域名** — 前端/后端需配置正式域名和 CORS
- [ ] **VITE_API_BASE_URL** — 前端 `client.ts` 中 baseURL 仍硬编码为 `http://localhost:8000`

### 运维准备

- [ ] **Docker 环境** — 安装 Docker Desktop 或服务器 Docker Engine
- [ ] **PostgreSQL 16** — 或使用 Docker 启动：`docker compose up -d db`
- [ ] **Redis 7** — 或使用 Docker: `docker compose up -d redis`
- [ ] **生产服务器** — AWS EC2 / 阿里云 ECS（至少 2C4G）
- [ ] **对象存储** — AWS S3 / 阿里云 OSS（资源文件存储）
- [ ] **nginx** — 前端生产部署需 nginx 托管静态文件

### 法律与合规

- [ ] **ICP 备案** — 中国上线需完成域名备案
- [ ] **用户协议 & 隐私政策** — Footer 链接为占位，需起草法律文档
- [ ] **题库版权** — 确认种子题目无版权风险
