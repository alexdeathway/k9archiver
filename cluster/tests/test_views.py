from multiprocessing.connection import Client
from django.test import TestCase,Client
from django.urls import reverse,resolve
from cluster.models import ClusterModel,NoteModel
from django.contrib.auth import get_user_model
from django.conf import settings
import datetime, os, random, string 
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

def dummy_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class TestView(TestCase):
    

    def setUp(self):
        '''
        TEST_ASSETS_DIR contains external required content for test. 
        '''
        self.TEST_ASSETS_DIR=os.path.join(settings.BASE_DIR,'test_assets')
        
        #dummy user data will be used to create and login during the test session
        self.user_dummy_username='testuser'
        self.user_dummy_password=dummy_password()
        
        self.client=Client()
        self.user = User.objects.create_user(username=self.user_dummy_username, password=self.user_dummy_password)
        self.client=self.client.login(username=self.user_dummy_username, password=self.user_dummy_password)
        
        self.testcluster=ClusterModel.objects.create(
            cluster_name="Test Cluster View",
            code_name="testclusterview",
            owner=self.user,
            description="This cluster is created for testing",
            date=today(),
            permission="PO",
        )


        self.testnote=NoteModel.objects.create(
            author=self.user,
            title="Test Note",
            cover=os.path.join(self.TEST_ASSETS_DIR,'images/test_cover.jpeg'),
            is_verified=False,
            is_verified_updated=False,
            code="testnote",
            body="this is test note.",
            cluster=self.testcluster,
        )
           
    def test_cluster_list_view_GET(self):
        pass
