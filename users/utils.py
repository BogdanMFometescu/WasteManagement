from django.db.models import Q
from .models import Profile, Certificate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_profile(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    certificates = Certificate.objects.filter(name__icontains=search_query)
    all_profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(certificate__in=certificates))

    return all_profiles, search_query


def paginate_profiles(request, profiles, results):
    page_profile = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        records = paginator.page(page_profile)
    except PageNotAnInteger:
        page_profile = 1
        records = paginator.page(page_profile)
    except EmptyPage:
        page_profile = paginator.num_pages
        records = paginator.page(page_profile)

    left_index = (int(page_profile) - 4)

    if left_index < 1:
        left_index = 1

    right_index = (int(page_profile) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, records
