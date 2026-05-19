# LexiconPrep 考研备考平台 - 技术设计文档

---

## 目录

1. [项目概述](#1-项目概述)
   - 1.1 项目背景
   - 1.2 项目目标
   - 1.3 项目范围

2. [技术栈选型](#2-技术栈选型)
   - 2.1 前端技术栈
   - 2.2 后端技术栈
   - 2.3 数据库选择
   - 2.4 开发工具与环境配置

3. [系统架构设计](#3-系统架构设计)
   - 3.1 整体架构图
   - 3.2 核心模块划分
   - 3.3 模块间交互流程

4. [数据库设计](#4-数据库设计)
   - 4.1 ER图
   - 4.2 主要数据表结构

5. [API接口设计](#5-api接口设计)
   - 5.1 RESTful API规范
   - 5.2 主要接口定义

6. [前端UI/UX设计](#6-前端uiux设计)
   - 6.1 页面布局
   - 6.2 主要组件设计
   - 6.3 交互流程

7. [安全策略](#7-安全策略)
   - 7.1 认证授权机制
   - 7.2 数据加密方案
   - 7.3 防攻击措施

8. [部署方案](#8-部署方案)
   - 8.1 环境配置
   - 8.2 部署流程

9. [项目进度计划](#9-项目进度计划)
   - 9.1 里程碑规划
   - 9.2 时间线

10. [风险评估与应对策略](#10-风险评估与应对策略)

---

## 1. 项目概述

### 1.1 项目背景

**LexiconPrep** 是一款专为考研学子打造的高端学情管理与备考平台。针对考研备考周期长、压力大、知识点细碎的痛点，通过科学的数据可视化与沉浸式的交互设计，帮助用户建立秩序感，缓解备考焦虑，提升复习效率。

### 1.2 项目目标

| 目标类型 | 描述 |
|---------|------|
| **用户体验** | 提供极简、清爽的学习界面，减少视觉疲劳 |
| **功能目标** | 实现智能题库、错题本、闪卡复习、真题模拟等核心功能 |
| **数据目标** | 通过数据分析提供学情洞察和学习建议 |
| **性能目标** | 首屏加载时间 < 2s，交互响应 < 500ms |

### 1.3 项目范围

**核心功能模块：**
- 智能仪表盘（Dashboard）
- 资源库与搜索（Library）
- 专注做题模式（Exam Simulator）
- 错题本管理（Mistake Bank）
- 闪卡复习（Flashcards）
- 学习进度追踪（Progress）
- 学友社区（Community）

**非功能范围：**
- 暂不支持实时视频课程
- 暂不支持在线支付功能

---

## 2. 技术栈选型

### 2.1 前端技术栈

| 分类 | 技术 | 版本 | 选型理由 |
|------|------|------|----------|
| 框架 | Vue.js | 3.x | 响应式设计、组合式API、性能优异 |
| UI框架 | Element Plus | 2.x | 丰富组件库、完善的设计系统 |
| 状态管理 | Pinia | 2.x | Vue官方推荐、轻量级、类型安全 |
| 路由 | Vue Router | 4.x | Vue官方路由、支持动态路由 |
| 图表库 | Chart.js | 4.x | 轻量级、响应式、丰富的图表类型 |
| 样式 | Tailwind CSS | 3.x | 原子化CSS、快速开发、设计系统友好 |
| 图标 | Material Icons | - | Google官方图标库、丰富多样 |

### 2.2 后端技术栈

| 分类 | 技术 | 版本 | 选型理由 |
|------|------|------|----------|
| 语言 | Python | 3.11+ | 简洁语法、丰富的数据处理库、AI友好 |
| 框架 | FastAPI | 0.100+ | 高性能、自动API文档、类型安全 |
| ORM | SQLAlchemy | 2.x | 强大的ORM工具、支持多种数据库 |
| 异步支持 | Asyncio | - | Python原生异步支持 |
| API文档 | Swagger UI | - | 自动生成交互式API文档 |

### 2.3 数据库选择

| 数据库类型 | 技术 | 版本 | 用途 |
|-----------|------|------|------|
| 主数据库 | PostgreSQL | 16.x | 关系型数据存储、ACID事务支持 |
| 缓存 | Redis | 7.x | 会话管理、热点数据缓存 |
| 全文搜索 | PostgreSQL + pg_trgm | - | 知识点、题目搜索 |

### 2.4 开发工具与环境配置

| 工具 | 用途 |
|------|------|
| Docker | 容器化部署、环境一致性 |
| Docker Compose | 多容器编排 |
| Git | 版本控制 |
| GitHub Actions | CI/CD自动化 |
| Prettier | 代码格式化 |
| ESLint | 代码质量检查 |
| Pytest | 后端单元测试 |
| Vitest | 前端单元测试 |

---

## 3. 系统架构设计

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        前端层 (Frontend)                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────┐  │
│  │  Dashboard   │ │   Library    │ │  Exam        │ │  Community│  │
│  │   仪表盘     │ │    资源库    │ │  Simulator   │ │   社区    │  │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └─────┬─────┘  │
│         │                │                │                │        │
└─────────┼────────────────┼────────────────┼────────────────┼────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        API网关层 (API Gateway)                      │
│                  CORS处理 | 认证校验 | 请求限流                      │
└────────────────────────────────────────┬────────────────────────────┘
                                         │
          ┌──────────────────────────────┼──────────────────────────────┐
          │                              │                              │
          ▼                              ▼                              ▼
┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│    用户服务       │      │    学习服务       │      │    内容服务       │
│  User Service     │      │  Learning Service │      │  Content Service  │
│  - 用户认证       │      │  - 题库管理       │      │  - 资源管理       │
│  - 个人信息       │      │  - 错题本         │      │  - 闪卡系统       │
│  - 学习计划       │      │  - 进度追踪       │      │  - 真题下载       │
└───────────────────┘      └───────────────────┘      └───────────────────┘
          │                              │                              │
          └──────────────────────────────┼──────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        数据层 (Data Layer)                          │
│  ┌───────────────────┐    ┌───────────────────┐    ┌─────────────┐   │
│  │   PostgreSQL      │    │      Redis        │    │   File      │   │
│  │  (关系型数据)     │    │   (缓存/会话)     │    │  Storage    │   │
│  └───────────────────┘    └───────────────────┘    └─────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 核心模块划分

| 模块名称 | 职责描述 | 核心功能 |
|---------|---------|----------|
| **用户服务** | 用户认证与管理 | 注册、登录、个人信息、学习计划 |
| **学习服务** | 学习行为管理 | 题库、错题本、进度追踪、数据分析 |
| **内容服务** | 学习资源管理 | 资源库、闪卡系统、真题下载 |
| **社区服务** | 社交功能 | 学友动态、学习小组 |

### 3.3 模块间交互流程

#### 用户登录流程
```
用户 → 前端 → API网关 → 用户服务 → PostgreSQL → 返回用户信息 → 前端
```

#### 做题流程
```
用户 → 前端(Exam Simulator) → API网关 → 学习服务 → PostgreSQL(题目) → 返回题目 → 前端
用户答题 → 提交答案 → 学习服务 → PostgreSQL(记录答题) → 返回结果 → 前端
```

---

## 4. 数据库设计

### 4.1 ER图

```
┌───────────┐     1:N     ┌───────────┐     N:M     ┌───────────┐
│   User    │◄───────────│  Question │───────────►│   Tag     │
├───────────┤             ├───────────┤             ├───────────┤
│ id        │             │ id        │             │ id        │
│ email     │             │ content   │             │ name      │
│ password  │             │ options   │             └───────────┘
│ nickname  │             │ answer    │
│ avatar    │             │ difficulty│     N:M     ┌───────────┐
└───────────┘             │ tag_ids   │◄───────────│   Exam    │
       │                  └───────────┘             ├───────────┤
       │                                           │ id        │
       │ 1:N                                       │ name      │
       ▼                                           │ duration  │
┌───────────┐     1:N     ┌───────────┐             │ question_ids│
│ StudyLog  │◄───────────│ Mistake   │             └───────────┘
├───────────┤             ├───────────┤
│ id        │             │ id        │
│ user_id   │             │ user_id   │
│ question_id│            │ question_id│
│ answer    │             │ wrong_count│
│ is_correct│            │ last_review│
│ timestamp │            └───────────┘
└───────────┘
```

### 4.2 主要数据表结构

#### 4.2.1 users 表（用户表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 用户唯一标识 |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 邮箱 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| nickname | VARCHAR(50) | NOT NULL | 昵称 |
| avatar | VARCHAR(255) | NULL | 头像URL |
| streak_days | INT | DEFAULT 0 | 连续学习天数 |
| total_knowledge_points | INT | DEFAULT 0 | 已掌握知识点数 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新时间 |

#### 4.2.2 questions 表（题目表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 题目唯一标识 |
| type | VARCHAR(20) | NOT NULL | 题型(SINGLE/MULTIPLE/JUDGE) |
| content | TEXT | NOT NULL | 题目内容 |
| options | JSONB | NOT NULL | 选项(JSON数组) |
| answer | JSONB | NOT NULL | 正确答案(JSON数组) |
| analysis | TEXT | NULL | 答案解析 |
| difficulty | INT | DEFAULT 1 | 难度(1-5) |
| subject | VARCHAR(50) | NOT NULL | 学科分类 |
| chapter | VARCHAR(100) | NULL | 章节 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 4.2.3 study_logs 表（学习记录表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 记录唯一标识 |
| user_id | UUID | FOREIGN KEY | 用户ID |
| question_id | UUID | FOREIGN KEY | 题目ID |
| user_answer | JSONB | NOT NULL | 用户答案 |
| is_correct | BOOLEAN | NOT NULL | 是否正确 |
| time_spent | INT | DEFAULT 0 | 答题耗时(秒) |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 答题时间 |

#### 4.2.4 mistakes 表（错题本表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 记录唯一标识 |
| user_id | UUID | FOREIGN KEY | 用户ID |
| question_id | UUID | FOREIGN KEY | 题目ID |
| wrong_count | INT | DEFAULT 1 | 错误次数 |
| last_review_at | TIMESTAMP | NULL | 最后复习时间 |
| next_review_at | TIMESTAMP | NOT NULL | 下次复习时间 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 4.2.5 flashcards 表（闪卡表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 闪卡唯一标识 |
| user_id | UUID | FOREIGN KEY | 用户ID |
| front | TEXT | NOT NULL | 正面内容 |
| back | TEXT | NOT NULL | 背面内容 |
| subject | VARCHAR(50) | NULL | 学科分类 |
| difficulty | INT | DEFAULT 1 | 难度(1-5) |
| review_count | INT | DEFAULT 0 | 复习次数 |
| next_review_at | TIMESTAMP | NOT NULL | 下次复习时间 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 4.2.6 resources 表（资源表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 资源唯一标识 |
| title | VARCHAR(255) | NOT NULL | 资源标题 |
| description | TEXT | NULL | 资源描述 |
| type | VARCHAR(20) | NOT NULL | 资源类型(PDF/VIDEO/DOC) |
| file_url | VARCHAR(500) | NOT NULL | 文件URL |
| size | BIGINT | NOT NULL | 文件大小(字节) |
| subject | VARCHAR(50) | NOT NULL | 学科分类 |
| year | INT | NULL | 年份 |
| downloads | INT | DEFAULT 0 | 下载次数 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

---

## 5. API接口设计

### 5.1 RESTful API规范

| 规范项 | 规则 |
|--------|------|
| 基础路径 | `/api/v1` |
| 版本控制 | URI中包含版本号 |
| HTTP方法 | GET(查询)、POST(创建)、PUT(更新)、DELETE(删除) |
| 状态码 | 200(成功)、201(创建)、400(请求错误)、401(未授权)、403(禁止)、404(未找到)、500(服务器错误) |
| 响应格式 | JSON格式 |
| 错误处理 | 统一错误响应格式 |

### 5.2 主要接口定义

#### 5.2.1 用户认证接口

| API路径 | HTTP方法 | 功能描述 |
|---------|---------|----------|
| `/api/v1/auth/register` | POST | 用户注册 |
| `/api/v1/auth/login` | POST | 用户登录 |
| `/api/v1/auth/logout` | POST | 用户登出 |
| `/api/v1/auth/refresh` | POST | 刷新Token |

**POST /api/v1/auth/register**

请求体：
```json
{
  "email": "string",
  "password": "string",
  "nickname": "string"
}
```

响应体：
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "email": "string",
    "nickname": "string",
    "access_token": "string",
    "refresh_token": "string"
  }
}
```

#### 5.2.2 用户信息接口

| API路径 | HTTP方法 | 功能描述 |
|---------|---------|----------|
| `/api/v1/users/me` | GET | 获取当前用户信息 |
| `/api/v1/users/me` | PUT | 更新用户信息 |
| `/api/v1/users/me/stats` | GET | 获取用户学习统计 |

#### 5.2.3 题目接口

| API路径 | HTTP方法 | 功能描述 |
|---------|---------|----------|
| `/api/v1/questions` | GET | 获取题目列表 |
| `/api/v1/questions/{id}` | GET | 获取单题详情 |
| `/api/v1/questions/{id}/answer` | POST | 提交答案 |

**GET /api/v1/questions**

请求参数：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| subject | string | 否 | 学科筛选 |
| difficulty | int | 否 | 难度筛选 |
| limit | int | 否 | 每页数量 |
| offset | int | 否 | 偏移量 |

**POST /api/v1/questions/{id}/answer**

请求体：
```json
{
  "user_answer": ["选项A", "选项B"],
  "time_spent": 45
}
```

响应体：
```json
{
  "status": "success",
  "data": {
    "is_correct": true,
    "correct_answer": ["选项A", "选项B"],
    "analysis": "答案解析..."
  }
}
```

#### 5.2.4 错题本接口

| API路径 | HTTP方法 | 功能描述 |
|---------|---------|----------|
| `/api/v1/mistakes` | GET | 获取错题列表 |
| `/api/v1/mistakes/{id}` | DELETE | 删除错题记录 |
| `/api/v1/mistakes/review` | POST | 复习错题 |

#### 5.2.5 闪卡接口

| API路径 | HTTP方法 | 功能描述 |
|---------|---------|----------|
| `/api/v1/flashcards` | GET | 获取闪卡列表 |
| `/api/v1/flashcards` | POST | 创建闪卡 |
| `/api/v1/flashcards/{id}` | PUT | 更新闪卡 |
| `/api/v1/flashcards/{id}` | DELETE | 删除闪卡 |
| `/api/v1/flashcards/review` | POST | 复习闪卡 |

#### 5.2.6 资源接口

| API路径 | HTTP方法 | 功能描述 |
|---------|---------|----------|
| `/api/v1/resources` | GET | 获取资源列表 |
| `/api/v1/resources/{id}` | GET | 获取资源详情 |
| `/api/v1/resources/{id}/download` | GET | 下载资源 |

#### 5.2.7 学习统计接口

| API路径 | HTTP方法 | 功能描述 |
|---------|---------|----------|
| `/api/v1/stats/overview` | GET | 获取学习概览统计 |
| `/api/v1/stats/progress` | GET | 获取学习进度 |
| `/api/v1/stats/trend` | GET | 获取学习趋势 |

---

## 6. 前端UI/UX设计

### 6.1 页面布局

#### 6.1.1 首页（index.html）

```
┌─────────────────────────────────────────────────────────────┐
│                    Top Navigation Bar                       │
│  [Logo]  [Question Bank] [Flashcards] [Mock Tests] [Login] │
├─────────────────────────────────────────────────────────────┤
│                        Hero Section                         │
│         [搜索框]                                            │
│         专注、极简、高效的考研备考新体验                      │
├─────────────────────────────────────────────────────────────┤
│                   Bento Grid - 专业导览                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   计算机    │ │    法学     │ │   经济学    │          │
│  │    科学     │ │    硕士     │ │             │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│  ┌─────────────────────────────┐ ┌─────────────┐          │
│  │      心理学专硕 (MAP)       │ │             │          │
│  └─────────────────────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                  Features Section                           │
│  自适应题库 · 悬浮番茄钟 · 智能复习算法                        │
├─────────────────────────────────────────────────────────────┤
│                         Footer                              │
│  [LexiconPrep] [Honor Code] [Terms] [Contact]              │
└─────────────────────────────────────────────────────────────┘
```

#### 6.1.2 仪表盘（dashboard.html）

```
┌─────────────────────────────────────────────────────────────┐
│  ┌───────────────┐ ┌─────────────────────────────────────┐  │
│  │    Sidebar    │ │           Main Content              │  │
│  │  [Dashboard]  │ │  ┌───────────────────────────────┐  │  │
│  │  [Library]    │ │  │         KPI Cards              │  │  │
│  │  [Exam Sim]   │ │  │  连续学习 已掌握知识点 专注时长  │  │  │
│  │  [Progress]   │ │  └───────────────────────────────┘  │  │
│  │  [Settings]   │ │  ┌───────────────────┐ ┌─────────┐  │  │
│  │               │ │  │  学习进度轨迹图   │ │ 能力图谱│  │  │
│  │  [Start Quiz] │ │  │    (折线图)       │ │ (雷达图)│  │  │
│  └───────────────┘ │  └───────────────────┘ └─────────┘  │  │
│                    │  ┌───────────┐ ┌─────────────────┐   │  │
│                    │  │ 错题本洞察 │ │   资源快捷入口    │   │  │
│                    │  └───────────┘ └─────────────────┘   │  │
│                    └─────────────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Side Panel (每日打卡 / 学习计划)             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### 6.1.3 专注做题模式（exam.html）

```
┌─────────────────────────────────────────────────────────────┐
│  [← 退出]                  专注做题模式                  [提交] │
│                              [计时器]                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐ ┌───────────────┐  │
│  │          Question Canvas            │ │   Answer      │  │
│  │  [题目内容]                         │ │   Sheet       │  │
│  │  ○ 选项A                           │ │               │  │
│  │  ○ 选项B                           │ │  [1][2][3][4] │  │
│  │  ○ 选项C                           │ │  [5][6][7][8] │  │
│  │  ○ 选项D                           │ │  ...          │  │
│  │                                    │ │               │  │
│  │         [上一题] [下一题]           │ │  [已答/未答]  │  │
│  └─────────────────────────────────────┘ └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 主要组件设计

#### 6.2.1 Glass Panel（毛玻璃卡片）

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
}
```

#### 6.2.2 Progress Ring（进度环）

- 用途：展示学习进度、完成率
- 实现：SVG + CSS动画

#### 6.2.3 KPI Card（关键指标卡片）

| 属性 | 说明 |
|------|------|
| icon | Material Icons图标 |
| label | 指标名称 |
| value | 指标数值 |
| unit | 单位 |
| trend | 趋势(上升/下降/平稳) |

#### 6.2.4 Question Card（题目卡片）

| 属性 | 说明 |
|------|------|
| type | 题型标识(单选/多选/判断) |
| content | 题目内容 |
| options | 选项列表 |
| selected | 已选答案 |
| status | 状态(未答/已答/正确/错误) |

### 6.3 交互流程

#### 6.3.1 登录流程

```
用户访问首页 → 点击登录按钮 → 输入邮箱密码 → 提交登录请求 → 
验证成功 → 跳转仪表盘 → 加载用户数据
```

#### 6.3.2 做题流程

```
用户进入做题模式 → 加载题目 → 选择答案 → 点击下一题 → 
完成所有题目 → 点击提交 → 显示成绩 → 查看解析
```

#### 6.3.3 打卡流程

```
用户进入仪表盘 → 点击打卡按钮 → 显示动画效果 → 
更新连续打卡天数 → 显示鼓励文案
```

---

## 7. 安全策略

### 7.1 认证授权机制

#### 7.1.1 JWT认证

- Access Token：短期令牌，有效期15分钟
- Refresh Token：长期令牌，有效期7天，存储在HttpOnly Cookie中

#### 7.1.2 权限控制

| 用户角色 | 权限说明 |
|---------|----------|
| 普通用户 | 访问个人数据、题库、错题本、闪卡 |
| 管理员 | 管理题目、资源、用户数据 |

### 7.2 数据加密方案

| 数据类型 | 加密方式 |
|---------|----------|
| 用户密码 | bcrypt(强度12) |
| JWT Token | HS256算法 |
| 传输数据 | HTTPS/TLS 1.3 |

### 7.3 防攻击措施

| 攻击类型 | 防护措施 |
|---------|----------|
| SQL注入 | 使用ORM参数化查询 |
| XSS攻击 | 前端输入过滤、后端输出转义 |
| CSRF攻击 | 使用CSRF Token |
| 暴力破解 | 登录失败锁定、验证码 |
| 接口限流 | Rate Limiting(每分钟最多100次请求) |

---

## 8. 部署方案

### 8.1 环境配置

#### 8.1.1 开发环境

```yaml
# docker-compose.dev.yml
services:
  web:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/lexiconprep
      - REDIS_URL=redis://redis:6379/0

  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=lexiconprep
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### 8.1.2 生产环境

- **服务器**: AWS EC2 / 阿里云ECS
- **负载均衡**: AWS ALB / Nginx
- **数据库**: AWS RDS PostgreSQL
- **缓存**: AWS ElastiCache Redis
- **存储**: AWS S3
- **CDN**: AWS CloudFront

### 8.2 部署流程

```
开发完成 → 代码提交 → GitHub Actions触发 → 
代码检查(ESLint/Pytest) → 构建Docker镜像 → 
推送至Docker Hub → 部署到生产环境 → 
健康检查 → 完成部署
```

---

## 9. 项目进度计划

### 9.1 里程碑规划

| 阶段 | 时间 | 目标 |
|------|------|------|
| **Phase 1** | 第1-2周 | 项目初始化、基础架构搭建 |
| **Phase 2** | 第3-4周 | 用户认证模块开发 |
| **Phase 3** | 第5-6周 | 题库系统开发 |
| **Phase 4** | 第7-8周 | 错题本、闪卡模块开发 |
| **Phase 5** | 第9-10周 | 仪表盘、数据分析开发 |
| **Phase 6** | 第11-12周 | 社区模块开发 |
| **Phase 7** | 第13-14周 | 测试与Bug修复 |
| **Phase 8** | 第15-16周 | 部署上线 |

### 9.2 时间线

```
Week 1-2: 需求分析 → 技术选型 → 架构设计 → 数据库设计
Week 3-4: 用户注册/登录 → JWT认证 → 权限控制
Week 5-6: 题目CRUD → 做题流程 → 答案提交
Week 7-8: 错题本管理 → 闪卡系统 → 记忆曲线算法
Week 9-10: 仪表盘页面 → Chart.js图表 → 学习统计
Week 11-12: 社区动态 → 学习小组 → 学友互动
Week 13-14: 单元测试 → 集成测试 → Bug修复
Week 15-16: Docker部署 → 性能优化 → 上线发布
```

---

## 10. 风险评估与应对策略

| 风险类型 | 风险描述 | 发生概率 | 影响程度 | 应对策略 |
|---------|---------|---------|---------|----------|
| **技术风险** | 前端性能问题 | 中 | 中 | 使用Vue3组合式API、懒加载、代码分割 |
| **技术风险** | 数据库性能瓶颈 | 中 | 高 | 索引优化、读写分离、Redis缓存 |
| **业务风险** | 用户留存率低 | 中 | 高 | 优化用户体验、增加社交功能、推送提醒 |
| **业务风险** | 题库内容不足 | 低 | 中 | 与高校合作、用户贡献机制 |
| **安全风险** | 数据泄露 | 低 | 高 | 数据加密、访问日志、定期安全审计 |
| **运营风险** | 服务器宕机 | 低 | 高 | 多可用区部署、自动故障转移 |

---

## 附录

### A. 颜色规范

| 颜色名称 | 色值 | 用途 |
|---------|------|------|
| Primary (科技蓝) | #0058bc | 主色调、交互元素 |
| Secondary (深灰) | #5f5e60 | 文字、次要元素 |
| Tertiary (成功绿) | #006b27 | 成功状态、正向反馈 |
| Error (错误红) | #ba1a1a | 错误状态、警告 |
| Background | #f9f9fb | 页面背景 |

### B. 字体规范

| 字体名称 | 用途 |
|---------|------|
| Manrope | 标题、Headline |
| Inter | 正文、Body |
| Geist | 标签、按钮文字 |

---

**文档版本**: v1.0  
**创建日期**: 2026-05-19  
**适用项目**: LexiconPrep 考研备考平台