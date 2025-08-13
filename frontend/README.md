# MedBrief 前端界面

本项目是 MedBrief 应用的前端用户界面，使用 React 和 Vite 构建。它为用户提供了一个直观的操作平台，用于管理医学文献监控主题、查看数据分析结果，并生成和管理分析报告PPT。

## 功能模块

根据项目组件和设计，前端主要包含三大功能模块：

1.  **主题与设置 (`TopicSettings.tsx`)**
    -   管理（增、删、改、查）用于文献追踪的医学主题。
    -   为每个主题配置关键词、检测频率和通知方式。
    -   设置PPT生成的格式模板。

2.  **文献分析 (`LiteratureAnalysis.tsx`)**
    -   展示特定主题下最新的文献检索结果。
    -   通过图表 (`TrendChart.tsx`, `DistributionChart.tsx`) 将文献数据可视化，如趋势、来源分布等。
    -   提供文献列表的浏览和详情查看。

3.  **PPT生成与历史 (`PPTGeneration.tsx`)**
    -   触发后端服务，根据当前分析结果生成PPT报告。
    -   查看和下载历史生成的PPT文件。

## 技术栈

- **框架**: React 18
- **构建工具**: Vite
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **图表库**: Recharts
- **图标**: Lucide React
- **代码规范**: ESLint

## 本地开发

**1. 环境准备**

- 确保您已安装 [Node.js](https://nodejs.org/) (建议使用 LTS 版本) 和 npm。
- 克隆本仓库到您的本地机器。

**2. 安装依赖**

进入前端项目目录 (`frontend/`)，然后运行以下命令安装所有依赖项：

```bash
npm install
```

**3. 启动开发服务器**

安装完成后，运行以下命令来启动 Vite 开发服务器：

```bash
npm run dev
```

服务启动后，您可以在浏览器中打开 `http://localhost:5173` (或终端提示的其他端口) 来查看和调试页面。

## 可用脚本命令

在 `frontend/` 目录下，您可以使用以下 npm 脚本：

- `npm run dev`: 启动开发服务器，支持热更新。
- `npm run build`: 将项目打包构建为生产环境的静态文件，输出到 `dist` 目录。
- `npm run lint`: 使用 ESLint 检查代码规范。
- `npm run preview`: 在本地预览生产环境构建后的应用。