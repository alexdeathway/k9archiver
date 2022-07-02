from django.test import TestCase,Client
from django.urls import reverse,resolve
from cluster.models import ClusterModel,NoteModel
from django.contrib.auth import get_user_model
from django.conf import settings
import os, random, string 

User=get_user_model()

def dummy_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class TestView(TestCase):
    

    def setUp(self):
        '''
        TEST_ASSETS_DIR contains external required content for test. 

        Test func naming: test_<name of url>_view_<METHOD>
        for ex if url is: path("create/",ClusterCreateView.as_view(),name="clustercreate"),
                    then:  test_clustercreate_view_POST

        Use different func for GET and POST method testing except for delete              

        '''
        self.TEST_ASSETS_DIR=os.path.join(settings.BASE_DIR,'test_assets')
        
        #dummy user data will be used to create and login during the test session
        self.user_dummy_username='testuser'
        self.user_dummy_password=dummy_password()
        self.user_dummy_is_author=False
        self.user_dummy_profile_picture=os.path.join(self.TEST_ASSETS_DIR,'images/test_user_profile_picture.jpeg')
        
        self.client=Client(enforce_csrf_checks=True)
        self.user=User.objects.create_user(username=self.user_dummy_username, password=self.user_dummy_password, is_author=self.user_dummy_is_author,profile_picture=self.user_dummy_profile_picture)
        self.client.login(username=self.user_dummy_username, password=self.user_dummy_password)
       
        self.testcluster=ClusterModel.objects.create(
            cluster_name="Test Cluster View",
            code_name="testclusterview",
            owner=self.user,
            description="This cluster is created for testing view",
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

        url= reverse('cluster:clustercreate',)
        data={
            'cluster_name':'Test Cluster View create',
            'code_name':'clusterviewposttest',
            'description':'This cluster is created for testing view clustercreate post',
            'permission':'PO',
        }

        #this get request is used to get and append csrf token to our data payload
        response_get=self.client.get(url)
        data['csrfmiddlewaretoken']=response_get.context['csrf_token']
              
        response=self.client.post(url,data)
       
        
        self.assertEqual(response.status_code,302)
        self.assertEqual(ClusterModel.objects.last().code_name,"clusterviewposttest")
        
        
    
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
        url= reverse('cluster:clusterupdate',args=[self.testcluster.code_name])
        data={
            'cluster_name':'Test Cluster View Update',
            'code_name':'clusterupdatetest',
            'description':'This cluster is created for testing view clustercreate post',
            'permission':'PO',
        }

        #this get request is used to get and append csrf token to our data payload
        response_get=self.client.get(url)
        data['csrfmiddlewaretoken']=response_get.context['csrf_token']
              
        response=self.client.post(url,data)
        
        self.assertEqual(response.status_code,302)
        self.assertEqual(ClusterModel.objects.get(code_name=data['code_name']).cluster_name,data['cluster_name'])     
    
    def test_clusterdelete_view(self):
        template="cluster/cluster_delete.html"
        url= reverse('cluster:clusterdelete',args=[self.testcluster.code_name])
        data={}
        #[GET]response for template test
        response=self.client.get(url)
        
        self.assertTemplateUsed(response,template)   
        self.assertEqual(response.status_code,200)

        #[POST]response confirming delete + csrf token
        data['csrfmiddlewaretoken']=response.context['csrf_token']
        response_confirm=self.client.post(url,data)
        self.assertEqual(response_confirm.status_code,302)

    def test_notecreate_view_GET(self):
        template="cluster/note_create.html"
        url=reverse("cluster:notecreate")

        response=self.client.get(url)
        self.assertTemplateUsed(response,template)   
        self.assertEqual(response.status_code,200)

    def test_notedetail_view(self):
        template="cluster/note_detail.html"
        url=reverse("cluster:notedetail",args=[self.testcluster.code_name,self.testnote.code])

        response=self.client.get(url)
        self.assertTemplateUsed(response,template)   
        self.assertEqual(response.status_code,200)    
    
    def test_noteupdate_view_GET(self):
        template="cluster/note_update.html"
        url=reverse("cluster:noteupdate",args=[self.testcluster.code_name,self.testnote.code])

        response=self.client.get(url)
        self.assertTemplateUsed(response,template)   
        self.assertEqual(response.status_code,200)
    
    def test_notedelete_view(self):
        template="cluster/note_delete.html"
        url= reverse('cluster:notedelete',args=[self.testcluster.code_name,self.testnote.code])
        
        data={}

        #[GET]response for template test
        response=self.client.get(url)
        self.assertTemplateUsed(response,template)   
        self.assertEqual(response.status_code,200)
        #adding csrf token to request
        data['csrfmiddlewaretoken']=response.context['csrf_token']  
        #[POST]response confirming delete
        response_confirm=self.client.post(url,data)
        self.assertEqual(response_confirm.status_code,302)
    
    def test_clusternotecreate_view_GET(self):
        template="cluster/note_create.html"
        url=reverse("cluster:clusternotecreate",args=[self.testcluster.code_name])

        response=self.client.get(url)
        self.assertTemplateUsed(response,template)   
        self.assertEqual(response.status_code,200)
    
    def test_clusterownernoteupdate_view_GET(self):
        template="cluster/note_update.html"
        url=reverse("cluster:clusterownernoteupdate",args=[self.testcluster.code_name,self.testnote.code])

        response=self.client.get(url)
        self.assertTemplateUsed(response,template)   
        self.assertEqual(response.status_code,200)
    

    def tearDown(self):
        self.testcluster.delete()
        self.testnote.delete()


