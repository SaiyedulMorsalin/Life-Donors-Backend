from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DonorProfile, UserBloodRequest, UserBloodDonate
from .constants import BLOOD_GROUP, GENDER_TYPE


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    mobile_number = serializers.CharField(max_length=11, required=True)
    blood_group = serializers.ChoiceField(choices=BLOOD_GROUP, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "blood_group",
            "password",
            "confirm_password",
        ]

    def validate(self, data):
        """Ensure passwords match and email is unique."""
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords don't match."})

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        return data

    def create(self, validated_data):
        """Create a new user with the validated data."""
        # Remove confirm_password field as it's not part of the User model
        validated_data.pop("confirm_password")

        # Extract fields for user creation
        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        mobile_number = validated_data["mobile_number"]
        blood_group = validated_data["blood_group"]
        password = validated_data["password"]

        # Create and save the User instance
        user = User.objects.create(
            username=username, first_name=first_name, last_name=last_name, email=email
        )
        user.set_password(password)
        user.is_active = False  # Account is inactive until email verification
        user.save()

        # Create the related DonorProfile instance
        DonorProfile.objects.create(
            user=user,
            blood_group=blood_group,
            gender="",  # Assign default or empty value as required
            district="",  # Assign default or empty value as required
            mobile_number=mobile_number,
            email=email,
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class DonorProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = DonorProfile
        fields = fields = [
            "user",
            "blood_group",
            "district",
            "date_of_donation",
            "gender",
            "is_available",
            "mobile_number",
            "email",
        ]


class UpdateDonorProfileSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(write_only=True)  # To accept user ID in input

    class Meta:
        model = DonorProfile
        fields = [
            # "user_id",
            "district",
            "date_of_donation",
            "gender",
        ]

    def update(self, instance, validated_data):
        # Update instance fields with validated data
        instance.district = validated_data.get("district", instance.district)
        instance.date_of_donation = validated_data.get(
            "date_of_donation", instance.date_of_donation
        )
        instance.gender = validated_data.get("gender", instance.gender)

        instance.save()
        return instance


class UserBloodRequestSerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField(many=False)
    user_id = serializers.IntegerField(write_only=True)
    req_donor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserBloodRequest
        fields = [
            "donor",
            "req_donor_id",
            "id",
            "user_id",
            "blood_group",
            "blood_request_type",
            "district",
            "date_of_donation",
            "gender",
            "accepted_donor_id",
            "details",
        ]


class UserBloodDonateSerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField(many=False)
    donor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserBloodDonate
        fields = [
            "donor",
            "donor_id",
            "blood_group",
            "district",
            "date_of_donation",
            "blood_request_type",
            "approve_donor_id",
            "gender",
            "details",
        ]
