from django.contrib import admin
from .models import DonorProfile, UserBloodRequest
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_active",)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class DonorProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "blood_group",
        "district",
        "gender",
        "is_available",
        "date_of_donation",
    ]


class UserBloodRequestAdmin(admin.ModelAdmin):
    list_display = [
        "donor_name",
        "blood_group",
        "gender",
        "district",
        "blood_request_type",
        "details",
        "cancel",
    ]

    def donor_name(self, obj):
        return obj.donor.user.first_name


admin.site.register(DonorProfile, DonorProfileAdmin)
admin.site.register(UserBloodRequest, UserBloodRequestAdmin)
