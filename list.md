# LexiconPrep 功能清单

---

## 已完成功能

### 前端 — 9 个页面

| 页面 | 路由 | 功能 |
|------|------|------|
| 首页 | `/` | Hero 大标题、学科分类 Bento Grid、三大特性卡片、Footer |
| 登录 | `/login` | 邮箱密码登录，对接 JWT API，错误提示，未登录自动跳转 |
| 注册 | `/register` | 昵称+邮箱+密码注册，对接注册 API，前端校验 |
| 仪表盘 | `/dashboard` | 4 KPI 卡片、Chart.js 折线图（学习趋势）、雷达图（能力图谱）、错题洞察、快捷入口 — 全部实时 API 数据 |
| 资源库 | `/library` | 双 Tab（资源库/错题本）、搜索防抖、学科/类型筛选、资源卡片、错题列表+删除、空状态 |
| 做题 | `/exam` | 学科选择 → 加载题目 → 选项即提交 → 即时判对错+显示解析 → 答题卡（颜色区分正确/错误/未答）→ 计时器 → 得分页 |
| 闪卡 | `/flashcards` | 学科筛选、翻转卡片、记住/再复习间隔重复、创建闪卡弹窗、删除 |
| 学习进度 | `/progress` | 4 统计卡片、柱状图（每周趋势）、环形图（科目分布）— 全部 API 数据 |
| 社区 | `/community` | 动态流（帖子+点赞+回复）、学习小组在线人数、排行榜 — API 数据 |
| 设置 | `/settings` | 个人信息编辑、每日目标/番茄钟时长滑块、深色模式/通知/音效开关 |

### 前端 — 架构

| 功能 | 状态 |
|------|------|
| Vue 3 + Composition API + TypeScript | 已完成 |
| Vite 开发服务器 | 已完成 |
| Vue Router（10 条路由 + 守卫） | 已完成 |
| Pinia（authStore + uiStore） | 已完成 |
| Axios HTTP 客户端（JWT 注入 + 401 拦截 + 错误 Toast） | 已完成 |
| Element Plus（x.AI 暗色主题深度定制） | 已完成 |
| Tailwind CSS（x.AI 设计 token 全量配置） | 已完成 |
| Chart.js（折线/柱状/雷达/环形图） | 已完成 |
| Toast 全局通知（成功/错误/提示，4 秒自动消失） | 已完成 |
| Skeleton 骨架屏组件 | 已完成 |

### 后端 — 7 个 API 模块

| 模块 | 端点 | 功能 |
|------|------|------|
| Auth | `POST /auth/register` | 注册，bcrypt 加密密码 |
| Auth | `POST /auth/login` | 登录，返回 access_token + refresh_token + user |
| Users | `GET /users/me` | 获取当前用户信息（JWT 认证） |
| Users | `PUT /users/me` | 更新昵称/头像 |
| Questions | `GET /questions` | 题目列表（学科/难度筛选 + 分页） |
| Questions | `GET /questions/{id}` | 单题详情 |
| Questions | `POST /questions/{id}/answer` | 提交答案 → 对错 + 解析；答错自动录入错题本（SM-2 算法） |
| Mistakes | `GET /mistakes` | 错题列表（JOIN 题目内容，按下次复习日排序） |
| Mistakes | `DELETE /mistakes/{id}` | 删除单条错题 |
| Mistakes | `POST /mistakes/{id}/review` | 复习错题（记住→延长间隔，忘记→回到1天） |
| Flashcards | `GET /flashcards` | 闪卡列表（学科筛选 + 分页） |
| Flashcards | `POST /flashcards` | 创建闪卡（自动设置首次复习日） |
| Flashcards | `PUT /flashcards/{id}` | 更新闪卡内容 |
| Flashcards | `DELETE /flashcards/{id}` | 删除闪卡 |
| Flashcards | `POST /flashcards/{id}/review` | 复习闪卡（SM-2 间隔：1→3→7→14→30→60天） |
| Resources | `GET /resources` | 资源列表（学科/类型筛选 + 搜索 + 分页） |
| Resources | `GET /resources/{id}` | 资源详情 |
| Stats | `GET /stats/overview` | 用户 KPI 概览 |
| Stats | `GET /stats/progress` | 每周趋势 + 科目分布 |
| Stats | `GET /stats/trend` | 7 日每日做题量 |
| Stats | `GET /stats/community` | 社区动态 + 小组 + 排行榜 |

### 后端 — 架构

| 功能 | 状态 |
|------|------|
| FastAPI + async | 已完成 |
| SQLAlchemy 2.0 async ORM | 已完成 |
| SQLite（零外部依赖开发模式） | 已完成 |
| JWT 认证（access 15min + refresh 7day） | 已完成 |
| bcrypt 密码加密（强度 12） | 已完成 |
| CORS 中间件 | 已完成 |
| Swagger UI 自动文档（`/docs`） | 已完成 |
| 种子数据（30 道题 + 12 个资源 + 测试用户） | 已完成 |
| SM-2 间隔重复算法 | 已完成 |
| Dockerfile + docker-compose.yml | 已完成 |

