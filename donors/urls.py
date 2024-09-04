from django.urls import path, include
from rest_framework import routers
from . import views

# Initialize the default router
router = routers.DefaultRouter()

# Register the ViewSets with the router
# router.register(r"requests", views.UserBloodRequestViewSet, basename="userbloodrequest")
router.register(r"donors", views.DonorSearchViewSet, basename="donor")

router.register(
    r"request_search", views.RequestsSearchViewSet, basename="request_search"
)
router.register(r"requests", views.UserBloodRequestView, basename="userbloodrequest")
router.register(r"available_request", views.BloodRequestView, basename="anyone_donate")

# Define urlpatterns
urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="user_register"),
    path(
        "profile/<int:user_id>/",
        views.UserProfileAPIView.as_view(),
        name="user_profile",
    ),
    path("login/", views.UserLoginApiView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path(
        "dashboard/<int:donor_id>/",
        views.UserDashboardAPIView.as_view(),
        name="user_dashboard",
    ),
    path(
        "create/request/",
        views.CreateUserBloodRequestView.as_view(),
        name="create_request",
    ),
    path(
        "create/donate/",
        views.CreateUserBloodDonateView.as_view(),
        name="create_donate",
    ),
    path(
        "update/profile/<int:pk>/",
        views.UpdateDonorProfileView.as_view(),
        name="update_profile",
    ),
    path("activate/<str:uid64>/<str:token>/", views.activate, name="activate"),
    path(
        "accept/request/<int:pk>/",
        views.UserBloodRequestAcceptView.as_view(),
        name="accept_request",
    ),
    path(
        "approve/request/<int:pk>/",
        views.UserBloodRequestApproveView.as_view(),
        name="accept_request",
    ),
    path("", include(router.urls)),
]
