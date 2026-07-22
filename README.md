# Bookstore API

API REST para gerenciamento de livros, construída com Django REST Framework como projeto prático do módulo de configuração do DRF.

## Stack

- Python 3.14
- Django 6.0
- Django REST Framework 3.17
- Poetry (gerenciamento de dependências)
- Ruff (lint + format)
- pytest + pytest-django + factory-boy (testes)

## Setup

```bash
poetry install
cp .env.example .env  # preencha o SECRET_KEY
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

## Endpoints

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| GET | `/api/books/` | Lista todos os livros | Pública |
| POST | `/api/books/` | Cria um novo livro | Requerida |
| GET | `/api/books/{id}/` | Detalha um livro | Pública |
| PUT/PATCH | `/api/books/{id}/` | Atualiza um livro | Requerida |
| DELETE | `/api/books/{id}/` | Remove um livro | Requerida |

## Testes

```bash
poetry run pytest
```

## Lint / Format

```bash
poetry run ruff check .
poetry run ruff format .
```
