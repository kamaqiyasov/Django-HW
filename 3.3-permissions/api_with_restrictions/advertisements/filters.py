from django_filters import DateFromToRangeFilter, rest_framework as filters
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()
    creator = filters.NumberFilter(field_name='creator__id')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    
    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'favorites']

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(favorites__creator=self.request.user)
        return queryset