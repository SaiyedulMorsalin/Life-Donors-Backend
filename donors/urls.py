from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Initialize the default router
router = routers.DefaultRouter()

# Register the ViewSet with a base name; URL parameters will be handled by ViewSet's actions
router.register(r"requests", views.UserBloodRequestViewSet, basename="userbloodrequest")
router.register("donors", views.DonorSearchViewSet, basename="donor")
urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="user_register"),
    path(
        "profile/<int:user_id>/",
        views.UserProfileAPIView.as_view(),
        name="user_profile",  # Changed name to "user_profile"
    ),
    path("login/", views.UserLoginApiView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path(
        "dashboard/<int:user_id>/",
        views.UserDashboardAPIView.as_view(),
        name="user_dashboard",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/activate/<str:uid64>/<str:token>/", views.activate, name="activate"),
    path("", include(router.urls)),
]
