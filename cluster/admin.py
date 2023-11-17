from django.contrib import admin
from .models import ClusterModel,NoteModel,NoteEventModel,NoteStatsViewModel,CliffNoteModel
# Register your models here.
admin.site.register(ClusterModel)
admin.site.register(NoteModel)
admin.site.register(NoteEventModel)
admin.site.register(NoteStatsViewModel)
admin.site.register(CliffNoteModel)
