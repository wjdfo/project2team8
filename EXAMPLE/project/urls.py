from django.contrib import admin
from django.urls import include, path
from project.response import Response

urlpatterns = [
    path("project/", include("project.urls")),
    # path("admin/", admin.site.urls),
]