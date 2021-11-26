from django import forms
from .models import ClusterModel,NoteModel

class ClusterCreationForm(forms.ModelForm):
    
    class Meta:
        model = ClusterModel
        fields = [
            "name",
            "code_name",
            "permission",
        ]


class NoteCreationForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
            request=kwargs.pop("request")
            cluster=ClusterModel.objects.filter(owner=request.user)
            super(NoteCreationForm,self).__init__(*args,**kwargs)
            self.fields["cluster"]=forms.ModelChoiceField(queryset=cluster)

    class Meta:
        model = NoteModel
        fields = [
            "name",
            "code",
            "body",
            "cluster",
        ]

class NoteUpdateForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
            request=kwargs.pop("request")
            cluster=ClusterModel.objects.filter(owner=request.user)
            super(NoteUpdateForm,self).__init__(*args,**kwargs)
            self.fields["cluster"]=forms.ModelChoiceField(queryset=cluster)

    class Meta:
        model = NoteModel
        fields = [
            "name",
            "body",
        ]
