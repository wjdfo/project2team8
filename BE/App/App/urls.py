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

    path('api/dart/prompt', views.DartAPI.chatbot_response, name="dart_chatbot_response"),
    path('api/dart/corporations', views.DartAPI.corporations_list, name="dart_corporations_list"),
    path('api/dart/summary/corporation=<str:corporation>', views.DartAPI.summary, name="dart_corporation_summary"),

    path('api/edgar/prompt', views.EdgarAPI.chatbot_response, name="edgar_chatbot_response"),
    path('api/edgar/corporations', views.EdgarAPI.corporations_list, name="edgar_corporations_list"),
    path('api/edgar/summary/corporation=<str:corporation>', views.EdgarAPI.summary, name="edgar_corporation_summary"),
]
