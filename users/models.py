from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_author=models.BooleanField(default=False)
    profile_picture=models.ImageField(upload_to="profile_picture", height_field=None, width_field=None, max_length=None)
    

    def __str__(self):
        return f"{self.username}"
