# Generated by Django 5.1 on 2024-09-03 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0005_userblooddonate_blood_request_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbloodrequest',
            name='accepted_donor_id',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
