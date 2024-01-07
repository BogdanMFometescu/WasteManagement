from django.db import models
import uuid
from users.models import Profile
from django.db.models import Sum
from .constants import EWC_CHOICES, WASTE_TYPE_CHOICES, RECYCLING_METHOD_CHOICES, DISPOSAL_METHOD_CHOICES


class Record(models.Model):
    owner = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    company = models.CharField(blank=True, null=True, max_length=300)
    county = models.CharField(blank=True, null=True, max_length=300)
    waste_name = models.CharField(null=True, blank=True, max_length=400)
    waste_code = models.CharField(blank=True, null=True,
                                  choices=EWC_CHOICES)
    generator = models.CharField(null=True, blank=True, max_length=400)
    generated_quantity = models.IntegerField(default=0, blank=True, null=True)
    recycled_quantity = models.IntegerField(default=0, blank=True, null=True)
    disposed_quantity = models.IntegerField(default=0, blank=True, null=True)
    waste_company = models.CharField(null=True, blank=True, max_length=400)
    recycling_method = models.CharField(null=True, blank=True, choices=RECYCLING_METHOD_CHOICES)
    tags = models.ManyToManyField('Tag', blank=True)
    disposal_method = models.CharField(null=True, blank=True, choices=DISPOSAL_METHOD_CHOICES)
    type_of_waste = models.CharField(null=True, blank=True, choices=WASTE_TYPE_CHOICES)
    picture = models.ImageField(blank=True, null=True)
    evidence = models.FileField(blank=True,null=True)
    waste_description = models.TextField(blank=True, null=True, max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        if self.waste_code:
            self.waste_name = dict(self._meta.get_field('waste_code').choices).get(self.waste_code)
        super().save(*args, **kwargs)

    @staticmethod
    def get_company_names(waste_code):
        companies_query = Record.objects.filter(waste_code=waste_code).values_list('company', flat=True).distinct()
        company_names = ', '.join(companies_query)
        return company_names

    @classmethod
    def get_total_quantities(cls):
        unique_waste_codes = cls.objects.values('waste_code').distinct()
        summaries = []

        for waste_code in unique_waste_codes:
            waste_code = waste_code['waste_code']

            companies_query = cls.objects.filter(waste_code=waste_code).values_list('company', flat=True).distinct()

            for company_name in companies_query:
                total_generated_quantity = \
                    cls.objects.filter(waste_code=waste_code, company=company_name).aggregate(
                        Sum('generated_quantity'))[
                        'generated_quantity__sum'] or 0
                total_recycled_quantity = \
                    cls.objects.filter(waste_code=waste_code, company=company_name).aggregate(Sum('recycled_quantity'))[
                        'recycled_quantity__sum'] or 0
                total_disposed_quantity = \
                    cls.objects.filter(waste_code=waste_code, company=company_name).aggregate(Sum('disposed_quantity'))[
                        'disposed_quantity__sum'] or 0

                stock_quantity = total_generated_quantity - (total_recycled_quantity + total_disposed_quantity)
                if stock_quantity < 0:
                    stock_quantity = 0

                summaries.append({
                    'waste_code': waste_code,
                    'total_generated_quantity': total_generated_quantity,
                    'total_recycled_quantity': total_recycled_quantity,
                    'total_disposed_quantity': total_disposed_quantity,
                    'stock_quantity': stock_quantity,
                    'company': company_name,
                })

        return summaries

    @classmethod
    def get_all_records(cls):
        summaries_of_records = []

        for record in cls.objects.all().values('company', 'waste_code', 'generated_quantity',
                                               'recycled_quantity', 'waste_name', 'disposed_quantity', 'created',
                                               'waste_company', 'recycling_method', 'disposal_method','type_of_waste').distinct():
            created_date = record['created'].strftime('%d-%m-%Y')
            summaries_of_records.append({
                'company': record['company'],
                'waste_code': record['waste_code'],
                'waste_name': record['waste_name'],
                'type_of_waste': record['type_of_waste'],
                'generated_quantity': record['generated_quantity'],
                'recycled_quantity': record['recycled_quantity'],
                'recycling_method': record['recycling_method'],
                'disposal_method': record['disposal_method'],
                'disposed_quantity': record['disposed_quantity'],
                'waste_company': record['waste_company'],
                'created': created_date,
            })

        return summaries_of_records


    @classmethod
    def get_quantity_by_county(cls):
        unique_waste_code = cls.objects.values('waste_code').distinct()
        total_quantities_per_waste_code = []

        for waste_code in unique_waste_code:
            waste_code = waste_code['waste_code']
            county_query = cls.objects.filter(waste_code=waste_code).values_list('county', flat=True).distinct()

            for county_name in county_query:
                total_generated_quantity = \
                    cls.objects.filter(waste_code=waste_code, county=county_name).aggregate(Sum('generated_quantity'))[
                        'generated_quantity__sum'] or 0
                total_recycled_quantity = \
                    cls.objects.filter(waste_code=waste_code, county=county_name).aggregate(Sum('recycled_quantity'))[
                        'recycled_quantity__sum'] or 0

                total_disposed_quantity = \
                    cls.objects.filter(waste_code=waste_code, county=county_name).aggregate(Sum('disposed_quantity'))[
                        'disposed_quantity__sum'] or 0

                stock_quantity = total_generated_quantity - (total_recycled_quantity + total_disposed_quantity)
                if stock_quantity < 0:
                    stock_quantity = 0

                for company_name in cls.objects.values('company').distinct():
                    total_quantities_per_waste_code.append({'company_name': company_name['company'],
                                                            'county_name': county_name,
                                                            'waste_code': waste_code,
                                                            'total_generated_quantity': total_generated_quantity,
                                                            'total_recycled_quantity': total_recycled_quantity,
                                                            'total_disposed_quantity': total_disposed_quantity,
                                                            'stock_quantity': stock_quantity,
                                                            })

        return total_quantities_per_waste_code

def __str__(self):
    return self.waste_name


class Tag(models.Model):
    name = models.CharField(null=True, blank=True, max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return self.name
