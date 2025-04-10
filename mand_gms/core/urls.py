# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('technician/', views.technician_dashboard, name='technician_dashboard'),
    path('technician/diagnosis/new/', views.create_diagnosis, name='create_diagnosis'),
    path('technician/diagnosis/<int:pk>/', views.diagnosis_detail, name='diagnosis_detail'),
    path('admin/company-settings/', views.company_settings_view, name='company_settings'),
    path('invoice/<int:pk>/', views.invoice_view, name='invoice_detail'),
    path('invoice/preview/<int:pk>/', views.invoice_preview, name='invoice_preview'),

]