import django_filters
from .models import Record
from django_filters import DateFilter,CharFilter


class FilterRecords(django_filters.FilterSet):
    start_date = DateFilter(field_name='created', lookup_expr='gte')
    end_date = DateFilter(field_name='created', lookup_expr='lte')
    county_filter  = CharFilter(field_name='county', lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        super(FilterRecords, self).__init__(*args, **kwargs)
        self.filters['start_date'].label = 'Start Date '
        self.filters['end_date'].label = 'End Date '
        self.filters['company'].label = 'Company name'
        self.filters['county_filter'].label = 'County'

    class Meta:
        model = Record
        fields = ['company', 'waste_code']




