import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "App.settings")
import django
django.setup()

from App.models import App

test = App(corp_name="현대자동차", corp_num="1234", corp_jamo="ㅎㄷㅈㄷㅊ")
test.save()

all_apps = App.objects.all()
for app in all_apps:
    print(app.corp_name, app.corp_num, app.corp_jamo)
