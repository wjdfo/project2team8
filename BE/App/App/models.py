from django.db import models

class App(models.Model):
    corp_num = models.CharField(max_length=30)
    corp_name = models.CharField(max_length=50)
    corp_jamo = models.CharField(max_length=50)
    is_dart = models.CharField(max_length=30)
