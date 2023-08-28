import re
from django import forms
from .models import ClusterModel,NoteModel
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from cluster.mixins import CoverFileSizeValidation

class ClusterCreationForm(forms.ModelForm,CoverFileSizeValidation):
    
    class Meta:
        model = ClusterModel
        
        labels={
            "cluster_name": "Cluster Name",
        }
        
        fields = [
            "cluster_name",
            "cover",
            "code_name",
            "description",
            "permission",
        ]



    def clean_code_name(self):
        code_name= self.cleaned_data['code_name']
        if not re.match(r'^[0-9a-zA-Z]*$',code_name):
                raise forms.ValidationError("Sorry , you can only have alphanumeric in Cluster code name") 
        return code_name

class ClusterUpdateForm(forms.ModelForm,CoverFileSizeValidation):
    
    class Meta:
        model = ClusterModel
        
        labels={
            "cluster_name": "Cluster Name",
        }
        
        fields = [
            "cluster_name",
            "cover",
            "code_name",
            "description",
            "permission",
        ]
    
    def clean_code_name(self):
        code_name= self.cleaned_data['code_name']
        if not re.match(r'^[0-9a-zA-Z]*$',code_name):
                raise forms.ValidationError("Sorry , you can only have alphanumeric in Cluster code name") 
        return code_name

class NoteCreationForm(forms.ModelForm,CoverFileSizeValidation):
    
    def __init__(self,*args, **kwargs):
            request=kwargs.pop("request")
            cluster=ClusterModel.objects.filter(owner=request.user)
            super(NoteCreationForm,self).__init__(*args,**kwargs)
            self.fields["cluster"]=forms.ModelChoiceField(queryset=cluster)

    class Meta:
        model = NoteModel
        widgets = {
            'body':SummernoteWidget(),
        }
        fields = [
            "title",
            "summary",
            "cluster",
            "cover",
            "code",
            "body",
        ]
    def clean_code(self):
        #'clean code'no pun intended
        code= self.cleaned_data['code']
        if not re.match(r'^[0-9a-zA-Z]*$',code):
                raise forms.ValidationError("Sorry , you can only have alphanumeric in code name") 
        return code    

class NoteUpdateForm(forms.ModelForm,CoverFileSizeValidation):
                            
    class Meta:
        model = NoteModel
        widgets = {
            'body':SummernoteWidget(),
        }
        fields = [
            "title",
            "summary",
            "cover",
            "body",
            "is_verified",
        ]
        exclude=[
            "is_verified",
        ]
 

    def clean_code(self):
        code= self.cleaned_data['code']
        if not re.match(r'^[0-9a-zA-Z]*$',code):
                raise forms.ValidationError("Sorry , you can only have alphanumeric in code name") 
        return code    
        
        

class ClusterNoteCreationForm(forms.ModelForm,CoverFileSizeValidation):
    
    def __init__(self,*args, **kwargs):
            code_name=kwargs.pop("cluster_code_name")
            #cluster=ClusterModel.objects.get(code_name=code_name)
            super(ClusterNoteCreationForm,self).__init__(*args,**kwargs)
            self.fields["cluster"].queryset=ClusterModel.objects.filter(code_name=code_name)
        

    class Meta:
        model = NoteModel
        widgets = {
            'body':SummernoteWidget(),
        }
        fields = [
            "title",
            "summary",
            "code",
            "cover",
            "body",
            "cluster",
        ]

    def clean_code(self):
        code= self.cleaned_data['code']
        if not re.match(r'^[0-9a-zA-Z]*$',code):
                raise forms.ValidationError("Sorry , you can only have alphanumeric in code name") 
        return code    


class ClusterOwnerNoteUpdateForm(forms.ModelForm,CoverFileSizeValidation):
                            
    class Meta:
        model = NoteModel
        widgets = {
            'body':SummernoteWidget(),
        }
        fields = [
            "title",
            "summary",
            "cover",
            "body",
            "is_verified",
        ]
 

    def clean_code(self):
        code= self.cleaned_data['code']
        if not re.match(r'^[0-9a-zA-Z]*$',code):
                raise forms.ValidationError("Sorry , you can only have alphanumeric in code name") 
        return code    
      
class AddUserToClusterForm(forms.Form):
    username = forms.CharField(label='Username')
    
