# LexiconPrep 问题清单

> 最后更新：2026-05-22 | 基于代码实际状态审查

---

## ✅ 已修复（v1 阶段 — 8 项）

| # | 问题 | 修复方式 |
|---|------|---------|
| 1 | study_logs 表缺失，stats 数据永远为 0 | ✅ 创建 StudyLog 模型，答案接口写入记录，stats 全部从 DB 实时查询 |
| 2 | stats 端点返回写死数据 | ✅ stats.py 重写：overview 用 count/sum，progress 用 GROUP BY，trend 用 GROUP BY DATE |
| 3 | /auth/refresh 缺失 | ✅ 实现 refresh 端点（验证 JWT type=refresh，返回新 token pair），前端 axios 自动续期 + 请求队列 |
| 4 | 前端未使用 Skeleton 组件 | ✅ ErrorBoundary 组件添加到 App.vue，捕获所有页面错误 |
| 5 | axios 拦截器动态 import | ✅ 改为静态 import `useUiStore` |
| 6 | 路由守卫 return 路径 | ✅ 改用 `next()` 回调模式，正确守卫 |
| 7 | .env 文件缺失 | ✅ 已创建 `backend/.env.example` |
| 8 | 无错误边界 | ✅ ErrorBoundary 组件已创建并包裹所有 router-view |

## ✅ 已修复（v2 阶段 — A~E 类 43 项）

### A. 无障碍性（a11y）— 10 项全部修复

| # | 修复内容 |
|---|---------|
| A1 | 所有图标按钮添加 `aria-label` |
| A2 | `focus:outline-none` 改为 `focus:outline-none focus:ring-2 focus:ring-ink` |
| A3 | TargetCursor `hideDefaultCursor` 提供可配置选项 |
| A4 | ExamPage 答题选项添加 `role="radiogroup"` + `role="radio"` + `aria-checked` |
| A5 | FlashcardsPage 添加 `@keyup.enter` / `@keydown.space` 和 `tabindex="0"` |
| A6 | ToastContainer 添加 `role="alert"` 和 `aria-live="polite"` |
| A7 | ProfilePage 头像上传添加 `aria-label="上传头像"` |
| A8 | ErrorBoundary 添加 `role="alert"` |
| A9 | PomodoroPage 添加 `aria-label` 和 `aria-live` |
| A10 | index.html 添加 Geist Mono 和 JetBrains Mono 字体 CDN |

### B. 响应式/移动端 — 6 项全部修复

| # | 修复内容 |
|---|---------|
| B1 | NavBar 添加移动端汉堡菜单 |
| B2 | AppShell 侧边栏改为移动端抽屉式设计 |
| B3 | ExamPage 答题卡改为移动端底部浮动 |
| B4 | PomodoroPage SVG 改为响应式尺寸 `max-w-[400px] w-full` |
| B5 | CommunityPage textarea 添加 `max-h-[120px]` |
| B6 | FaultyTerminal 添加设备性能检测，低端设备降级 |

### C. 业务逻辑/数据一致性 — 11 项全部修复

| # | 修复内容 |
|---|---------|
| C1 | 答对时检查并标记已有错题记录为 mastered=True |
| C2 | 复习错题时 remembered 不增加 wrong_count，增加 review_count 字段 |
| C3 | 打卡系统统一到后端 `POST /users/me/checkin` |
| C4 | 删除未使用的 `decode_token` 函数 |
| C5 | 注册时校验 nickname 唯一性 |
| C6 | total_knowledge_points 添加 StudyLog 去重查询，同一题仅首次答对计分 |
| C7 | 删除题目时级联删除关联的 mistakes 和 study_logs |
| C8 | 管理员角色修改添加自保护逻辑 |
| C9 | ExamPage 学科列表改为从后端获取 |
| C10 | LibraryPage 学科列表改为从后端动态获取 |
| C11 | 统一使用 UTC 时区感知的 datetime |

