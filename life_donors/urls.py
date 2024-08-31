from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("donors.urls")),
    path("blood/", include("bloods.urls")),
]
