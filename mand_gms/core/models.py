from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Model for Customer
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Model for Car Registration
class Car(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    year = models.IntegerField()
    plate_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.car_make} {self.car_model} ({self.plate_number})"

# Model for Invoice
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.id} for {self.customer}"

# Model for Spare Part Inventory
class SparePart(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Model for User (extends Django's built-in AbstractUser)
class User(AbstractUser):
    role_choices = [
        ('Admin', 'Admin'),
        ('Cashier', 'Cashier'),
        ('Controller', 'Controller'),
        ('Technician', 'Technician'),
    ]
    role = models.CharField(max_length=10, choices=role_choices)

    # Adding related_name to avoid conflict
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',  # Custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='core_user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_set',  # Custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='core_user'
    )

    def __str__(self):
        return self.username

#Technician diagnostic page 
class DiagnosisStatus(models.TextChoices):
    NOT_STARTED = 'NS', 'Not Started'
    IN_PROGRESS = 'IP', 'In Progress'
    AWAITING_PARTS = 'AP', 'Awaiting Parts'
    COMPLETED = 'CO', 'Completed'

class Diagnosis(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    diagnosis_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status = models.CharField(
        max_length=2,
        choices=DiagnosisStatus.choices,
        default=DiagnosisStatus.NOT_STARTED
    )
    notes = models.TextField(blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    def get_total_amount(self):
        return sum(update.line_total() for update in self.diagnosisupdate_set.all())

class DiagnosisUpdate(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.unit_price
    
class CompanySettings(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    address = models.TextField(blank=True)
    vat_number = models.CharField(max_length=9)
    tel = models.BigIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company Setting"
        verbose_name_plural = "Company Settings"
