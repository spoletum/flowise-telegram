all:
	docker compose up -d
	poetry run python main.py