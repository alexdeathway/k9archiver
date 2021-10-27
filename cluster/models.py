from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User=get_user_model()


class ClusterModel(models.Model):
    name=models.CharField(max_length=50)
    code_name=models.CharField(max_length=20,unique=True)
    owner=models.OneToOneField(User, on_delete=models.CASCADE,related_name="CluseterModel_User")
    participant=None
     

class NoteModel(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="NoteModel_User")
    name=models.CharField(max_length=50)
    code=models.CharField(max_length=20,unique=True)
    cluster=models.ForeignKey("ClusterModel", on_delete=models.CASCADE,related_name="NoteModel_ClusterModel")




