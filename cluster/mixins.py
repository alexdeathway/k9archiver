from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin
from cluster.models import ClusterModel,NoteModel

class ClusterOwnerPermission(PermissionRequiredMixin):
    """
    For checking if user is owner of cluster
    """
    permission_denied_message="Only cluster owner can perform this action."
    raise_exception = False

    def has_permission(self) -> bool:
        object=self.get_object()
        user = self.request.user
        if isinstance(object,ClusterModel):
            cluster=object
            return user == cluster.owner
        note=object
        return  user == note.author or user == note.cluster.owner

class ClusterMemberPermission(PermissionRequiredMixin):
    """
    Objective: To check if user have certain permission in cluster, we can't allow cluster level 
    actions except note creation to member that's why this permission.
    actions: Cluster Note Create,Note modify & update 
    """
    permission_denied_message = "Sorry,You don't have permission to perform this action."

    def has_permission(self):
        object=self.get_object()
        user = self.request.user
        if isinstance(object,ClusterModel):
            """
            allow note creation if user is member or owner of cluster.
            """
            cluster=object
            return user == cluster.owner or cluster.members.filter(id=user.id).exists()
        #allow note modification        
        elif isinstance(object,NoteModel):
            note=object
            return  user == note.author or user == note.cluster.owner #or note.cluster.members.filter(id=user.id).exists()
       

