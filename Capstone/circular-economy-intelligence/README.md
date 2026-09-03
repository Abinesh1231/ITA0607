# Circular Economy Intelligence System

An end-to-end ML capstone for waste material identification, recyclability assessment,
recycling value estimation, recommendations, and dashboard analytics.

## Current implementation

- FastAPI backend
- React + Vite frontend
- SQLite database by default
- Transfer-learning image classifier scaffold using PyTorch
- Valuation engine using material rates and estimated weight
- Optional YOLO detection integration when a trained detector is available
- API tests and frontend service layer
- Docker and deployment configuration
- Dataset preparation and training scripts

## Dataset

The selected dataset contains 12 waste classes:

battery, biological, cardboard, clothes, green-glass, metal, paper, plastic,
shoes, trash, brown-glass, white-glass

Place the extracted dataset under:

`ml/data/raw/garbage_classification/`

The code supports either class-folder datasets directly or an explicit processed
train/val/test directory layout.

## Quick start

### Backend

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

Set `VITE_API_URL` if the backend is not at `http://127.0.0.1:8000`.

## ML

```bash
python scripts/setup.py
python -m ml.src.data.split
python -m ml.src.classification.train
python -m ml.src.classification.evaluate
```

The default classifier uses EfficientNet-B0 transfer learning. CPU training works,
but a CUDA-capable GPU is strongly recommended.

## Important

The provided classification dataset does not contain reliable market prices or
physical weights. Recycling value is therefore estimated from:

`estimated_weight_kg × reference_rate_per_kg × quality_factor`

For production/research validity, replace the sample rates with documented local
recycling-market data and use a real weight measurement when available.
