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
    ClusterViews Url test begins here
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

    def test_clusterownernoteupdate_url_is_resolved(self):    
        url=reverse('cluster:clusterownernoteupdate',args=[self.testcluster.code_name,self.testnote.code])
        self.assertEqual(resolve(url).func.view_class,ClusterOwnerNoteUpdateView)            

    '''
    NoteViews Url test begins here
    '''

    def test_notecreate_url_is_resolved(self):    
        url=reverse('cluster:notecreate')
        self.assertEqual(resolve(url).func.view_class,NoteCreateView)

    def test_noteupdate_url_is_resolved(self):    
        url=reverse('cluster:noteupdate',args=[self.testcluster.code_name,self.testnote.code])
        self.assertEqual(resolve(url).func.view_class,NoteUpdateView)

    def test_notedetail_url_is_resolved(self):    
        url=reverse('cluster:notedetail',args=[self.testcluster.code_name,self.testnote.code])
        self.assertEqual(resolve(url).func.view_class,NoteDetailView)

    def test_notedelete_url_is_resolved(self):    
        url=reverse('cluster:notedelete',args=[self.testcluster.code_name,self.testnote.code])
        self.assertEqual(resolve(url).func.view_class,NoteDeleteView)

    def tearDown(self):
        self.user.delete()
        self.testcluster.delete()
        self.testnote.delete()          