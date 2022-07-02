from django.test import TestCase,Client
from django.urls import reverse,resolve
from cluster.models import ClusterModel,NoteModel
from django.contrib.auth import get_user_model
from django.conf import settings
import os, random, string 
from cluster.forms import ClusterCreationForm,ClusterUpdateForm

User=get_user_model()

def dummy_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class TestForm(TestCase):
    def setUp(self):
        '''
        TEST_ASSETS_DIR contains external required content for test. 

        Test func naming: test_<name of form>_<test_condition>
        for ex if form is ClusterCreationForm which we are we testing for object creation
                    then:  test_ClusterCreationForm_object_creation
           

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
       
       #dimmy objects and data 
        self.testcluster=ClusterModel.objects.create(
            cluster_name="Test Cluster Form",
            code_name="testclusterform",
            owner=self.user,
            description="This cluster is created for testing form",
            permission="PO",
        )

        self.testnote=NoteModel.objects.create(
            author=self.user,
            title="Note for Testing Form",
            cover=os.path.join(self.TEST_ASSETS_DIR,'images/test_cover.jpeg'),
            is_verified=False,
            is_verified_updated=False,
            code="testnoteview",
            body="this is test for form",
            cluster=self.testcluster,
        )

        self.cluster_dummy_data={
                'cluster_name':'Cluster Dummy Data',
                'code_name':'dummycluster',
                'description':'This cluster is created for testing view clustercreate post',
                'permission':'PO',
            }
        self.note_dummy_data={
                "title":"Note Dummy Data",
                "code":"dummynote",
                # "cover":,
                "body":"This is dummy data used for testing forms.",
                "cluster":self.testcluster,
                }
        
    def test_ClusterCreationForm_object_creation_via_url(self):
            url=reverse('cluster:clustercreate')
            data=self.cluster_dummy_data
            
            get_response=self.client.get(url)
            data['csrfmiddlewaretoken']=get_response.context['csrf_token']
            post_response=self.client.post(url,data=data)

            self.assertEqual(post_response.status_code,302)

    def test_ClusterCreationForm_code_name_length_field_validation_test(self):
            url=reverse('cluster:clustercreate')
            #Testing length validation of code_name
            bad_data=self.cluster_dummy_data
            bad_data['code_name']='toolongcodenameforcodenamefield'          
            get_response=self.client.get(url)
            bad_data['csrfmiddlewaretoken']=get_response.context['csrf_token']
            post_response=self.client.post(url,data=bad_data)
           
            self.assertContains(post_response,'Ensure this value has at most 20 characters (it has 31)')

    def test_ClusterCreationForm_code_name_alphanumeric_validation_test(self):
            #alphanumeric code_name test
            url=reverse('cluster:clustercreate')
            bad_data=self.cluster_dummy_data
            bad_data['code_name']='th!s!sn0t@ll0wed'          
            get_response=self.client.get(url)
            bad_data['csrfmiddlewaretoken']=get_response.context['csrf_token']
            post_response=self.client.post(url,data=bad_data)
           
            self.assertContains(post_response,'Sorry , you can only have alphanumeric in Cluster code name')


    def tearDown(self):
            self.testcluster.delete()
            self.testnote.delete()
              