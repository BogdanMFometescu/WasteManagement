import csv
from operator import itemgetter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RecordForm
from .models import Record
from .utils import search_waste, REPORTS_COLUMNS_VALUES, REPORTS_COLUMNS_HEADER, paginate_records
from .filters import FilterRecords


def records(request):
    all_records, search_query = search_waste(request)
    custom_range, all_records = paginate_records(request, all_records, 3)

    context = {'records': all_records, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'records/records.html', context)


def record(request, pk):
    one_record = Record.objects.get(id=pk)
    context = {'record': one_record}
    return render(request, 'records/single-record.html', context)


@login_required(login_url='login')
def create_record(request):
    profile = request.user.profile
    form = RecordForm()
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.owner = profile
            new_record.save()
            return redirect('records')

    context = {'form': form}
    return render(request, 'records/records-form.html', context)


@login_required(login_url='login')
def update_record(request, pk):
    profile = request.user.profile
    record_to_update = profile.record_set.get(id=pk)
    form = RecordForm(instance=record_to_update)
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES, instance=record_to_update)
        if form.is_valid():
            form.save()
            return redirect('records')

    context = {'form': form}
    return render(request, 'records/records-form.html', context)


@login_required(login_url='login')
def delete_record(request, pk):
    profile = request.user.profile
    record_to_delete = profile.record_set.get(id=pk)
    form = RecordForm(instance=record_to_delete)
    if request.method == 'POST':
        record_to_delete.delete()
        return redirect('records')

    context = {'object': form}
    return render(request, 'records/delete-record.html', context)


@login_required(login_url='login')
def get_reports(request):
    summaries = Record.get_total_quantities()
    summaries_of_records = Record.get_all_records()
    all_records = Record.objects.all()
    my_filter = FilterRecords(request.GET, queryset=all_records)
    all_records = my_filter.qs


    context = {
        'summaries': summaries,
        'summaries_of_records': summaries_of_records,
        'my_filter':my_filter,
        'all_records':all_records

    }

    return render(request, 'records/reports.html', context)


@login_required(login_url='login')
def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename =report.csv'
    writer = csv.writer(response)
    writer.writerow(['Title: List of all waste records'])
    writer.writerow([])
    writer.writerow(REPORTS_COLUMNS_HEADER)
    all_records = Record.objects.all().values_list(*REPORTS_COLUMNS_VALUES)

    sorted_records = sorted(all_records, key=itemgetter(0))

    for one_record in sorted_records:
        writer.writerow(one_record)

    return response


@login_required(login_url='login')
def export_to_csv_view(request):
    return render(request, 'records/export-to-csv.html')


