from django.forms import ModelForm
from .models import ClusterModel

class ClusterCreationForm(ModelForm):
    
    class Meta:
        model = ClusterModel
        fields = [
            ""
        ]
