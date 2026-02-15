# Server Load Forecasting System

ML system for forecasting server load during sale events and planning infrastructure capacity.

## Features

- **Time Series Forecasting**: Predicts server load using historical traffic data with XGBoost model
- **Capacity Planning**: Calculates required server count based on forecasted load with safety buffers
- **Cost Estimation**: Estimates monthly infrastructure costs based on required server count
- **Interactive Dashboard**: Streamlit web interface for scenario planning
- **RESTful API**: FastAPI endpoints for programmatic access to forecasts
- **Peak Capacity Planning**: p95 percentile analysis for peak load handling

## Architecture

The system consists of three main components:

1. **Forecasting Engine** (`src/forecast.py`): Uses a pre-trained XGBoost model to predict traffic loads
2. **Capacity Planner** (`src/capacity.py`): Calculates required servers and costs based on forecasts
3. **Web Interface** (`src/app.py`): Streamlit dashboard for interactive scenario planning
4. **API Service** (`src/api.py`): FastAPI service for programmatic access to forecasts

## Prerequisites

- Python 3.12+
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

### Local Installation

Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -e .
```

### Containerized Installation

Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Usage

### Running Locally

#### Web Dashboard (Streamlit)
```bash
streamlit run src/app.py
```
The dashboard will be accessible at `http://localhost:8501`

#### API Service (FastAPI)
```bash
uvicorn src.api:app --reload
```
The API will be accessible at `http://localhost:8000`

#### API Endpoints
- `GET /` - Health check
- `GET /forecast/` - Get forecast with parameters:
  - `days` (int, default: 30): Forecast horizon in days (1-365)
  - `base_rps` (float, default: 150000.0): Current average RPS (1000-1000000)
  - `growth_rate` (float, default: 5.0): Monthly growth percentage (0-50)
- `GET /docs` - Interactive API documentation (Swagger UI)

Example API call:
```
http://localhost:8000/forecast/?days=30&base_rps=150000&growth_rate=5
```