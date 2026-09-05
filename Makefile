pretty:
	isort twitchrewards/ tests/
	black twitchrewards/ tests/

setupdb:
	docker compose build
	docker compose up -d
	docker exec -it app alembic upgrade head

run:
	docker compose build app
	docker compose up -d app

clean:
	docker stop app db
	docker remove app db
	docker system prune -a
