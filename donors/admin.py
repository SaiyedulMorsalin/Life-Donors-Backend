from django.contrib import admin
from .models import DonorProfile, UserBloodRequest

# Register your models here.
admin.site.register(DonorProfile)
admin.site.register(UserBloodRequest)
