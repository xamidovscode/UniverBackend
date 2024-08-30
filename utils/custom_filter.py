from apps.common import models as common
import django_filters


class FloorFilter(django_filters.FilterSet):
    floor = django_filters.BooleanFilter(method="get_floors_or_rooms", label="Floors")

    class Meta:
        model = common.Floor
        fields = ['parent']

    @classmethod
    def get_floors_or_rooms(cls, queryset, name, value):
        if value:
            print(1111111111111111, value)
        return queryset

