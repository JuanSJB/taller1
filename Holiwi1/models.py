from django.db import models

# Create your models here.

class movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='Holiwi1/images/')
    url = models.URLField(blank=True)
