from django.db import models
from django.contrib.auth.models import User
from .constants import BLOOD_GROUP, GENDER_TYPE, REQUEST_TYPE as BLOOD_REQUEST_TYPE


class DonorProfile(models.Model):
    user = models.OneToOneField(User, related_name="donors", on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP)
    district = models.CharField(max_length=100, null=True, blank=True)
    date_of_donation = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"


class UserBloodRequest(models.Model):
    donor = models.ForeignKey(
        DonorProfile, related_name="d_req_profile", on_delete=models.CASCADE
    )  # Changed 'user' to 'donor'
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP)
    blood_request_type = models.CharField(choices=BLOOD_REQUEST_TYPE, max_length=20)
    district = models.CharField(max_length=100, null=True, blank=True)
    date_of_donation = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=10)
    details = models.TextField()
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Donor: {self.donor.user.first_name} - Request: {self.blood_request_type}"
        )


class UserBloodDonate(models.Model):
    donor = models.ForeignKey(
        DonorProfile, related_name="d_donate_profile", on_delete=models.CASCADE
    )  # Changed 'user' to 'donor'
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP)
    district = models.CharField(max_length=100, null=True, blank=True)
    date_of_donation = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=10)
    details = models.TextField()
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Donor: {self.donor.user.first_name} - Request: {self.blood_request_type}"
        )
