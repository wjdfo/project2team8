import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "App.settings")
import django
django.setup()

from .models import App

def recommendation(search):
    matching_stocks = App.objects.filter(corp_name__icontains=search) | \
                    App.objects.filter(corp_num__icontains=search) | \
                    App.objects.filter(corp_jamo__icontains=search)

    return matching_stocks