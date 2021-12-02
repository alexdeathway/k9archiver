from django import forms
from .models import ClusterModel,NoteModel

class ClusterCreationForm(forms.ModelForm):
    
    class Meta:
        model = ClusterModel
        
        labels={
            "cluster_name": "Cluster Name",
        }
        
        fields = [
            "cluster_name",
            "code_name",
            "permission",
        ]

class ClusterUpdateForm(forms.ModelForm):
    
    class Meta:
        model = ClusterModel
        
        labels={
            "cluster_name": "Cluster Name",
        }
        
        fields = [
            "cluster_name",
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
            "title",
            "code",
            "body",
            "cluster",
        ]

class NoteUpdateForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
            request=kwargs.pop("request")
            note=kwargs.get('instance') #avoid using pop here, it will remove instance from request body itself
            super(NoteUpdateForm,self).__init__(*args,**kwargs)
            if request.user == note.cluster.owner:
                self.fields['is_verified']=forms.BooleanField()

    class Meta:
        model = NoteModel
        fields = [
            "title",
            "body",
        ]
        
    