---

## 未完成功能

### 高优先级

| 功能 | 说明 |
|------|------|
| **学习记录持久化** | 当前答题判分后未写入 `study_logs` 表，stats 数据为写死值。需在 `/questions/{id}/answer` 中写入 study_logs，stats 端点从 DB 实时查询 |
| **Token 刷新** | `/auth/refresh` 端点未实现，前端 access_token 过期后直接跳登录，体验差 |
| **管理员后台** | 题目管理（增删改查）、用户管理、资源上传 — 无界面 |
| **真实数据库** | 当前用 SQLite 开发。生产环境需切换 PostgreSQL（已有 Docker 配置模板） |
| **Redis 缓存** | 热点数据（题库列表、资源列表）无缓存层 |

### 中优先级

| 功能 | 说明 |
|------|------|
| **社区发帖** | 当前社区动态为只读 API 写死数据。需帖子 CRUD + 点赞 + 评论 |
| **学习小组** | 创建/加入小组、组内讨论 — 无后端 |
| **文件上传/下载** | 资源库当前为写死 URL，无真实文件上传和下载计数 |
| **搜索** | 题目搜索（`/questions?search=`）、资源全文搜索 未实现 |
| **认证邮箱验证** | 注册无邮箱验证，无密码重置功能 |
| **用户头像上传** | Settings 页无头像上传功能 |

### 低优先级

| 功能 | 说明 |
|------|------|
| **国际化 i18n** | 无多语言支持 |
| **暗色/浅色切换** | Settings 页有开关但 x.AI 设计系统为纯暗色，浅色需要完整设计 |
| **PWA 离线支持** | 无 Service Worker |
| **E2E 测试** | 无 Cypress/Playwright 测试 |
| **CI/CD** | GitHub Actions 流水线未配置 |

---

## 扩展功能（未来版本）

| 功能 | 说明 |
|------|------|
| **AI 智能推荐** | 根据错题分析薄弱知识点，推荐针对性练习 |
| **AI 闪卡生成** | 输入知识点 → LLM 自动生成闪卡 |
| **实时视频课程** | 直播 + 录播课程（project.md 标注为 Phase 2） |
| **在线支付** | 订阅制付费（project.md 标注为 Phase 2） |
| **学习提醒推送** | Web Push / 微信小程序推送 |
| **移动端 App** | React Native / Flutter |
| **多人对战模式** | 实时 PK 做题 |
| **语音朗读** | 英语单词/文章 TTS |
| **OCR 导入** | 拍照导入纸质错题 |

---

## 需要人工准备的事项

### 内容准备

- [ ] **题库数据** — 当前只有 30 道种子题（10政治+10英语+10数学），需准备至少 500+ 道真实考研真题，覆盖各学科、各章节、各难度
- [ ] **资源文件** — 12 个资源为元数据占位，`file_url` 指向 `/files/` 但实际文件不存在。需准备 PDF/DOC/视频文件
- [ ] **闪卡内容** — 需准备各学科高频考点闪卡数据
- [ ] **社区初始内容** — 当前为固定写死数据，正式上线需清理

### 环境配置

- [ ] **JWT 密钥** — `backend/.env` 中 `JWT_SECRET_KEY` 当前为 `change-me-in-production-use-a-real-secret`，需更换为随机密钥
- [ ] **数据库密码** — 切换到 PostgreSQL 后需配置强密码
- [ ] **HTTPS 证书** — 生产环境必须启用 TLS
- [ ] **域名** — 前端/后端需配置正式域名和 CORS

### 运维准备

- [ ] **Docker 环境** — 安装 Docker Desktop 或服务器 Docker Engine
- [ ] **PostgreSQL 16** — 或使用 Docker 启动：`docker run -d --name lexicon-db -e POSTGRES_DB=lexiconprep -e POSTGRES_USER=lexicon -e POSTGRES_PASSWORD=<强密码> -p 5432:5432 postgres:16`
- [ ] **Redis 7** — 或使用 Docker: `docker run -d --name lexicon-redis -p 6379:6379 redis:7`
- [ ] **生产服务器** — AWS EC2 / 阿里云 ECS（至少 2C4G）
- [ ] **对象存储** — AWS S3 / 阿里云 OSS（资源文件存储）

### 法律与合规

- [ ] **ICP 备案** — 中国上线需完成域名备案
- [ ] **用户协议 & 隐私政策** — 当前 Footer 链接为占位，需起草法律文档
- [ ] **题库版权** — 确认种子题目无版权风险
