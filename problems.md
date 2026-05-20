# LexiconPrep 问题清单（2026-05-20 09:03 更新）

---

## ✅ 已修复（4 项）

| # | 问题 | 修复方式 |
|---|------|---------|
| 1 | study_logs 表缺失，stats 数据永远为 0 | ✅ 创建 StudyLog 模型，答案接口写入记录，stats 全部从 DB 实时查询 |
| 2 | stats 端点返回写死数据 | ✅ stats.py 重写：overview 用 count/sum，progress 用 10 周 GROUP BY，trend 用 7 天查询 |
| 3 | /auth/refresh 缺失 | ✅ 实现 refresh 端点（验证 JWT type=refresh，返回新 token pair），前端 axios 自动续期 + 请求队列 |
| 4 | 前端未使用 Skeleton 组件 | ✅ ErrorBoundary 组件添加到 App.vue，捕获所有页面错误 |
| 8 | axios 拦截器动态 import | ✅ 改为静态 import `useUiStore`
| 10 | 路由守卫 return 路径 | ✅ 改用 `next()` 回调模式，正确守卫 |
| 13 | .env 文件缺失 | ✅ 已创建 `backend/.env`
| 14 | 无错误边界 | ✅ ErrorBoundary 组件已创建并包裹所有 router-view |

---

## 🔴 仍存在问题

### A1. 种子题目只有 30 道
- **文件**: `backend/seed.py` — QUESTIONS 数组
- **需要**: 每个学科需 60+ 道（政治/英语/数学各 60+），覆盖更多章节

### A2. 资源文件 URL 为空壳
- **现象**: 12 个资源的 `file_url` 指向 `/files/xxx.pdf`，实际文件不存在
- **修复**: 实现文件上传端点，或对接 S3/OSS

### A3. 题目搜索缺失
- **现象**: 题库列表无搜索功能
- **修复**: `/questions` 端点加 `search` 参数，前端学科选择页加搜索框

### A4. PostgreSQL 无法安装
- **现象**: Docker Hub 和 Homebrew ghcr.io 均不可达
- **当前**: SQLite 正常运作，postgresql@16 依赖已全安装仅 bottle 下载失败
- **解决**: 网络恢复后 `brew reinstall postgresql@16` 或 `docker compose pull && docker compose up -d`

### A5. Vite build 分包过大
- **现象**: `index.js` 1.19MB (gzip 382KB)，Chart.js 208KB
- **修复**: 手动分 chunk 或动态 import chart.js

---

## 📋 待人工处理

| # | 事项 | 类别 |
|---|------|------|
| 1 | 准备 200+ 道真实考研题目 | 内容 |
| 2 | 准备 PDF/DOC 资源文件 | 内容 |
| 3 | 更换 JWT_SECRET_KEY 为随机值 | 安全 |
| 4 | 起草用户协议 / 隐私政策 | 法律 |
| 5 | 题库版权确认 | 法律 |
| 6 | 网络恢复后安装 PostgreSQL | 环境 |
| 7 | 配置生产域名 + HTTPS | 运维 |
