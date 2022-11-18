from django.contrib import admin
from django.urls import path, include,re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("id/", include("identification.urls")),
    path("API/", include("API.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("bracket/", include("bracket.urls")),
    ]
