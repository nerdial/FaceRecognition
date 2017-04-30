from django.db import models

# Create your models here.
class Camera(models.Model):
    url = models.TextField()
    name = models.CharField(max_length=200)
    camera_type = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=500)
    active = models.BooleanField(default=False)
    in_use = models.BooleanField(default=False)
    def in_active_mode(self):
        self.in_use = False
        self.active = False
        self.save()

    #def active_mode(self):

    def in_use_mode(self):
        self.in_use = True
        self.save()