import django_filters
from gameofthrones.models import BiologicalType, CharacterAliase, CharacterFamilyTie, CharacterInfo, \
	CharacterTitle, Culture, House, RelationType


class CharacterFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(
        field_name='full_name',
        label='Character Name',
        lookup_expr='icontains'
    )

    culture = django_filters.ModelChoiceFilter(
        field_name = 'culture',
        label = 'Culture',
        queryset = Culture.objects.all().order_by('culture_name'),
        lookup_expr = 'exact'
    )

    house = django_filters.ModelChoiceFilter(
        field_name = 'house',
        label = 'House',
        queryset = House.objects.all().order_by('house_name'),
        lookup_expr = 'exact'
    )


    class Meta:
        model = CharacterInfo
        # form = SearchForm
        # fields [] is required, even if empty.
        fields = []