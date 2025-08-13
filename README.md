# MedBrief: Briefing Expert, Your Automated Medical Literature Tracking and Analysis Assistant

MedBrief is a full-stack web application designed to help medical researchers, clinicians, and students automatically track the latest literature on specific medical topics, perform data visualization analysis, and generate beautiful PowerPoint (PPT) briefings with one click.

# Note:
This project is only a simulated data project. The backend data relies on [insert_my_data.py](backend%2Finsert_my_data.py) for simulated insertion.

# Requirements Analysis

In the fast-paced medical field, practitioners need to continuously follow the latest research advances in their professional directions. Traditional manual search, reading, organization, and reporting methods are inefficient and time-consuming. This project aims to solve the following pain points:

- **Information Overload**: Difficulty in quickly filtering out the most relevant and valuable content from massive literature.
- **Low Efficiency**: Manually organizing literature, analyzing trends, and creating report PPTs is highly repetitive and time-consuming work.
- **Lack of Insights**: Difficulty in intuitively discovering in-depth information such as research trends, core journals, and active research institutions.

# Core Features

- **Intelligent Topic Management**: Easily create and manage medical topics of interest, set keywords and monitoring cycles.
- **Automated Data Analysis**:
    - **Trend Analysis**: Automatically analyze the trend of publications on specific topics over time (e.g., by quarter, year).
    - **Multi-dimensional Distribution**: Visually display the distribution of literature across dimensions such as journals, authors, countries/regions, and research institutions.
- **One-click PPT Report Generation**: Automatically generate structured, illustrated PowerPoint reports based on the latest analysis data, which can be directly used for academic presentations or internal communication.
- **User-friendly Web Interface**: Provide an intuitive frontend interface for users to easily perform topic settings, data viewing, and report downloads.

# Technology Stack

This project adopts a modern web architecture with separated frontend and backend.

- **Backend**
    - **Language**: Python 3
    - **Framework**: FastAPI
    - **Database**: SQLite + SQLAlchemy ORM
    - **PPT Generation**: `python-pptx`
    - **Data Processing**: `pandas`, `scikit-learn`
    - **Deployment**: Docker, Uvicorn

- **Frontend**
    - **Language**: TypeScript
    - **Framework**: React 18
    - **Build Tool**: Vite
    - **UI/Style**: Tailwind CSS
    - **Charts**: Recharts
    - **Deployment**: Docker, Nginx

# How to Run

We strongly recommend using Docker to run this project, as it handles all environment dependencies and configurations for you.

### 1. Using Docker (Recommended)

**Prerequisites**: Please ensure that [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose are installed on your computer.

**Steps**:

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/johnson7788/TopicUpdate
    cd TopicUpdate
    ```

2. In the project root directory, execute the following command to build and start all services:
    ```bash
    docker-compose up --build
    ```
    This command will automatically build the Docker images for the frontend and backend and start two containers.

3. **Access the Application**:
    - **Frontend Interface**: Open your browser and visit `http://localhost:9000`
    - **Backend API**: The backend service is running at `http://localhost:8000`

### 2. Running Locally (for Developers)

If you want to run the frontend and backend services separately on your local machine for development.

#### Start Backend

```bash
# 1. Navigate to the backend directory
cd backend/

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Initialize the database and populate sample data
python insert_my_data.py

# 4. Start the FastAPI service
python main.py
# The service will be running at http://localhost:8000
```

#### Start Frontend

```bash
# 1. Navigate to the frontend directory
cd frontend/

# 2. Install npm dependencies
npm install

# 3. Start the Vite development server
npm run dev
# The service will be running at http://localhost:5173 (or another port indicated in the terminal)
```
**Note**: When running the frontend locally, ensure that `frontend/.env` file's `VITE_API_BASE_URL` points to your backend address (e.g., `http://localhost:8000`).

# API Documentation

The backend service is based on FastAPI and comes with powerful automated API documentation. After starting the backend service, you can access the following addresses to view and interact with it:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

# Screenshots
![document_monitor.png](doc%2Fdocument_monitor.png)
![help.png](doc%2Fhelp.png)
![history.png](doc%2Fhistory.png)
![topic_setting.png](doc%2Ftopic_setting.png)

# Running Tests

The backend of this project includes unit tests. To run the tests, navigate to the `backend/` directory and execute:

```bash
pytest
```

# wechat
![weichat.png](doc%2Fweichat.png)

# License

This project is open-source under the [MIT License](LICENSE).
