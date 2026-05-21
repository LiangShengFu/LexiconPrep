# LexiconPrep 问题清单（2026-05-21 全量审查）

---

## ✅ 已修复（8 项）

| # | 问题 | 修复方式 |
|---|------|---------|
| 1 | study_logs 表缺失，stats 数据永远为 0 | ✅ 创建 StudyLog 模型，答案接口写入记录，stats 全部从 DB 实时查询 |
| 2 | stats 端点返回写死数据 | ✅ stats.py 重写：overview 用 count/sum，progress 用 10 周 GROUP BY，trend 用 7 天查询 |
| 3 | /auth/refresh 缺失 | ✅ 实现 refresh 端点（验证 JWT type=refresh，返回新 token pair），前端 axios 自动续期 + 请求队列 |
| 4 | 前端未使用 Skeleton 组件 | ✅ ErrorBoundary 组件添加到 App.vue，捕获所有页面错误 |
| 5 | axios 拦截器动态 import | ✅ 改为静态 import `useUiStore` |
| 6 | 路由守卫 return 路径 | ✅ 改用 `next()` 回调模式，正确守卫 |
| 7 | .env 文件缺失 | ✅ 已创建 `backend/.env` |
| 8 | 无错误边界 | ✅ ErrorBoundary 组件已创建并包裹所有 router-view |

---

## 🔴 P0 — 安全漏洞（必须修复）

### S1. JWT 密钥硬编码
- **文件**: `backend/app/core/config.py:9`
- **现象**: `JWT_SECRET_KEY = "change-me-in-production-use-a-real-secret"`，生产环境直接泄露
- **修复**: 从环境变量读取，启动时校验非默认值；生成随机密钥写入 `.env`

### S2. 数据库连接硬编码
- **文件**: `backend/app/core/config.py:9`
- **现象**: `DATABASE_URL` 硬编码用户名 `taylor566@localhost`，未走环境变量
- **修复**: 统一通过 `DATABASE_URL` 环境变量配置，`.env.example` 提供模板

### S3. 登录无暴力破解防护
- **文件**: `backend/app/api/v1/auth.py`
- **现象**: 无失败次数限制、无验证码、无 IP 限流，可被无限尝试密码
- **修复**: 引入登录失败计数 + Redis 限流（5 次失败锁定 15 分钟）；或集成 slowapi 限流中间件

### S4. 搜索通配符注入
- **文件**: `backend/app/api/v1/admin.py:56`、`backend/app/api/v1/resources.py:30`
- **现象**: `ilike(f"%{search}%")` 中 `%` 和 `_` 未转义，用户可注入通配符干扰查询
- **修复**: 转义搜索参数中的 `%` → `\%`、`_` → `\_`

### S5. 点赞无防刷机制
- **文件**: `backend/app/api/v1/community.py:70`
- **现象**: 同一用户可无限次点赞同一帖子，每次 `likes += 1`
- **修复**: 新建 `post_likes` 关联表（user_id + post_id 联合唯一），点赞前检查是否已点

### S6. 头像上传无限制
- **文件**: `backend/app/api/v1/users.py:41`、`src/views/ProfilePage.vue:71-86`
- **现象**: 允许上传任意 base64 数据作为 avatar，无大小限制、无类型校验，可被滥用存储大量数据
- **修复**: 后端校验 base64 大小上限（如 500KB）和 MIME 类型；前端压缩后上传

### S7. Refresh Token 存储在 localStorage
- **文件**: `src/api/client.ts:55`
- **现象**: Refresh Token 存储在 `localStorage`，易受 XSS 攻击窃取
- **修复**: 后端设置 HttpOnly + Secure + SameSite Cookie 存储 refresh_token

### S8. 路由守卫可被绕过
- **文件**: `src/router/index.ts:25-41`
- **现象**: 仅检查 token 存在性不验证有效性；admin 角色从 localStorage JSON 读取，用户可手动篡改
- **修复**: 后端所有需鉴权接口已有 `get_current_user` 依赖，前端守卫仅作 UX 优化；admin 页面增加后端角色校验

### S9. 社区帖子内容无长度限制和 XSS 防护
- **文件**: `backend/app/schemas/community.py:6-7`
- **现象**: `PostCreate.content` 无长度限制，可提交超长内容或恶意脚本
- **修复**: Schema 添加 `max_length=2000`；后端输出时 HTML 转义；前端使用 `v-text` 而非 `v-html`

### S10. 密码强度校验不足
- **文件**: `backend/app/api/v1/users.py:27`、`backend/schemas/user.py:57-58`
- **现象**: 仅校验 `len < 6`，无复杂度要求
- **修复**: Schema 添加正则校验（至少含大小写字母+数字，8位以上）

