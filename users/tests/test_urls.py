from django.test import TestCase
from django.urls import reverse,resolve
from cluster.models import ClusterModel,NoteModel
from django.contrib.auth import get_user_model
from django.conf import settings
import random, datetime, os,string
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


class TestUrl(TestCase):
    

    def setUp(self):
        '''
        
        TEST_ASSETS_DIR contains external required content for test. 
        
        Test func naming: test_<name of url>_url_is_resolved
        for ex if url is: path("create/",ClusterCreateView.as_view(),name="clustercreate"),
                    then:  test_clustercreate_url_is_resolved
        
        '''

        self.TEST_ASSETS_DIR=os.path.join(settings.BASE_DIR,'test_assets')

        #dummy user data will be used to create and login during the test session 
        self.user_dummy_username='testuser'
        self.user_dummy_password=dummy_password()
        
        self.user = User.objects.create_user(username=self.user_dummy_username, password=self.user_dummy_password)
        self.testcluster=ClusterModel.objects.create(
            cluster_name="Test Cluster",
            code_name="testcluster",
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
    
    '''
    Users Url test begins here
    '''