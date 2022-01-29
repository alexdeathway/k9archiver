from django.test import TestCase,Client,RequestFactory
from django.urls import reverse,resolve
from cluster.models import ClusterModel,NoteModel
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
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
        self.user_dummy_is_author=False
        self.user_dummy_profile_picture=os.path.join(self.TEST_ASSETS_DIR,'images/test_user_profile_picture.jpeg')
        
        self.client=Client()
        self.user=User.objects.create_user(username=self.user_dummy_username, password=self.user_dummy_password, is_author=self.user_dummy_is_author,profile_picture=self.user_dummy_profile_picture)
        self.client.login(username=self.user_dummy_username, password=self.user_dummy_password)
       
        self.testcluster=ClusterModel.objects.create(
            cluster_name="Test Cluster View",
            code_name="testclusterview",
            owner=self.user,
            description="This cluster is created for testing view",
            date=today(),
            permission="PO",
        )

        self.testnote=NoteModel.objects.create(
            author=self.user,
            title="Test Note",
            cover=os.path.join(self.TEST_ASSETS_DIR,'images/test_cover.jpeg'),
            is_verified=False,
            is_verified_updated=False,
            code="testnoteview",
            body="this is test note view.",
            cluster=self.testcluster,
        )
           
    def test_clusterlist_view_GET(self):
        template="cluster/cluster_list.html"
        url= reverse('cluster:clusterlist')
        
        response=self.client.get(url)
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,template)

    def test_clustercreate_view_POST(self):
        template="cluster/cluster_create.html"
        url= reverse('cluster:clustercreate')
        response=self.client.post(url,data={
            "cluster_name":"Test Cluster View create",
            "cluster_code":"testclusterviewcreate",
            "description":"This cluster is created for testing view clustercreate",
            "permission":"PO",
        })

        #this part need redirect and post data testing

        # self.assertTemplateUsed(response,template)
        # self.assertEqual(response.status_code,302)
        # self.assertEqual(ClusterModel.objects.first().code_name,"testclusterviewcreate")
    
    def test_clusterdetail_view_GET(self):
        template="cluster/cluster_detail.html"
        url= reverse('cluster:clusterdetail',args=[self.testcluster.code_name])
        response=self.client.get(url)
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,template)  

    def test_clusterupdate_view_GET(self):
        template="cluster/cluster_update.html"
        url= reverse('cluster:clusterupdate',args=[self.testcluster.code_name])
        response=self.client.get(url)
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,template)

    def test_clusterupdate_view_POST(self):
        template="cluster/cluster_update.html"
        url= reverse('cluster:clusterupdate',args=[self.testcluster.code_name])
        request=RequestFactory()
        request.user=self.user
        request.post(url)
        response=ClusterUpdateView.as_view()(request)

        
        self.assertEqual(response.status_code,302)
        self.assertEqual(ClusterModel.objects.get(cluster_code="testclusterview").cluster_name,"Updated Test Cluster View")     
    
    def test_clusterdelete_view(self):
        template="cluster/cluster_delete.html"
        url= reverse('cluster:clusterdelete',args=[self.testcluster.code_name])
        
        #[GET]response for template test
        response=self.client.get(url)
        self.assertTemplateUsed(response,template)   
        
        #[POST]response confirming delete
        response_confirm=self.client.post(url)
        self.assertEqual(response_confirm.status_code,302)

                 

    
    def tearDown(self):
        self.testcluster.delete()
        self.testnote.delete()