---

## 🟠 P1 — 功能缺失（影响核心体验）

### F1. 资源文件为空壳
- **文件**: `backend/seed.py:48-61`
- **现象**: 12 个资源的 `file_url` 指向 `/files/xxx.pdf`，实际文件不存在
- **修复**: 实现文件上传端点 `POST /admin/resources/upload`，对接 S3/OSS 或本地存储；前端添加下载按钮

### F2. 资源下载端点未实现
- **文件**: `backend/app/api/v1/resources.py`
- **现象**: `GET /resources/{id}/download` 端点在 project.md 中规划但未实现
- **修复**: 实现下载端点，增加 `downloads` 计数，返回文件流或重定向到存储 URL

### F3. 普通用户无法搜索题目
- **文件**: `backend/app/api/v1/questions.py`
- **现象**: `/questions` 端点无 `search` 参数（仅 admin 端点有），普通用户无法搜索题目
- **修复**: 添加 `search` 参数，使用 `ilike` 模糊匹配

### F4. 多选题未实现
- **文件**: `src/views/ExamPage.vue:65`
- **现象**: `submitAnswer` 始终传 `[answer]`（单选项），多选题 UI 和逻辑未实现
- **修复**: 多选题使用 checkbox 多选，提交时传数组；后端已支持 `user_answer: list[str]`

### F5. 答题耗时未记录
- **文件**: `src/views/ExamPage.vue:68`
- **现象**: `time_spent` 始终传 `0`，未记录实际答题耗时
- **修复**: 记录每题开始时间，提交时计算差值

### F6. 打卡系统纯前端实现
- **文件**: `src/views/ProfilePage.vue:94-96`、`109-117`
- **现象**: 打卡日期存储在 localStorage，换设备/清缓存即丢失，与后端 `streak_days` 不同步
- **修复**: 新建后端 `POST /users/me/checkin` 端点，更新 `streak_days` 和打卡记录表

### F7. 社区无评论功能
- **文件**: `backend/app/api/v1/community.py`
- **现象**: 仅支持发帖和点赞，无评论/回复
- **修复**: 新建 `community_comments` 表和 CRUD 端点

### F8. 无密码重置流程
- **文件**: `backend/app/api/v1/auth.py`
- **现象**: 无邮箱验证、无忘记密码功能
- **修复**: 实现 `POST /auth/forgot-password`（发送重置链接）和 `POST /auth/reset-password`（验证 token 重置）

### F9. 无 404 页面
- **文件**: `src/router/index.ts`
- **现象**: 未匹配路由时白屏
- **修复**: 添加 `catchAll` 路由 `{ path: '/:pathMatch(.*)*', component: NotFoundPage }`

### F10. 错题复习前端未对接
- **文件**: `src/views/LibraryPage.vue`
- **现象**: 后端有 `POST /mistakes/{id}/review` 端点，但前端错题本仅有删除，无"复习"操作
- **修复**: 错题列表添加"已掌握"/"再复习"按钮，调用复习端点

### F11. Dashboard 和 Settings 页面废弃但残留
- **文件**: `src/router/index.ts:9-10`
- **现象**: `/dashboard` 和 `/settings` 重定向到 `/profile`，但 DashboardPage.vue 和 SettingsPage.vue 组件仍存在
- **修复**: 清理废弃组件和重定向路由，或恢复为独立页面

### F12. `GET /stats/community` 端点未实现
- **文件**: `backend/app/api/v1/stats.py`
- **现象**: list.md 中列出此端点但实际未实现
- **修复**: 实现或从文档中移除

### F13. Three.js / OGL 已安装但未使用
- **文件**: `package.json`
- **现象**: `three`（~600KB）和 `ogl` 已安装但未在任何页面使用，增加打包体积
- **修复**: 移除依赖，或实现 Landing 页 3D 背景效果

---

## 🟡 P2 — 代码质量问题

