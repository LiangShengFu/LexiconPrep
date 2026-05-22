# LexiconPrep 问题清单（2026-05-21 深度审查 v2）

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

---

## 🔍 深度审查补充（v2 新增）

### A. 无障碍性（a11y）问题

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| A1 | 全局 | 所有 `<button>` 使用 `<button>` 标签但无 `aria-label`，图标按钮（如删除、编辑、返回）无文字说明 | 添加 `aria-label` 属性 |
| A2 | 全局 | 22 处 `focus:outline-none` 移除了所有焦点轮廓，键盘用户无法识别当前聚焦元素 | 改为 `focus:outline-none focus:ring-2 focus:ring-ink` 保留可见焦点 |
| A3 | `src/components/TargetCursor.vue:33` | `hideDefaultCursor: true` 隐藏系统光标，影响无障碍使用 | 提供可配置选项，默认不隐藏 |
| A4 | `src/views/ExamPage.vue` | 答题选项使用 `<button>` 但无 `role="radio"` 或 `aria-checked`，屏幕阅读器无法识别为选项组 | 添加 `role="radiogroup"` + `role="radio"` + `aria-checked` |
| A5 | `src/views/FlashcardsPage.vue:96` | 闪卡翻转仅依赖 `@click`，无键盘操作支持 | 添加 `@keyup.enter` / `@keydown.space` 和 `tabindex="0"` |
| A6 | `src/components/ToastContainer.vue` | Toast 通知无 `role="alert"` 或 `aria-live="polite"`，屏幕阅读器不会播报 | 添加 `role="alert"` 和 `aria-live="polite"` |
| A7 | `src/views/ProfilePage.vue:131` | 头像上传 `<input type="file">` 隐藏在 `<label>` 内，但 label 无描述性文字 | 添加 `aria-label="上传头像"` |
| A8 | `src/components/ErrorBoundary.vue` | 错误边界无 `role="alert"` | 添加 `role="alert"` |
| A9 | `src/views/PomodoroPage.vue` | 番茄钟全屏模式无 `aria-label` 描述计时器状态 | 添加 `aria-label` 和 `aria-live` |
| A10 | `index.html:10` | 仅加载了 Courier Prime 字体，缺少 Geist Mono 和 JetBrains Mono 的 Google Fonts 链接，回退到系统字体 | 添加字体 CDN 或本地字体文件 |

### B. 响式 / 移动端问题

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| B1 | `src/components/NavBar.vue:34` | 导航链接 `hidden md:flex`，移动端无汉堡菜单，无法导航 | 添加移动端汉堡菜单 |
| B2 | `src/components/AppShell.vue:38` | 侧边栏固定 `w-56`，移动端占据过多空间 | 添加移动端折叠/抽屉式侧边栏 |
| B3 | `src/views/ExamPage.vue:139` | 答题区 `lg:grid-cols-4`，移动端答题卡占满宽度，题目区域被压缩 | 优化移动端布局，答题卡改为底部浮动 |
| B4 | `src/views/PomodoroPage.vue:63` | 番茄钟 SVG 固定 `400x400px`，小屏幕溢出 | 改为响应式尺寸 `max-w-[400px] w-full` |
| B5 | `src/views/CommunityPage.vue:68` | 发帖区 textarea 无 `max-height` 限制，移动端可能撑满屏幕 | 添加 `max-h-[120px]` |
| B6 | `src/components/FaultyTerminal.vue` | WebGL 终端特效在低端移动设备上可能导致性能问题 | 检测设备性能，低端设备降级或跳过渲染 |

### C. 业务逻辑 / 数据一致性问题

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| C1 | `backend/app/api/v1/questions.py:86-95` | 答错时自动创建错题记录，但答对时不检查是否已有错题记录（已掌握的题不应再出现在错题本中） | 答对时检查并标记已有错题记录为"已掌握" |
| C2 | `backend/app/api/v1/mistakes.py:82-85` | 复习错题时 `wrong_count += 1` 无论 remembered 与否，语义混乱 | remembered 时不增加 wrong_count，增加 `review_count` 字段 |
| C3 | `backend/app/api/v1/stats.py` | `overview` 和 `progress` 端点返回的 `streak_days` 来自 User 表，但打卡系统是前端 localStorage 实现，两者不同步 | 统一打卡逻辑到后端 |
| C4 | `backend/app/services/auth.py` | `decode_token` 函数已定义但**从未被使用**（deps.py 直接内联了相同逻辑） | 删除或统一使用 |
| C5 | `backend/app/api/v1/auth.py` | 注册时未校验 nickname 唯一性，两个用户可以有相同昵称 | 添加 nickname 唯一性校验或接受重复 |
| C6 | `backend/app/api/v1/questions.py:76` | `total_knowledge_points` 每次答对 +1，但重复答对同一题也累加，且答错不减少 | 添加 StudyLog 去重查询，同一题仅首次答对计分 |
| C7 | `backend/app/api/v1/admin.py:93-105` | 删除题目时不级联删除关联的 mistakes 和 study_logs 记录 | 添加级联删除或软删除 |
| C8 | `backend/app/api/v1/admin.py:122-135` | 管理员可将任何用户（包括自己）降级为普通用户，可能导致无管理员 | 添加自保护逻辑：不允许降级最后一个管理员 |
| C9 | `src/views/ExamPage.vue:25` | 学科列表硬编码为 `['政治', '英语', '数学']`，与后端实际学科不同步 | 从后端获取学科列表或提取为常量 |
| C10 | `src/views/LibraryPage.vue:25` | 资源库学科列表硬编码为 6 个，与种子数据不完全匹配 | 从后端动态获取学科列表 |
| C11 | `backend/app/api/v1/community.py:99` | 排行榜 `cutoff` 使用 `datetime.utcnow()`，但数据库中 `timestamp` 使用 `server_default=func.now()`，两者时区可能不一致 | 统一使用 UTC 时区感知的 datetime |
| C12 | 后端全局 | 14 处使用 `datetime.utcnow()`（已弃用），Python 3.12+ 推荐使用 `datetime.now(timezone.utc)` | 全局替换为 `datetime.now(timezone.utc)` |

