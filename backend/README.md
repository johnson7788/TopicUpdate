# MedBrief 后端服务

本项目是 MedBrief 应用的后端服务，基于 FastAPI 构建。它提供了一系列 API，用于分析医学文献数据、管理主题，并能根据分析结果自动生成 PowerPoint (PPT) 报告。

## 主要功能

- **自动生成PPT**: 根据指定的主题和时间范围，自动创建包含数据分析图表的 PPT 报告。
- **文献数据分析**:
    - **趋势分析**: 分析特定主题文献随时间发表的趋势。
    - **分布分析**: 分析文献在期刊、作者、机构等维度的分布情况。
    - **关键词云**: 基于文献摘要生成关键词词云。
- **RESTful API**: 提供用于管理文献和主题的标准化接口。

## 技术栈

- **语言**: Python 3
- **Web框架**: FastAPI
- **数据库**: SQLite + SQLAlchemy (ORM)
- **PPT处理**: `python-pptx`
- **数据分析**: `pandas`, `scikit-learn`
- **中文分词**: `jieba`
- **服务器**: `uvicorn`

## 项目设置与安装

**1. 环境准备**

- 确保您已安装 Python 3.8 或更高版本。
- 克隆本仓库到您的本地机器。

**2. 安装依赖**

进入后端项目目录 (`backend/`)，然后运行以下命令安装所有必需的库：

```bash
pip install -r requirements.txt
```

## 数据库初始化

**1. 自动创建库表**

应用在首次启动时会自动在 `backend/` 目录下创建一个名为 `medbrief.db` 的 SQLite 数据库文件，并自动创建所需的数据表。

**2. 填充初始数据**

为了让系统能够正常使用，您需要向数据库中填充初始的文献和主题数据。请运行以下脚本：

```bash
python insert_my_data.py
```

## 运行项目

完成安装和数据库初始化后，在 `backend/` 目录下运行以下命令来启动应用服务：

```bash
python main.py
```

服务启动后，您可以通过浏览器访问 `http://0.0.0.0:8000` 或 `http://localhost:8000`。

## API 文档

FastAPI 提供了自动化的交互式 API 文档。在服务运行后，您可以访问以下地址查看和测试所有 API：

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 运行测试

本项目使用 `pytest` 进行单元测试。要运行测试，请在 `backend/` 目录下执行：

```bash
pytest
```

## 工具脚本

项目中包含一些独立的实用工具脚本。

### `compare_ppts.py`

此脚本用于比较两个 PPT 文件的文本内容差异。这对于验证不同版本的 PPT 生成结果非常有用。

**使用方法**:

```bash
python compare_ppts.py <第一个PPT文件.pptx> <第二个PPT文件.pptx>
```
