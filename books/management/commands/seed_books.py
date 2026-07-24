from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from books.models import Book


class Command(BaseCommand):
    help = "Popula a tabela Book com dados fake para testar paginação"

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, default=500)

    def handle(self, *args, **options):
        fake = Faker("pt_BR")
        total = options["total"]

        with transaction.atomic():
            for _ in range(total):
                Book.objects.create(
                    title=fake.sentence(nb_words=3).rstrip("."),
                    price=Decimal(
                        fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                    ).quantize(Decimal("0.01")),
                    stock=fake.random_int(min=0, max=200),
                    author=fake.name(),
                    isbn=fake.unique.isbn13(separator=""),
                    published_at=fake.date_between(start_date="-30y", end_date="today"),
                )

        self.stdout.write(self.style.SUCCESS(f"{total} livros criados."))