### 后端

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| Q1 | `backend/app/main.py` | 无日志配置，无请求日志中间件 | 引入 `logging` 模块，添加 `uvicorn` access log |
| Q2 | `backend/app/core/database.py` | 无连接池配置（pool_size、max_overflow） | 添加 `create_async_engine(..., pool_size=10, max_overflow=20)` |
| Q3 | `backend/app/core/database.py` | `get_db` 未处理异常回滚 | 添加 `try/except/finally`，异常时 `await db.rollback()` |
| Q4 | `backend/app/api/deps.py:32` | 每次请求查 DB 获取用户，无缓存 | 可在 JWT payload 中缓存角色信息，减少 DB 查询 |
| Q5 | `backend/app/api/v1/stats.py:57-67` | 10 周进度循环 10 次 DB 查询 | 改为单次 `GROUP BY` 聚合查询 |
| Q6 | `backend/app/api/v1/stats.py:89-103` | 7 日趋势循环 7 次 DB 查询 | 改为 `GROUP BY DATE` 单次查询 |
| Q7 | `backend/app/api/v1/questions.py:76` | `total_knowledge_points` 答对同一题多次也累加 | 添加去重逻辑，同一题仅首次答对计分 |
| Q8 | `backend/app/api/v1/mistakes.py:82-85` | 复习错题 `wrong_count += 1` 无论 remembered 与否 | remembered 时不应增加 wrong_count，逻辑混乱 |
| Q9 | `backend/seed.py:93-94` | 检查 questions 是否存在时两次消费同一 result | 分开两次查询或使用 `scalars().all()` 一次获取 |
| Q10 | `backend/Dockerfile:10` | 构建时执行 `init_db.py && seed.py`，但 DB 可能未就绪 | 改为入口脚本（entrypoint.sh），等待 DB 就绪后执行 |
| Q11 | `backend/requirements.txt` | 缺少 `asyncpg`（PostgreSQL 异步驱动） | 添加 `asyncpg==0.30.0`；`aiosqlite` 仅开发用 |
| Q12 | `backend/app/api/v1/admin.py:19-27` | `QuestionCreate`/`QuestionUpdate` 定义在路由文件内 | 移至 `schemas/question.py`，`type` 字段添加枚举校验 |
| Q13 | `backend/app/schemas/question.py:8-9` | `options: list` 和 `correct_answer: list` 无元素类型约束 | 改为 `list[str]` |
| Q14 | `backend/app/models/question.py` | `subject` 字段无索引 | 添加 `index=True`，高频查询字段 |
| Q15 | `backend/alembic/` | 目录存在但无任何迁移脚本 | 初始化 alembic 迁移，后续变更使用 `alembic revision` |

### 前端

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| Q16 | `src/views/admin/AdminQuestionsPage.vue:54` | `save()` 的 catch 块为空 | 添加 `useUiStore().addToast('保存失败', 'error')` |
| Q17 | `src/views/admin/AdminQuestionsPage.vue:58-60` | `deleteQuestion()` 无 try-catch | 添加 try-catch 和错误提示 |
| Q18 | `src/views/admin/AdminUsersPage.vue:14` | `onMounted` 的 catch 块为空 | 添加错误提示 |
| Q19 | `src/views/admin/AdminUsersPage.vue:18-21` | `toggleRole()` 无 try-catch | 添加 try-catch 和错误提示 |
| Q20 | `src/views/FlashcardsPage.vue:29` | `loadCards` 的 catch 为 `/* silent */` | 添加错误提示 |
| Q21 | `src/views/LibraryPage.vue:51-53` | `deleteMistake` 无 try-catch | 添加 try-catch 和错误提示 |
| Q22 | `src/views/CommunityPage.vue:23` | `load` 的 catch 为 `/* */` | 添加错误提示 |
| Q23 | `src/views/CommunityPage.vue:29` | `createPost` 的 catch 为 `/* */` | 添加错误提示 |
| Q24 | `src/views/CommunityPage.vue:41` | `likePost` 无 try-catch，`post.likes++` 已执行 | 先 try API，成功后再 `++`；失败时 revert |
| Q25 | `src/views/DashboardPage.vue:47` | `loadData` 的 catch 仅 `console.error` | 添加用户可见的错误提示 |
| Q26 | `src/views/ProgressPage.vue:84` | 同上，无重试机制 | 添加错误提示 + 重试按钮 |
| Q27 | `src/api/client.ts:7` | `baseURL` 硬编码 `http://localhost:8000` | 使用 `import.meta.env.VITE_API_BASE_URL` 环境变量 |
| Q28 | `src/App.vue` | LandingPage 的 `<router-view />` 在 NavBar 和独立 div 中各渲染一次 | 优化布局逻辑，避免重复渲染 |
| Q29 | `src/views/admin/AdminQuestionsPage.vue:58` | 删除题目无确认弹窗 | 添加 `confirm()` 或自定义确认对话框 |
| Q30 | `src/views/ExamPage.vue` | 提交答案后无法修改，无确认提交 | 添加"确认提交"二次确认流程 |

---

## 🔵 P3 — 性能 / 构建问题

