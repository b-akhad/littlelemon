from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self): 
        return self.first_name


# Add code to create Menu model
class Menu(models.Model):
   name = models.CharField(max_length=200) 
   price = models.IntegerField(null=False) 
   menu_item_description = models.TextField(max_length=1000, default='') 

   def __str__(self):
      return self.name
   



class CustomUser(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            if kwargs['password']:
                self.set_password(kwargs['password'])
        except Exception:
            pass
        finally:
            super(CustomUser, self).save(*args, **kwargs)

    
    class Meta:
        db_table = 'account'
        verbose_name = _("User")
        verbose_name_plural = _("Users")