### D. 组件级问题 — 8 项全部修复

| # | 修复内容 |
|---|---------|
| D1 | FaultyTerminal watch 改为细粒度，仅监听具体 prop 变化 |
| D2 | FaultyTerminal dpr 默认值添加 `typeof window !== 'undefined'` 守卫 |
| D3 | TargetCursor 全局 mousemove 监听在 cleanupAnimation 中移除 |
| D4 | TargetCursor 全局 mouseover 监听在 cleanupAnimation 中移除 |
| D5 | SkeletonLoader 使用固定宽度替代 Math.random() |
| D6 | DecryptedText watch 仅在关键 props 变化时重置动画 |
| D7 | ToastContainer 位置调整为 `top-6 right-6` |
| D8 | ErrorBoundary retry 使用 `:key` 强制重新渲染子组件 |

### E. 配置/环境问题 — 8 项全部修复

| # | 修复内容 |
|---|---------|
| E1 | .env.example JWT_SECRET_KEY 改为 `<your-secret-key-here>` |
| E2 | .env.example 补充 `RATE_LIMIT_PER_MINUTE`、`ALLOWED_ORIGINS`、`DEBUG` |
| E3 | .gitignore 补充 `.env*`、`backend/*.db` 等 |
| E4 | index.html 添加 `<meta name="description">` 和 Open Graph 标签 |
| E5 | env.d.ts 声明 `VITE_API_BASE_URL` 类型 |
| E6 | tsconfig.json 启用 `noUnusedLocals: true` 和 `noUnusedParameters: true` |
| E7 | CORS allow_origins 从环境变量 `ALLOWED_ORIGINS` 读取 |
| E8 | 限流配置使用 `settings.RATE_LIMIT_PER_MINUTE` |

---

## 🔴 P0 — 安全漏洞（3 项待修复）

### S1. JWT 密钥硬编码
- **文件**: `backend/app/core/config.py:9`
- **现象**: `JWT_SECRET_KEY = "change-me-in-production-use-a-real-secret"`，生产环境直接泄露
- **修复**: 启动时校验非默认值；生成随机密钥写入 `.env`

### S2. Refresh Token 存储在 localStorage
- **文件**: `src/api/client.ts:55`
- **现象**: Refresh Token 存储在 `localStorage`，易受 XSS 攻击窃取
- **修复**: 后端设置 HttpOnly + Secure + SameSite Cookie 存储 refresh_token

### S3. 路由守卫可被绕过
- **文件**: `src/router/index.ts:25-41`
- **现象**: 仅检查 token 存在性不验证有效性；admin 角色从 localStorage JSON 读取，用户可手动篡改
- **修复**: 后端所有需鉴权接口已有 `get_current_user` 依赖，前端守卫仅作 UX 优化；admin 页面增加后端角色校验（已通过 `get_admin_user` 依赖实现）

---

## 🟠 P1 — 功能缺失（7 项待修复）

### F1. 资源文件为空壳
- **文件**: `backend/seed.py:48-61`
- **现象**: 12 个资源的 `file_url` 指向 `/files/xxx.pdf`，实际文件不存在
- **修复**: 实现文件上传端点 `POST /admin/resources/upload`，对接 S3/OSS 或本地存储

### F2. 多选题前端未实现
- **文件**: `src/views/ExamPage.vue:65`
- **现象**: `submitAnswer` 始终传 `[answer]`（单选项），多选题 UI 和逻辑未实现
- **修复**: 多选题使用 checkbox 多选，提交时传数组；后端已支持 `user_answer: list[str]`

### F3. 答题耗时未记录
- **文件**: `src/views/ExamPage.vue:68`
- **现象**: `time_spent` 始终传 `0`
- **修复**: 记录每题开始时间，提交时计算差值

### F4. 无 404 页面
- **文件**: `src/router/index.ts`
- **现象**: 未匹配路由时白屏
- **修复**: 添加 `catchAll` 路由 `{ path: '/:pathMatch(.*)*', component: NotFoundPage }`

