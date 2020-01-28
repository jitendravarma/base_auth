from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

# Create your models here.


class BaseUserProfile(AbstractUser):
    """
    BaseUserProfile inherited from abstract user, set user type and create
    respective profile
    """

    middle_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Base User Profile"
        verbose_name_plural = "Base User Profiles"
    
    @property
    def fullname(self):
        if self.last_name and self.first_name:
            return "%s %s" % (self.first_name, self.last_name)
        elif self.first_name:
            return "%s " % (self.first_name)
        else:
            return "%s " % (self.email)

