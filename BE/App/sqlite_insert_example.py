import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "App.settings")
import django
django.setup()

import pandas as pd

from App.models import App

current_dir = os.getcwd()
file_path = current_dir + '/database_input.xlsx'

df = pd.read_excel(file_path)

for index, row in df.iterrows():
    test = App(corp_num=row.iloc[0], corp_name=row.iloc[1], corp_jamo=row.iloc[2], is_dart=row.iloc[3])
    test.save()
    
all_apps = App.objects.all()
for app in all_apps:
    print(app.corp_name, app.corp_num, app.corp_jamo)