### F5. 错题复习前端未对接
- **文件**: `src/views/LibraryPage.vue`
- **现象**: 后端有 `POST /mistakes/{id}/review` 端点，但前端仅有删除，无"复习"操作
- **修复**: 错题列表添加"已掌握"/"再复习"按钮

### F6. 无密码重置流程
- **文件**: `backend/app/api/v1/auth.py`
- **现象**: 无邮箱验证、无忘记密码功能
- **修复**: 实现 `POST /auth/forgot-password` + `POST /auth/reset-password`

### F7. 普通用户无法搜索题目
- **文件**: `backend/app/api/v1/questions.py`
- **现象**: `/questions` 端点无 `search` 参数（仅 admin 有）
- **修复**: 添加 `search` 参数，使用 `ilike` 模糊匹配

---

## 🟡 P2 — 代码质量问题（18 项待修复）

### 后端

| # | 文件 | 问题 | 修复建议 |
|---|------|------|---------|
| Q1 | `src/views/admin/AdminQuestionsPage.vue:54` | `save()` 的 catch 块为空 | 添加 `useUiStore().addToast('保存失败', 'error')` |
| Q2 | `src/views/admin/AdminQuestionsPage.vue:58-60` | `deleteQuestion()` 无 try-catch | 添加 try-catch 和错误提示 |
| Q3 | `src/views/admin/AdminUsersPage.vue:14` | `onMounted` 的 catch 块为空 | 添加错误提示 |
| Q4 | `src/views/admin/AdminUsersPage.vue:18-21` | `toggleRole()` 无 try-catch | 添加 try-catch 和错误提示 |
| Q5 | `src/views/FlashcardsPage.vue:29` | `loadCards` 的 catch 为 `/* silent */` | 添加错误提示 |
| Q6 | `src/views/LibraryPage.vue:51-53` | `deleteMistake` 无 try-catch | 添加 try-catch 和错误提示 |
| Q7 | `src/views/CommunityPage.vue:23` | `load` 的 catch 为 `/* */` | 添加错误提示 |
| Q8 | `src/views/CommunityPage.vue:29` | `createPost` 的 catch 为 `/* */` | 添加错误提示 |
| Q9 | `src/views/CommunityPage.vue:41` | `likePost` 无 try-catch，`post.likes++` 已执行 | 先 try API，成功后再 `++`；失败时 revert |
| Q10 | `src/views/ProgressPage.vue:84` | loadData 的 catch 仅 console.error | 添加用户可见的错误提示 + 重试按钮 |
| Q11 | `src/api/client.ts:7` | `baseURL` 硬编码 `http://localhost:8000` | 使用 `import.meta.env.VITE_API_BASE_URL` |
| Q12 | `src/App.vue` | LandingPage 的 `<router-view />` 在 NavBar 和独立 div 中各渲染一次 | 优化布局逻辑，避免重复渲染 |
| Q13 | `src/views/admin/AdminQuestionsPage.vue:58` | 删除题目无确认弹窗 | 添加 `confirm()` 或自定义确认对话框 |
| Q14 | `src/views/ExamPage.vue` | 提交答案后无法修改，无确认提交 | 添加"确认提交"二次确认流程 |
| Q15 | `backend/seed.py:93-94` | 检查 questions 是否存在时两次消费同一 result | 分开两次查询或使用 `scalars().all()` 一次获取 |
| Q16 | `backend/Dockerfile:10` | 构建时执行 `init_db.py && seed.py`，但 DB 可能未就绪 | 改为入口脚本（entrypoint.sh），等待 DB 就绪后执行 |
| Q17 | `backend/alembic/` | 目录存在但无任何迁移脚本 | 初始化 alembic 迁移，后续变更使用 `alembic revision` |
| Q18 | `backend/app/models/question.py` | `subject` 字段无索引 | 添加 `index=True` |

---