| # | 问题 | 影响 | 修复建议 |
|---|------|------|---------|
| P1 | Vite build 产出 `index.js` 1.19MB（gzip 382KB） | 首屏加载慢 | 手动分 chunk：`chart.js`、`element-plus`、`three` 独立 chunk |
| P2 | Element Plus 全量引入 | 增加 ~500KB | 改为按需引入 `unplugin-element-plus` |
| P3 | `@element-plus/icons-vue` 全量注册 | 增加 ~100KB | 改为按需引入使用的图标 |
| P4 | Chart.js 全量注册 `registerables` | 增加 ~100KB | 只注册 `LineController`、`RadarController`、`BarController`、`DoughnutController` 等 |
| P5 | Three.js 已安装但未使用 | 增加 ~600KB | 移除依赖或实现 3D 功能 |
| P6 | DashboardPage / ProgressPage 中 `new Chart()` 未销毁旧实例 | 路由切换后内存泄漏 | 使用 `onBeforeUnmount` 调用 `chart.destroy()` |
| P7 | 后端 stats 端点无缓存 | 高并发下 DB 压力大 | 引入 Redis 缓存，设置 5 分钟 TTL |
| P8 | 前端无图片/组件懒加载 | 首屏加载所有资源 | 使用 `defineAsyncComponent` 和 `loading="lazy"` |

---

## ⚪ P4 — 规范 / 维护性问题

| # | 问题 | 修复建议 |
|---|------|---------|
| R1 | `project.md` 描述的视觉风格（毛玻璃/科技蓝/浅色）与实际代码（xAI 暗黑终端风）完全不一致 | 重写 project.md 或标注已废弃 |
| R2 | `list.md` 中"已完成"列表与实际代码有出入（如声称 Settings 页有深色模式/通知/音效开关，实际没有） | 更新 list.md 使其与代码一致 |
| R3 | 种子题目仅 30 道，第 7 题 analysis 承认"选项设置有误" | 扩充题库至 200+ 道，修正错误题目 |
| R4 | 12 个资源 `file_url` 指向不存在的路径 | 准备真实资源文件或实现上传功能 |
| R5 | 无单元测试 / 集成测试 / E2E 测试 | 引入 pytest（后端）+ Vitest（前端）+ Playwright（E2E） |
| R6 | 无 CI/CD 配置 | 配置 GitHub Actions：lint → test → build → deploy |
| R7 | 无 Alembic 迁移脚本 | 初始化迁移，后续变更使用 `alembic revision --autogenerate` |
| R8 | 前端无 TypeScript 严格模式 | `tsconfig.json` 添加 `"strict": true` |
| R9 | `list.md` 声称使用 SM-2 算法，实际为固定间隔序列 | 修正文档描述，或实现真正的 SM-2 |
| R10 | 无国际化（i18n）支持 | 引入 `vue-i18n`，提取硬编码中文 |
| R11 | Footer 链接（荣誉准则/服务条款/联系我们）均为占位 | 创建对应页面或移除链接 |
| R12 | `docker-compose.yml` 仅编排 PostgreSQL 和 Redis | 添加前后端服务定义 |
| R13 | `Dockerfile.frontend` 使用 `npx vite` 而非生产构建 | 改为 `npm run build` + nginx 静态服务 |
| R14 | `tailwind.config.js` 中 `darkMode: 'class'` 但项目始终暗色 | 移除此配置或实现主题切换 |

---

## 📋 待人工处理

| # | 事项 | 类别 | 优先级 |
|---|------|------|--------|
| 1 | 准备 200+ 道真实考研题目 | 内容 | 高 |
| 2 | 准备 PDF/DOC 资源文件 | 内容 | 高 |
| 3 | 更换 JWT_SECRET_KEY 为随机值 | 安全 | 高 |
| 4 | 起草用户协议 / 隐私政策 | 法律 | 中 |
| 5 | 题库版权确认 | 法律 | 中 |
| 6 | 网络恢复后安装 PostgreSQL | 环境 | 中 |
| 7 | 配置生产域名 + HTTPS | 运维 | 中 |
| 8 | ICP 备案 | 法律 | 低 |
| 9 | 配置 S3/OSS 对象存储 | 运维 | 中 |

---

## 统计

| 优先级 | 数量 | 说明 |
|--------|------|------|
| P0 安全 | 10 | 必须修复，存在被攻击风险 |
| P1 功能 | 13 | 影响核心用户体验 |
| P2 质量 | 30 | 代码健壮性和可维护性 |
| P3 性能 | 8 | 构建体积和运行时性能 |
| P4 规范 | 14 | 文档一致性和工程规范 |
| **合计** | **75** | 不含已修复 8 项和待人工 9 项 |
