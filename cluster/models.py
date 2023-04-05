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
    cover=models.ImageField(default="default_cluster_cover.jpg",upload_to="cluster_cover")
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="ClusterModel_User")
    description=models.TextField(max_length=600,default="Empty")
    date=models.DateField(auto_now=True)
    permission=models.CharField(choices=Permission_level,max_length=10,default="PO")
    members = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return f"{self.code_name}"
     

class NoteModel(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="NoteModel_User")
    title=models.CharField(max_length=50)
    cover=models.ImageField(upload_to="note_cover", height_field=None, width_field=None, max_length=None)
    is_verified=models.BooleanField(default=False)
    is_verified_updated=models.BooleanField(default=False)
    code=models.CharField(max_length=20,unique=True)
    summary=models.CharField(max_length=250,default="None")
    body=models.TextField(max_length=100000,default="Empty")
    cluster=models.ForeignKey("ClusterModel", on_delete=models.CASCADE,related_name="NoteModel_ClusterModel")

    @property
    def updates_count(self):
        return NoteEventModel.objects.filter(event_model=self).count() 

    @property
    def views_count(self):
        return NoteStatsViewModel.objects.filter(note=self).count()
    
    
    # @property
    # def views_count(self):
    #     return NoteStatsModel.objects.filter(post=self).count()
    
    def __str__(self):
        return f"{self.code}"

class NoteEventModel(models.Model):
    Event_list=(
        ("created","created"),
        ("updated","updated"),
        ("approved","approved"),
    )

    event_model=models.ForeignKey(NoteModel ,on_delete=models.CASCADE,related_name="NoteEventModel_NoteModel")
    event_name=models.CharField(choices=Event_list, max_length=20)
    event_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="NoteEventModel_User")

    def __str__(self):
        return f"{self.event_model} {self.event_name} by {self.event_by}"

# class ClusterGallery(models.Model):
#     cluster=models.ForeignKey(ClusterModel,on_delete=models.CASCADE,related_name='ClusterGallery_ClusterModel')
#     image=models.ImageField(upload_to="Cluster images", height_field=None, width_field=None, max_length=None)

#     def __str__(self):
#         return f'{self.cluster}\'s Image'

class NoteStatsViewModel(models.Model):
    note=models.ForeignKey(NoteModel, on_delete=models.CASCADE,related_name='NoteStatsModel_NoteModel')
    ip_address= models.GenericIPAddressField(default="0.0.0.0")

    def __str__(self):
        return f'{self.ip_address} in {self.note.title} post'

# class BookMarkModel(models.Model):
#     bookmarked=models.ForeignKey("app.Model", verbose_name=_("test"), on_delete=models.CASCADE)