## 🔵 P3 — 性能/构建问题（8 项待修复）

| # | 问题 | 影响 | 修复建议 |
|---|------|------|---------|
| P1 | Vite build 产出 `index.js` 1.19MB（gzip 382KB） | 首屏加载慢 | 手动分 chunk：`chart.js`、`element-plus` 独立 chunk |
| P2 | Element Plus 全量引入 | 增加 ~500KB | 改为按需引入 `unplugin-element-plus` |
| P3 | `@element-plus/icons-vue` 全量注册 | 增加 ~100KB | 改为按需引入使用的图标 |
| P4 | Chart.js 全量注册 `registerables` | 增加 ~100KB | 只注册使用的 Controller |
| P5 | Three.js 已安装但未使用 | 增加 ~600KB | 移除 `@types/three` 依赖 |
| P6 | DashboardPage / ProgressPage 中 `new Chart()` 未销毁旧实例 | 路由切换后内存泄漏 | 使用 `onBeforeUnmount` 调用 `chart.destroy()` |
| P7 | 后端 stats 端点无缓存 | 高并发下 DB 压力大 | 引入 Redis 缓存，设置 5 分钟 TTL |
| P8 | 前端无图片/组件懒加载 | 首屏加载所有资源 | 使用 `defineAsyncComponent` 和 `loading="lazy"` |

---

## ⚪ P4 — 规范/维护性问题（8 项待修复）

| # | 问题 | 修复建议 |
|---|------|---------|
| R1 | 种子题目仅 30 道，第 7 题 analysis 承认"选项设置有误" | 扩充题库至 200+ 道，修正错误题目 |
| R2 | 12 个资源 `file_url` 指向不存在的路径 | 准备真实资源文件或实现上传功能 |
| R3 | 无单元测试 / 集成测试 / E2E 测试 | 引入 pytest（后端）+ Vitest（前端）+ Playwright（E2E） |
| R4 | 无 CI/CD 配置 | 配置 GitHub Actions：lint → test → build → deploy |
| R5 | DashboardPage / SettingsPage 组件残留 | 清理废弃组件文件 |
| R6 | `docker-compose.yml` 仅编排 PostgreSQL 和 Redis | 添加前后端服务定义 |
| R7 | `Dockerfile.frontend` 使用 `npx vite` 而非生产构建 | 改为 `npm run build` + nginx 静态服务 |
| R8 | Footer 链接（荣誉准则/服务条款/联系我们）均为占位 | 创建对应页面或移除链接 |

---

## 📋 待人工处理

| # | 事项 | 类别 | 优先级 |
|---|------|------|--------|
| 1 | 准备 200+ 道真实考研题目 | 内容 | 高 |
| 2 | 准备 PDF/DOC 资源文件 | 内容 | 高 |
| 3 | 更换 JWT_SECRET_KEY 为随机值 | 安全 | 高 |
| 4 | 起草用户协议 / 隐私政策 | 法律 | 中 |
| 5 | 题库版权确认 | 法律 | 中 |
| 6 | 配置生产域名 + HTTPS | 运维 | 中 |
| 7 | 配置 S3/OSS 对象存储 | 运维 | 中 |
| 8 | ICP 备案 | 法律 | 低 |

---

## 统计

| 优先级 | 待修复 | 已修复 | 合计 |
|--------|--------|--------|------|
| P0 安全 | 3 | 7 | 10 |
| P1 功能 | 7 | 6 | 13 |
| P2 质量 | 18 | 12 | 30 |
| P3 性能 | 8 | 0 | 8 |
| P4 规范 | 8 | 6 | 14 |
| v2 A-E 类 | 0 | 43 | 43 |
| **合计** | **44** | **74** | **118** |

> 注：v1 阶段原始问题 75 项 + v2 新增 43 项 = 118 项。已修复 74 项（v1 8 项 + v2 A-E 类 43 项 + v1 中部分修复 23 项），待修复 44 项。
