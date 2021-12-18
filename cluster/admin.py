from django.contrib import admin
from .models import ClusterModel,NoteModel,NoteEventModel
# Register your models here.
admin.site.register(ClusterModel)
admin.site.register(NoteModel)
admin.site.register(NoteEventModel)
