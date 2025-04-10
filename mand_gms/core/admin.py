from django.contrib import admin
from .models import Car, Diagnosis, DiagnosisUpdate  # Import your Car model
from .models import Customer  # Import your customer model
from .models import Invoice  # Import your invoices model
from .models import SparePart #Import your Spareparts model
from .models import CompanySettings


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'car_model', 'plate_number', 'year', 'customer')
    search_fields = ('plate_number', 'car_make', 'car_model')
    list_filter = ('year', 'car_make')
    ordering = ('-year',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name',)

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity_in_stock')
    search_fields = ('name',)
    list_filter = ('price',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'car', 'total_amount')
    search_fields = ('customer__first_name', 'customer__last_name')
    ordering = ('-id',)
   
@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('car', 'technician', 'diagnosis_date', 'status')
    list_filter = ('status', 'technician')
    search_fields = ('car__name', 'technician__username', 'description')

@admin.register(DiagnosisUpdate)
class DiagnosisUpdateAdmin(admin.ModelAdmin):
    list_display = ('diagnosis', 'update_time', 'update_by', 'status_update', 'notes')
    list_filter = ('status_update', 'update_by')
    search_fields = ('diagnosis__car__name', 'notes')

@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'vat_number', 'tel')
