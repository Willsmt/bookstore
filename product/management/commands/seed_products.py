from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from product.models import Product


class Command(BaseCommand):
    help = "Popula a tabela Product com dados fake para testar paginação"

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, default=500)

    def handle(self, *args, **options):
        fake = Faker("pt_BR")
        total = options["total"]

        products = [
            Product(
                title=fake.sentence(nb_words=3).rstrip("."),
                price=Decimal(
                    fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                ).quantize(Decimal("0.01")),
                stock=fake.random_int(min=0, max=200),
            )
            for _ in range(total)
        ]

        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f"{total} produtos criados."))
