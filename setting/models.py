from django.db import models

class ProjectSetting(models.Model):
    recognition_algorithm = models.CharField(max_length=200)
    confidence = models.IntegerField(default=0)

