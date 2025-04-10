from django.contrib import admin
from .models import Car, Customer, SparePart, Invoice

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'car_model', 'plate_number', 'customer', 'year')
    search_fields = ('plate_number', 'car_make', 'car_model')
    list_filter = ('year',)

admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(SparePart)
# Register custom User model if you have one
