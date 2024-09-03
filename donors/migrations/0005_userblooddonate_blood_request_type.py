# Generated by Django 5.1 on 2024-09-03 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0004_remove_userblooddonate_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='userblooddonate',
            name='blood_request_type',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Running', 'Running'), ('Completed', 'Completed')], max_length=20, null=True),
        ),
    ]
