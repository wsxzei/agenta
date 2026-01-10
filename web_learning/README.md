# Agenta 前端学习项目

这是一个从零开始的学习项目，旨在帮助后端开发者逐步理解现代前端开发。

## 项目目标

通过模块化的方式，重建 Agenta 开源项目的前端部分，学习：
- Next.js 框架的使用
- TypeScript 类型系统
- 状态管理（Jotai + React Query）
- 组件化开发
- 现代前端工程化实践

## 技术栈

### 核心框架
- **Next.js 15**: React 框架，提供服务端渲染和路由功能
- **React 19**: UI 库
- **TypeScript 5.8**: 类型安全

### UI & 样式
- **Ant Design 6**: 企业级 UI 组件库
- **Tailwind CSS 3**: 原子化 CSS 框架

### 状态管理
- **Jotai 2**: 原子化状态管理
- **React Query (TanStack Query 5)**: 服务端状态管理

### 其他工具
- **Axios**: HTTP 请求库
- **Prettier**: 代码格式化

## 项目结构

```
web_learning/
├── src/
│   ├── components/    # 可复用组件
│   ├── hooks/         # 自定义 Hooks
│   ├── lib/           # 工具库和配置
│   ├── pages/         # 页面组件（使用 Pages Router）
│   ├── services/      # API 服务层
│   ├── state/         # 状态管理
│   └── styles/        # 全局样式
├── public/            # 静态资源
├── package.json       # 依赖配置
├── tsconfig.json      # TypeScript 配置
└── next.config.ts     # Next.js 配置
```

## 安装与运行

### 1. 安装依赖

```bash
npm install
# 或
pnpm install
# 或
yarn install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 `http://localhost:3000` 查看应用

### 3. 构建生产版本

```bash
npm run build
npm start
```

### 4. 代码检查与格式化

```bash
# 检查代码
npm run lint

# 自动修复
npm run lint-fix

# 格式化检查
npm run format

# 格式化修复
npm run format-fix

# 类型检查
npm run types:check
```

## 学习模块

项目按模块逐步实现，每个模块包含：
1. 代码实现
2. 详细的代码讲解
3. 关键概念说明
4. 与原项目的对比

### 已完成的模块

- **模块 1: 项目初始化与环境搭建** ✅

  - 创建基础配置文件
  - 搭建开发环境
  - 理解 Next.js 项目结构

## 学习建议

1. **按顺序学习**：每个模块都有依赖关系，建议按顺序完成
2. **动手实践**：不要只看代码，要亲自修改和运行
3. **理解原理**：重点是理解"为什么这样设计"，而不仅仅是"怎么做"
4. **对比原项目**：对照 `/web` 目录中的原项目代码，加深理解

## 与原项目的区别

为了教学目的，本项目进行了以下简化：
1. 移除了企业版（EE）相关的代码
2. 简化了一些复杂的配置
3. 精简了部分工具库和中间件
4. 使用更简洁的项目结构

核心的架构模式和编码风格保持一致。

## 常见问题

### Q: 为什么使用 Pages Router 而不是 App Router？
A: 原项目使用 Pages Router，为了保持一致性和便于对比，我们也使用相同的路由方式。

### Q: 什么是 Jotai？
A: Jotai 是一个原子化的状态管理库，比 Redux 更简洁。它将状态分解为独立的"原子"，组件可以只订阅需要的原子。

### Q: 为什么同时使用 Jotai 和 React Query？
A:
- **Jotai**: 管理客户端状态（UI 状态、用户输入等）
- **React Query**: 管理服务端状态（API 数据、缓存等）

两者配合使用，实现最佳的性能和开发体验。

## 参考资源

- [Next.js 官方文档](https://nextjs.org/docs)
- [React 官方文档](https://react.dev)
- [TypeScript 官方文档](https://www.typescriptlang.org/docs)
- [Jotai 官方文档](https://jotai.org)
- [Ant Design 文档](https://ant.design)
- [Tailwind CSS 文档](https://tailwindcss.com)

## 许可证

与主项目保持一致

