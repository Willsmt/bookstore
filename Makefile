.PHONY: up down build logs shell migrate collectstatic seed

up: ## Sobe os serviços (builda se necessário)
	docker compose up --build

down: ## Derruba os serviços
	docker compose down

build: ## Rebuilda a imagem sem subir
	docker compose build

logs: ## Acompanha o log só do serviço web
	docker compose logs -f web

shell: ## Abre um shell dentro do container web
	docker compose exec web bash

migrate: ## Roda as migrations dentro do container
	docker compose exec web python manage.py migrate

collectstatic: ## Roda collectstatic dentro do container
	docker compose exec web python manage.py collectstatic --noinput

seed: ## Popula o banco com produtos de teste
	docker compose exec web python manage.py seed_products --total 500
