from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models.fields import chp


User=get_user_model()

class ClusterModel(models.Model):
    Permission_level=(
        ("PO","Participant Only"),
        ("p","Public"),
    )        
    name=models.CharField(max_length=50)
    code_name=models.CharField(max_length=20,unique=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="CluseterModel_User")
    permission=models.CharField(choices=Permission_level,max_length=10,default="PO")
    participant=None

    def __str__(self):
        return f"{self.code_name}"
     

class NoteModel(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="NoteModel_User")
    name=models.CharField(max_length=50)
    code=models.CharField(max_length=20,unique=True)
    body=models.CharField(max_length=1200,default="Empty")
    cluster=models.ForeignKey("ClusterModel", on_delete=models.CASCADE,related_name="NoteModel_ClusterModel")

    def __str__(self):
        return f"{self.code}"


