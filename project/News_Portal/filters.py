from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, DateTimeFilter
from .models import *
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    postCategory = ModelMultipleChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория',
        # empty_label='все',
        conjoined=False

    )
    added_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'titel_name': ['icontains'],

            # 'postCategory': ['exact'],
        }


class PostFilter2(FilterSet):
    postCategory = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='все',
        # conjoined=False

    )
    added_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'titel_name': ['icontains'],

            'postCategory': ['exact'],
        }
