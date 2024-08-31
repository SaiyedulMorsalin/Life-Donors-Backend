from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BloodRequest(models.Model):
    pass


class DonationRequest(models.Model):
    pass


class BloodHistory(models.Model):
    users = models.ForeignKey(User, related_name="all_donors", on_delete=models.CASCADE)
    request_history = models.ForeignKey(
        BloodRequest, related_name="req_history", on_delete=models.CASCADE
    )
    donation_history = models.ForeignKey(
        DonationRequest, related_name="donates_history", on_delete=models.CASCADE
    )
    pass


class BloodCampaign(models.Model):
    users = models.OneToOneField(
        User, related_name="camp_user", on_delete=models.CASCADE
    )
    campaign_date = models.DateTimeField()
    district = models.CharField(max_length=25)
    location = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=4)
    pass
