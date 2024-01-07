from django.urls import path
from . import views

urlpatterns = [path('', views.records, name='records'),
               path('record/<str:pk>/', views.record, name='record'),
               path('create-record/', views.create_record, name='create-record'),
               path('update-record/<str:pk>/', views.update_record, name='update-record'),
               path('delete-record/<str:pk>/', views.delete_record, name='delete-record'),
               path('reports/', views.get_reports, name='reports'),
               path('export-to-csv/', views.export_to_csv, name='export-to-csv'),
               path('export/', views.export_to_csv_view, name='export'),
               path('export-to-pdf/', views.export_to_pdf, name='export-pdf'),
               path('export-pdf-view/', views.export_to_pdf_view, name='export-pdf-view'),
               ]
