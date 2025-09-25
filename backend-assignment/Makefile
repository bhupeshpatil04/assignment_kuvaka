run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q

docker-build:
	docker build -t lead-scoring:latest .

docker-up:
	docker-compose up --build
