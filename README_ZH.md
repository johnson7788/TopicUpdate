# MedBrief: 简报专家，您的自动化医学文献追踪与分析助手

MedBrief 是一个全栈Web应用，旨在帮助医学研究者、临床医生和学生自动追踪特定医学主题的最新文献，进行数据可视化分析，并一键生成精美的 PowerPoint (PPT) 简报。

# 注意：
本项目只是一个模拟数据的项目，后端的数据依赖[insert_my_data.py](backend%2Finsert_my_data.py)进行模拟插入。

# 需求分析

在快节奏的医学领域，从业者需要持续关注其专业方向的最新研究进展。传统的人工检索、阅读、整理和汇报方式效率低下且耗时巨大。本项目旨在解决以下痛点：

- **信息过载**: 难以从海量文献中快速筛选出最相关、最有价值的内容。
- **效率低下**: 手动整理文献、分析趋势和制作报告PPT是一项重复性高、耗时长的劳动。
- **缺乏洞察**: 难以直观地发现研究趋势、核心期刊、活跃研究机构等深层信息。

# 核心功能

- **智能化主题管理**: 轻松创建和管理您感兴趣的医学主题，设定关键词和监控周期。
- **自动化数据分析**:
    - **趋势分析**: 自动分析特定主题文献随时间（如按季度、年度）的发表数量趋势。
    - **多维度分布**: 可视化展示文献在期刊、作者、国家/地区及研究机构等维度的分布情况。
- **一键生成PPT报告**: 根据最新的分析数据，自动生成结构清晰、图文并茂的PowerPoint报告，可直接用于学术汇报或内部交流。
- **友好的Web界面**: 提供直观的前端界面，方便用户进行主题设置、数据查看和报告下载。

# 技术栈

本项目采用前后端分离的现代Web架构。

- **后端 (Backend)**
    - **语言**: Python 3
    - **框架**: FastAPI
    - **数据库**: SQLite + SQLAlchemy ORM
    - **PPT生成**: `python-pptx`
    - **数据处理**: `pandas`, `scikit-learn`
    - **部署**: Docker, Uvicorn

- **前端 (Frontend)**
    - **语言**: TypeScript
    - **框架**: React 18
    - **构建工具**: Vite
    - **UI/样式**: Tailwind CSS
    - **图表**: Recharts
    - **部署**: Docker, Nginx

# 如何运行

我们强烈推荐使用 Docker 来运行本项目，因为它能为您处理好所有环境依赖和配置。

### 1. 使用 Docker (推荐)

**前提**: 请确保您的电脑上已经安装了 [Docker](https://www.docker.com/products/docker-desktop/) 和 Docker Compose。

**步骤**:

1.  克隆本仓库到您的本地：
    ```bash
    git clone https://github.com/johnson7788/TopicUpdate
    cd TopicUpdate
    ```

2.  在项目根目录下，执行以下命令来构建并启动所有服务：
    ```bash
    docker-compose up --build
    ```
    该命令会自动构建前端和后端的 Docker 镜像，并启动两个容器。

3.  **访问应用**:
    - **前端界面**: 打开浏览器访问 `http://localhost:9000`
    - **后端 API**: 后端服务运行在 `http://localhost:8000`

### 2. 本地手动运行 (适合开发者)

如果您希望在本地分别运行前端和后端服务进行开发。

#### 启动后端

```bash
# 1. 进入后端目录
cd backend/

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 初始化数据库并填充示例数据
python insert_my_data.py

# 4. 启动FastAPI服务
python main.py
# 服务将运行在 http://localhost:8000
```

#### 启动前端

```bash
# 1. 进入前端目录
cd frontend/

# 2. 安装npm依赖
npm install

# 3. 启动Vite开发服务器
npm run dev
# 服务将运行在 http://localhost:5173 (或终端提示的其他端口)
```
**注意**: 在手动运行前端时，请确保 `frontend/.env` 文件中的 `VITE_API_BASE_URL` 指向您的后端地址 (例如 `http://localhost:8000`)。

# API 文档

后端服务基于 FastAPI，自带强大的自动化API文档。在后端服务启动后，您可以访问以下地址进行查看和交互：

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

# 截图
![document_monitor.png](doc%2Fdocument_monitor.png)
![help.png](doc%2Fhelp.png)
![history.png](doc%2Fhistory.png)
![topic_setting.png](doc%2Ftopic_setting.png)

# 运行测试

本项目后端包含单元测试。要运行测试，请进入 `backend/` 目录并执行：

```bash
pytest
```

# 许可证

本项目基于 [MIT License](LICENSE) 开源。