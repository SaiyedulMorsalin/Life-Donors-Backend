from django_filters import rest_framework as filters
from .models import DonorProfile


class DonorProfileFilter(filters.FilterSet):
    blood_group = filters.CharFilter(field_name="blood_group", lookup_expr="iexact")
    district = filters.CharFilter(field_name="district", lookup_expr="iexact")
    date_of_donation = filters.DateFilter(
        field_name="date_of_donation", lookup_expr="exact"
    )
    # donor_type = filters.CharFilter(field_name="donor_type", lookup_expr="iexact")  # Remove or replace this line

    class Meta:
        model = DonorProfile
        fields = [
            "blood_group",
            "district",
            "date_of_donation",
        ]
