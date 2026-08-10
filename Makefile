.PHONY: install run test seed docker-up docker-down

install:
	python3 -m pip install -r requirements.txt

run:
	chmod +x ./start.sh && PORT=46999 bash ./start.sh

test:
	pytest tests/ -v --tb=short

seed:
	python3 seed.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down
