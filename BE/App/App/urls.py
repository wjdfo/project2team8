"""
URL configuration for App project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/prompt', views.API.chatbot_response, name="chatbot_response"),
    path('api/summary', views.API.summary, name="corporation_summary"),
    path('api/corporations', views.API.corporations_list, name="corporations_list"),
    path('api/report_url', views.API.report, name="corporation_report_url"),
    path('api/compare', views.API.compare, name="corporation_compare"),
]
