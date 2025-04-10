# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .models import  Diagnosis, DiagnosisStatus, DiagnosisUpdate, Invoice
from .forms import CompanySettingsForm, DiagnosisForm, DiagnosisUpdateForm
from .models import CompanySettings


@login_required
@permission_required('core.view_diagnosis')
def technician_dashboard(request):
    # Show diagnoses assigned to this technician
    diagnoses = Diagnosis.objects.filter(technician=request.user).order_by('-diagnosis_date')
    return render(request, 'core/technician_dashboard.html', {'diagnoses': diagnoses})

@login_required
@permission_required('core.add_diagnosis')
def create_diagnosis(request):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.technician = request.user
            diagnosis.save()
            return redirect('diagnosis_detail', pk=diagnosis.pk)
    else:
        form = DiagnosisForm()
    return render(request, 'core/diagnosis_form.html', {'form': form})

@login_required
@permission_required('core.view_diagnosis')
def diagnosis_detail(request, pk):
    diagnosis = get_object_or_404(Diagnosis, pk=pk)
    updates = diagnosis.updates.all().order_by('-update_time')
    
    # Pass the status choices to the template
    status_choices = diagnosis_detail.choices
    
    if request.method == 'POST':
        update_form = DiagnosisUpdateForm(request.POST)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.diagnosis = diagnosis
            update.update_by = request.user
            update.save()
            
            # Update the main diagnosis status if the update includes a status change
            if update.status_update:
                diagnosis.status = update.status_update
                if update.status_update == 'CO':  # If completed
                    diagnosis.completion_date = timezone.now()
                diagnosis.save()
                
            return redirect('diagnosis_detail', pk=pk)
    else:
        update_form = DiagnosisUpdateForm()

    return render(request, 'core/diagnosis_detail.html', {
        'diagnosis': diagnosis,
        'updates': updates,
        'update_form': update_form,
        'status_choices': status_choices,  # Pass status choices to the template
    })@login_required
@permission_required('core.view_diagnosis')
def diagnosis_detail(request, pk):
    diagnosis = get_object_or_404(Diagnosis, pk=pk)
    updates = diagnosis.updates.all().order_by('-update_time')
    
    # Pass the status choices to the template
    status_choices = DiagnosisStatus.choices
    
    if request.method == 'POST':
        update_form = DiagnosisUpdateForm(request.POST)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.diagnosis = diagnosis
            update.update_by = request.user
            update.save()
            
            # Update the main diagnosis status if the update includes a status change
            if update.status_update:
                diagnosis.status = update.status_update
                if update.status_update == 'CO':  # If completed
                    diagnosis.completion_date = timezone.now()
                diagnosis.save()
                
            return redirect('diagnosis_detail', pk=pk)
    else:
        update_form = DiagnosisUpdateForm()

    return render(request, 'core/diagnosis_detail.html', {
        'diagnosis': diagnosis,
        'updates': updates,
        'update_form': update_form,
        'status_choices': status_choices,  # Pass status choices to the template
    })

@staff_member_required
def company_settings_view(request):
    settings = CompanySettings.objects.first()
    if not settings:
        settings = CompanySettings.objects.create()

    if request.method == 'POST':
        form = CompanySettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('company_settings')
    else:
        form = CompanySettingsForm(instance=settings)

    return render(request, 'core/company_settings.html', {'form': form})


@login_required
def home(request):
    # You can render a homepage template if you want, or just redirect to login
    return render(request, 'core/home.html')  # Adjust as necessary

@staff_member_required
def invoice_preview(request, pk):
    diagnosis = get_object_or_404(Diagnosis, pk=pk)
    updates = diagnosis.diagnosisupdate_set.all()
    company = CompanySettings.objects.first()
    total = diagnosis.get_total_amount()

    return render(request, 'core/invoice_preview.html', {
        'company': company,
        'diagnosis': diagnosis,
        'updates': updates,
        'total': total
    })