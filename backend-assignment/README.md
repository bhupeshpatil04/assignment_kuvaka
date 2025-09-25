
# Lead Intent Scoring Service

FastAPI backend that scores leads using rules + AI reasoning.

## Setup (local)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# set OPENAI_API_KEY optionally
uvicorn app.main:app --reload --port 8000
```

## Run with Docker (recommended)
Build and run with Docker Compose:
```bash
docker-compose up --build
```
Or build + run directly:
```bash
docker build -t lead-scoring:latest .
docker run -p 8000:8000 --env-file .env lead-scoring:latest
```

## Run tests
```bash
make test
# or
pytest -q
```

## API Usage
- POST /offer
- POST /leads/upload
- POST /score
- GET /results
- GET /results/export

See assignment description for details.

