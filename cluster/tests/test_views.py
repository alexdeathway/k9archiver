from django.test import TestCase
from django.urls import reverse,resolve
from cluster.models import ClusterModel,NoteModel
from django.contrib.auth import get_user_model
from django.conf import settings
import datetime 
import os
from cluster.views import (
                        ClusterListView,
                        ClusterCreateView,
                        ClusterDetailView,
                        ClusterUpdateView,
                        ClusterDeleteView,
                        ClusterNoteCreateView,
                        ClusterOwnerNoteUpdateView,
                        NoteCreateView,
                        NoteUpdateView,
                        NoteDetailView,
                        NoteDeleteView,
                    )  


User=get_user_model()

def today():
    return datetime.date.today()

class TestUrl(TestCase):
    
    # def test_upload_image(image):
    #         file=File(open(image))
    #         return file

    def setUp(self):
        '''
        TEST_ASSETS_DIR contains external required content for test. 
        '''

        self.TEST_ASSETS_DIR=os.path.join(settings.BASE_DIR,'test_assets')
        
        self.user = User.objects.create_user(username='testuser', password='password')
        self.testcluster=ClusterModel.objects.create(
            cluster_name="Test Cluster",
            code_name="testcluster",
            owner=self.user,
            description="This cluster is created for testing",
            date=today(),
            permission="PO",
        )


        # self.testnote=NoteModel.objects.create(
        #     author=self.user,
        #     title="Test Note",
        #     cover=self.test_upload_image('test_cover.jpg'),
        #     is_verified=False,
        #     is_verified_updated=False,
        #     code="testnote",
        #     body="this is test note.",
        #     cluster=self.testcluster,
        # )
    
    