from django.urls import path, include
from rest_framework import routers
from . import views

# Initialize the default router
router = routers.DefaultRouter()

# Register the ViewSets with the router
# router.register(r"requests", views.UserBloodRequestViewSet, basename="userbloodrequest")
router.register(r"donors", views.DonorSearchViewSet, basename="donor")

router.register(r"requests", views.UserBloodRequestView, basename="userbloodrequest")

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
        "dashboard/<int:user_id>/",
        views.UserDashboardAPIView.as_view(),
        name="user_dashboard",
    ),
    path(
        "create/request/",
        views.CreateUserBloodRequestView.as_view(),
        name="create_request",
    ),
    path("users/activate/<str:uid64>/<str:token>/", views.activate, name="activate"),
    # path(
    #     "requests/",
    #     views.UserBloodRequestAPIView.as_view(),
    #     name="blood_requests",
    # ),
    path("", include(router.urls)),
]
