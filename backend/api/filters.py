import django_filters as filters

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name="tags__slug", method='filter_tags')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter_tags(self, queryset, name, tags):
        return queryset.filter(tags__slug__in=tags.split(','))
