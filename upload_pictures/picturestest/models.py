from django.db import models


# Create your models here.

class PicTest(models.Model):
    pic = models.ImageField(upload_to='book/')
