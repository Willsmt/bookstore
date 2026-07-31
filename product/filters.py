import django_filters

from product.models import Category, Product


class ProductFilterSet(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.filter(is_active=True).only("id", "name"),
    )

    class Meta:
        model = Product
        fields = ["categories"]
