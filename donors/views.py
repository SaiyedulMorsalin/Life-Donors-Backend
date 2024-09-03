from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status, filters, generics


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend


from .filters import DonorProfileFilter, RequestFilter
from .serializers import (
    UserRegistrationSerializer,
    DonorProfileSerializer,
    UserBloodRequestSerializer,
    UserLoginSerializer,
    UpdateDonorProfileSerializer,
    UserBloodDonateSerializer,
)
from .models import DonorProfile, UserBloodRequest, UserBloodDonate
import logging

logger = logging.getLogger(__name__)


# Create your views here.


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = request.build_absolute_uri(
                reverse("activate", kwargs={"uid64": uid, "token": token})
            )
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                "confirm_email.html", {"confirm_link": confirm_link}
            )

            try:
                email = EmailMultiAlternatives(email_subject, "", to=[user.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
                return Response(
                    {"message": "Check your email for confirmation."},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                return Response(
                    {"error": "Failed to send confirmation email."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Function View to Activate User Account via Email Link
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return redirect("user_register")


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)

                session_id = request.session.session_key

                # If session ID doesn't exist yet, create it
                if not session_id:
                    request.session.create()
                    session_id = request.session.session_key

                return Response(
                    {"token": token.key, "user_id": user.id, "session_id": session_id},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid Credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect("login")


class UserProfileAPIView(APIView):

    def get(self, request, user_id, *args, **kwargs):
        try:
            user_profiles = DonorProfile.objects.filter(user__id=user_id)
            serializer = DonorProfileSerializer(user_profiles, many=True)
            return Response(serializer.data)
        except DonorProfile.DoesNotExist:
            return Response(
                {"error": "UserProfile not found...."}, status=status.HTTP_404_NOT_FOUND
            )


class UserBloodRequestView(viewsets.ModelViewSet):
    serializer_class = UserBloodRequestSerializer

    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = UserBloodRequest.objects.all()
        donor_id = self.request.query_params.get("donor_id")
        if donor_id:
            queryset = queryset.filter(donor_id=donor_id)
        return queryset


class BloodRequestView(viewsets.ModelViewSet):
    serializer_class = UserBloodRequestSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserBloodRequest.objects.filter(
            blood_request_type__in=["Pending", "Running"]
        )
        donor_id = self.request.query_params.get("donor_id")
        if donor_id:
            queryset = queryset.exclude(donor_id=donor_id)
        print(donor_id)
        return queryset


class CreateUserBloodRequestView(APIView):

    def post(self, request):
        serializer = UserBloodRequestSerializer(data=request.data)

        if serializer.is_valid():
            # Extracting the validated data
            blood_group = serializer.validated_data["blood_group"]
            user_id = serializer.validated_data["user_id"]
            blood_request_type = serializer.validated_data["blood_request_type"]
            district = serializer.validated_data["district"]
            date_of_donation = serializer.validated_data["date_of_donation"]
            gender = serializer.validated_data["gender"]
            details = serializer.validated_data["details"]

            if user_id:

                # Fetch the DonorProfile instance instead of UserBloodRequest
                donor_profile = get_object_or_404(DonorProfile, user__id=user_id)
                user_data = serializer.validated_data.pop("user_id")
                # Creating a new UserBloodRequest instance with the correct donor profile
                if (
                    donor_profile.blood_group
                    and donor_profile.district
                    and donor_profile.gender
                ):
                    UserBloodRequest.objects.create(
                        donor=donor_profile,
                        blood_group=blood_group,
                        blood_request_type="Pending",
                        district=district,
                        date_of_donation=date_of_donation,
                        gender=gender,
                        details=details,
                    )
                    print(donor_profile)
                    return Response(
                        {"message": "Your Blood Request Create Successfully!!"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "message": "Please your Profile fully updated then make a request for blood....."
                        },
                        status=status.HTTP_200_OK,
                    )

            else:
                return Response(
                    {"error": "Invalid Credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDashboardAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserBloodRequestSerializer

    def get(self, request, donor_id, *args, **kwargs):

        try:
            donor_profile = get_object_or_404(DonorProfile, id=donor_id)
            print("users_pro", donor_profile.user)
        except DonorProfile.DoesNotExist:
            return Response({"error": "Donor profile not found."}, status=404)

        # Fetch the user's own blood requests
        user_requests = UserBloodRequest.objects.filter(donor__user=donor_profile.user)
        print("user_req", user_requests)
        user_requests_serializer = UserBloodRequestSerializer(user_requests, many=True)
        user_donates = UserBloodDonate.objects.filter(donor__user=donor_profile.user)
        user_donates_serializer = UserBloodDonateSerializer(user_donates, many=True)
        # Combine all the data into a response
        data = {
            "donor_id": donor_id,
            "my_requests": user_requests_serializer.data,
            "my_donate": user_donates_serializer.data,
            # "pending_requests": pending_requests_serializer.data,
        }

        # Return the combined data as a Response
        return Response(data, status=status.HTTP_200_OK)


class DonorSearchViewSet(viewsets.ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DonorProfileFilter
    search_fields = ["blood_group", "district", "date_of_donation"]


class UpdateDonorProfileView(generics.UpdateAPIView):
    queryset = DonorProfile.objects.all()
    serializer_class = UpdateDonorProfileSerializer


class CreateUserBloodDonateView(APIView):

    def post(self, request):
        serializer = UserBloodDonateSerializer(data=request.data)

        if serializer.is_valid():
            # Extracting the validated data
            blood_group = serializer.validated_data["blood_group"]
            blood_request_type = serializer.validated_data["blood_request_type"]
            donor_id = serializer.validated_data["donor_id"]
            district = serializer.validated_data["district"]
            date_of_donation = serializer.validated_data["date_of_donation"]
            gender = serializer.validated_data["gender"]
            details = serializer.validated_data["details"]

            if donor_id:
                # Fetch the DonorProfile instance instead of UserBloodRequest
                donor_profile = get_object_or_404(DonorProfile, user__id=donor_id)
                user_data = serializer.validated_data.pop("donor_id")
                # Creating a new UserBloodRequest instance with the correct donor profile
                UserBloodDonate.objects.create(
                    donor=donor_profile,
                    blood_group=blood_group,
                    district=district,
                    date_of_donation=date_of_donation,
                    gender=gender,
                    details=details,
                )
                print(donor_profile)

                return Response(
                    {"user": "User Found"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid Credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBloodRequestAcceptView(APIView):

    def put(self, request, pk, format=None):
        donor_id = self.request.query_params.get("donor_id")
        accept_donor = get_object_or_404(DonorProfile, id=donor_id)
        print("acc_donor", accept_donor)

        print("donor_accept_id", donor_id)
        serializer_class = UserBloodRequestSerializer
        try:
            # Fetch the UserBloodRequest instance by its primary key (pk)
            blood_request = get_object_or_404(UserBloodRequest, id=pk)
        except UserBloodRequest.DoesNotExist:
            return Response(
                {"error": "Blood request not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if blood_request and accept_donor:

            print("change before", blood_request)
            blood_request.blood_request_type = "Running"
            print("change after", blood_request)
            print("donor", blood_request.donor)
            print("id", blood_request.id)
            blood_request.save()
            return Response(
                {
                    "message": "Request Accepted  successfully.",
                    "accept_donor_id": accept_donor.id,
                },
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserBloodRequestApproveView(APIView):
    serializer_class = UserBloodRequestSerializer

    def put(self, request, pk, format=None):
        donor_id = self.request.query_params.get("donor_id")
        accept_donor = get_object_or_404(DonorProfile, id=donor_id)
        try:
            # Fetch the UserBloodRequest instance by its primary key (pk)
            blood_request = get_object_or_404(UserBloodRequest, id=pk)
        except UserBloodRequest.DoesNotExist:
            return Response(
                {"error": "Blood request not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if blood_request and accept_donor:
            UserBloodDonate.objects.create(
                donor=accept_donor,
                blood_group=accept_donor.blood_group,
                blood_request_type="Completed",
                district=accept_donor.district,
                date_of_donation=accept_donor.date_of_donation,
                gender=accept_donor.gender,
            )
            print("change before", blood_request)
            blood_request.blood_request_type = "Completed"
            print("change after", blood_request)
            print("id", blood_request.id)
            blood_request.save()
            return Response(
                {
                    "message": "Request Approved  successfully.",
                    "accept_donor_id": accept_donor.id,
                },
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestsSearchViewSet(viewsets.ModelViewSet):
    queryset = UserBloodRequest.objects.all()
    serializer_class = UserBloodRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RequestFilter
    search_fields = ["blood_group", "district", "date_of_donation"]


# class UserBloodDonateView(viewsets.ModelViewSet):
#     serializer_class = UserBloodRequestSerializer

#     # permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         queryset = UserBloodDonate.objects.all()
#         donor_id = self.request.query_params.get("donor_id")
#         if donor_id:
#             queryset = queryset.filter(donor_id=donor_id)
#         return queryset
