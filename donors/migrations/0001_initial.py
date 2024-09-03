# Generated by Django 5.1 on 2024-09-03 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DonorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=4)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_donation', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('is_available', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='donors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBloodDonate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=4)),
                ('district', models.CharField(max_length=100)),
                ('date_of_donation', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('blood_request_type', models.CharField(choices=[('Pending', 'Pending'), ('Running', 'Running'), ('Completed', 'Completed')], max_length=20)),
                ('details', models.CharField(max_length=255, unique=True)),
                ('cancel', models.BooleanField(default=False)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='d_donate_profile', to='donors.donorprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UserBloodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=4)),
                ('blood_request_type', models.CharField(choices=[('Pending', 'Pending'), ('Running', 'Running'), ('Completed', 'Completed')], max_length=20)),
                ('district', models.CharField(max_length=100)),
                ('date_of_donation', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('accepted_donor_id', models.CharField(blank=True, max_length=12, null=True)),
                ('details', models.CharField(max_length=255, unique=True)),
                ('cancel', models.BooleanField(default=False)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='d_req_profile', to='donors.donorprofile')),
            ],
        ),
    ]
