import django_filters
from .models import Kitten


class KittenFilter(django_filters.FilterSet):
    breed = django_filters.CharFilter(field_name="breed__name", lookup_expr="icontains")

    class Meta:
        model = Kitten
        fields = ["breed"]

