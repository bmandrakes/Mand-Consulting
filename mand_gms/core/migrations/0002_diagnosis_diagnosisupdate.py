# Generated by Django 5.2 on 2025-04-06 07:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('NS', 'Not Started'), ('IP', 'In Progress'), ('AP', 'Awaiting Parts'), ('CO', 'Completed')], default='NS', max_length=2)),
                ('notes', models.TextField(blank=True)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.car')),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosisUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('status_update', models.CharField(blank=True, choices=[('NS', 'Not Started'), ('IP', 'In Progress'), ('AP', 'Awaiting Parts'), ('CO', 'Completed')], max_length=2, null=True)),
                ('notes', models.TextField()),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='core.diagnosis')),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
