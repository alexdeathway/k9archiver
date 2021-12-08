from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NoteModel ,NoteEventModel

@receiver(post_save,sender=NoteModel)
def note_create_event(sender,created, instance,**kwargs ):
    if created:
        pass