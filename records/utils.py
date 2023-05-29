from django.db.models import Q
from .models import Record, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

REPORTS_COLUMNS_VALUES = ['company', 'waste_code', 'waste_name', 'type_of_waste','generated_quantity',
                          'recycled_quantity', 'disposed_quantity',
                          'recycling_method', 'disposal_method', 'waste_company', 'created']

REPORTS_COLUMNS_HEADER = ['Company', 'Waste Code', 'Waste Name', 'Type', 'Generated', 'Recycled', 'Disposed',
                          'Recycling Method',
                          'Disposal Method', 'Waste Company', 'Created']


def search_waste(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(Q(name__icontains=search_query))
    records = Record.objects.filter(
        Q(waste_name__icontains=search_query) | Q(tags__in=tags))

    return records, search_query


def paginate_records(request, records, results):
    page = request.GET.get('page')
    paginator = Paginator(records, results)

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        records = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        records = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, records
