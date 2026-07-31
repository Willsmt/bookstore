# Bookstore API

[![CI](https://github.com/Willsmt/bookstore/actions/workflows/ci.yml/badge.svg)](https://github.com/Willsmt/bookstore/actions/workflows/ci.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/willsmt/bookstore/badge)](https://www.codefactor.io/repository/github/willsmt/bookstore)

API REST para gerenciamento de catálogo, pedidos e estoque, construída com Django REST Framework. Projeto prático do curso EBAC Full Stack Python.

## Stack

- Python 3.14
- Django 6.0
- Django REST Framework 3.17
- PostgreSQL
- Poetry (gerenciamento de dependências)
- Docker + Docker Compose
- Ruff (lint + format)
- pytest + pytest-django + factory-boy (testes)
- GitHub Actions (CI: lint, testes, build da imagem)

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