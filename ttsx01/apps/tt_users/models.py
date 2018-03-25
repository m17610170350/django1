from django.db import models
from utils.models import BaseModel
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser, BaseModel):
    class Meta:  # ttsx --> dailyfresh --> df
        db_table = 'tt_users'


class AreaInfo(models.Model):
    title = models.CharField(max_length=20)
    aParent = models.ForeignKey('self', null=True, blank=True)


class AddressInfo(BaseModel):
    receiver = models.CharField(max_length=10)
    province = models.ForeignKey('AreaInfo', related_name='province')
    city = models.ForeignKey('AreaInfo', related_name='city')
    district = models.ForeignKey('AreaInfo', related_name='district')
    addr = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=11)
    isDefault = models.BooleanField(default=0)
    user = models.ForeignKey('UserInfo')

    class Meta:
        db_table = 'df_address'
