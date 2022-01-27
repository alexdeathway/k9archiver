from django.core import files
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

class TestUrl(TestCase):
    
    # def test_upload_image(image):
    #         file=File(open(image))
    #         return file

    def setUp(self):
        '''
        TEST_ASSETS_DIR contains external required content for test. 
        '''

        self.TEST_ASSETS_DIR=os.path.join(settings.BASE_DIR,'test_assets')
        
        self.user = User.objects.create_user(username='testuser', password=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)))
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
    Cluster Views Url test begins here
    '''

    def test_clusterlist_url_is_resolved(self):
        url=reverse('cluster:clusterlist')
        self.assertEqual(resolve(url).func.view_class,ClusterListView)

    def test_clusterdetail_url_is_resolved(self):    
        url=reverse('cluster:clusterdetail',args=[self.testcluster.code_name])
        self.assertEqual(resolve(url).func.view_class,ClusterDetailView)

    def test_clustercreate_url_is_resolved(self):    
        url=reverse('cluster:clustercreate')
        self.assertEqual(resolve(url).func.view_class,ClusterCreateView)

    def test_clusterupdate_url_is_resolved(self):    
        url=reverse('cluster:clusterupdate',args=[self.testcluster.code_name])
        self.assertEqual(resolve(url).func.view_class,ClusterUpdateView)

    def test_clusterdelete_url_is_resolved(self):    
        url=reverse('cluster:clusterdelete',args=[self.testcluster.code_name])
        self.assertEqual(resolve(url).func.view_class,ClusterDeleteView)

    def test_clusternotecreate_url_is_resolved(self):    
        url=reverse('cluster:clusternotecreate',args=[self.testcluster.code_name])
        self.assertEqual(resolve(url).func.view_class,ClusterNoteCreateView)

    def test_clusternotecreate_url_is_resolved(self):    
        url=reverse('cluster:clusternotecreate',args=[self.testcluster.code_name])
        self.assertEqual(resolve(url).func.view_class,ClusterNoteCreateView)        

    '''
    Note Views Url test begins here
    '''