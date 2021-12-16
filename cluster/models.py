from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models.fields import chp


User=get_user_model()

class ClusterModel(models.Model):
    Permission_level=(
        ("p","Public"),
        ("PO","Participant Only"),       
    )        
    cluster_name=models.CharField(max_length=100)
    code_name=models.CharField(max_length=20,unique=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="ClusterModel_User")
    description=models.CharField(max_length=600,default="Empty")
    date=models.DateField(auto_now=True)
    permission=models.CharField(choices=Permission_level,max_length=10,default="PO")
    participant=None

    def __str__(self):
        return f"{self.code_name}"
     

class NoteModel(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="NoteModel_User")
    title=models.CharField(max_length=50)
    cover=models.ImageField(upload_to="note_cover", height_field=None, width_field=None, max_length=None)
    is_verified=models.BooleanField(default=False)
    is_verified_updated=models.BooleanField(default=False)
    code=models.CharField(max_length=20,unique=True)
    body=models.CharField(max_length=15000,default="Empty")
    cluster=models.ForeignKey("ClusterModel", on_delete=models.CASCADE,related_name="NoteModel_ClusterModel")

    def __str__(self):
        return f"{self.code}"