### D. 组件级问题

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| D1 | `src/components/FaultyTerminal.vue:293` | `watch(() => props, ..., { deep: true })` 任何 prop 变化都触发完整重建（cleanup + setup），性能极差 | 细粒度 watch，仅监听变化的 prop 并更新对应 uniform |
| D2 | `src/components/FaultyTerminal.vue:196` | `dpr` 默认值 `Math.min(window.devicePixelRatio \|\| 1, 2)` 在 SSR 或 Node 环境下 `window` 不存在 | 添加 `typeof window !== 'undefined'` 守卫 |
| D3 | `src/components/TargetCursor.vue:58` | `window.addEventListener('mousemove', ...)` 全局监听但未在 cleanupAnimation 中移除 | 在 cleanupAnimation 中移除 mousemove 和 mouseover 全局监听 |
| D4 | `src/components/TargetCursor.vue:60` | `window.addEventListener('mouseover', ...)` 同上，全局监听未清理 | 同上 |
| D5 | `src/components/SkeletonLoader.vue:13` | `Math.random()` 在模板中使用，每次渲染产生不同的宽度，导致布局抖动 | 使用固定宽度或基于 index 的确定性值 |
| D6 | `src/components/DecryptedText.vue:87` | watch 监听了 8 个依赖项，任何变化都重置动画，过于激进 | 仅在关键 props（text、animateOn）变化时重置 |
| D7 | `src/components/ToastContainer.vue:12` | Toast 位置固定 `bottom-6 right-6`，与 PomodoroTimer 组件位置重叠 | Toast 改为 `top-6 right-6` 或动态调整位置 |
| D8 | `src/components/ErrorBoundary.vue:13` | `retry()` 仅重置状态，不重新挂载子组件，可能无法真正恢复 | 使用 `:key` 强制重新渲染子组件 |

### E. 配置 / 环境问题

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| E1 | `backend/.env.example:9` | JWT_SECRET_KEY 示例值与代码默认值相同，用户可能直接使用 | 示例值改为 `<your-secret-key-here>` |
| E2 | `backend/.env.example` | 缺少 `RATE_LIMIT_PER_MINUTE` 和 `DEBUG` 配置项 | 补充完整配置模板 |
| E3 | `.gitignore` | 缺少 `*.env`（仅有 `.env`）、`backend/.env`、`node_modules` 的精确路径 | 补充 `.env*`、`backend/*.db` 等 |
| E4 | `index.html` | 缺少 `<meta name="description">` SEO 标签 | 添加描述和 Open Graph 标签 |
| E5 | `env.d.ts` | 未声明 `import.meta.env.VITE_API_BASE_URL` 类型 | 添加 `ImportMetaEnv` 接口声明 |
| E6 | `tsconfig.json:14` | `strict: true` 已启用，但 `noUnusedLocals: false` 和 `noUnusedParameters: false` 放宽了检查 | 逐步启用，清理未使用的变量和参数 |
| E7 | `backend/app/main.py:23-28` | CORS `allow_origins` 硬编码 `localhost:3000` 和 `localhost:5173`，生产环境需手动修改 | 从环境变量读取 `ALLOWED_ORIGINS` |
| E8 | `backend/app/core/config.py` | `RATE_LIMIT_PER_MINUTE` 已定义但**从未使用** | 实现限流中间件或移除配置 |

---

## v2 统计更新

| 优先级 | v1 数量 | v2 新增 | 合计 |
|--------|---------|---------|------|
| P0 安全 | 10 | 0 | 10 |
| P1 功能 | 13 | 0 | 13 |
| P2 质量 | 30 | +30 | 60 |
| P3 性能 | 8 | +1 | 9 |
| P4 规范 | 14 | +8 | 22 |
| **合计** | **75** | **+39** | **114** |
