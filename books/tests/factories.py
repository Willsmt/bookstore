import factory
from books.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=3)
    price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    stock = factory.Faker("pyint", min_value=0, max_value=50)
    is_active = True
    author = factory.Faker("name")
    isbn = factory.Sequence(lambda n: f"{9780000000000 + n}")
    published_at = factory.Faker("date_between", start_date="-30y", end_date="today")
