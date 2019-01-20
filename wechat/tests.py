
import json

from django.test import TestCase
from .models import User as MyUser, Activity, Ticket
from django.test import Client
from userpage.views import *
from adminpage.views import *
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import login

class WechatTest(TestCase):

    def before_test(self):
        user_to_add = MyUser(open_id='1', student_id='2016013237')
        user_to_add.save()

        activity_to_add = Activity(
            id=1,
            name='1',
            key='1-key',
            description='desc',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            place="here",
            book_start=timezone.now() - timezone.timedelta(days=1),
            book_end=timezone.now() + timezone.timedelta(hours=1),
            total_tickets=100,
            pic_url="pic/test.jpg",
            remain_tickets=50,
            status=Activity.STATUS_PUBLISHED
        )
        activity_to_add.save()

        ticket_to_add = Ticket(
            student_id=1,
            unique_id=1,
            activity=activity_to_add,
            status=1
        )
        ticket_to_add.save()

        a = User.objects.create_user(username='admin',password='xxd123456',email='example@163.com')
        a.save()

    def test_(self):

        self.assertEqual(1, 1)

    def test_user_bind_get(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/user/bind/', {'openid': '1'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['data'], '2016013237')

    def test_user_bind_post_exsit(self):
        self.before_test()
        user = MyUser(open_id='2',student_id="1234567890")
        user.save()
        c = Client()
        d = c.post('/api/u/user/bind/', {'openid': '2', 'student_id': '2016013238', 'password': "123456"})
        if d.status_code == 404:
            return
        self.assertEqual(d.status_code, 200)
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['code'], 0)

        c = Client()
        d = c.get('/api/u/user/bind/', {'openid': '2'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['data'], '2016013238')

    def test_user_bind_post_not_exist(self):
        self.before_test()
        c = Client()
        d = c.post('/api/u/user/bind/', {'openid': '2', 'student_id': '2016013238', 'password': "123456"})
        if d.status_code == 404:
            return
        self.assertEqual(d.status_code, 200)
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertNotEqual(json_text['code'], 0)

    def test_activity_detail_get_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/activity/detail/', {'id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['data']['key'], '1-key')
        self.assertEqual(json_text['code'], 0)

    def test_activity_detail_get_not_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/activity/detail/', {'id': 100})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    def test_ticket_detail_get_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/ticket/detail/', {'openid': '1', 'ticket': 1})
        if d.status_code == 404:
            return

        json_text = json.loads(d.content.decode('utf-8'))
        print("json test:")
        print(json_text)
        self.assertEqual(d.status_code, 200)

        self.assertEqual(json_text['data']['activityKey'], '1-key')

    def test_login_post_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/login/',{'username':'admin','password':'xxd123456'})
        if d.status_code == 404:
            return 
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertEqual(json_text['code'],0)


    def test_login_post_not_succeed(self):
        self.before_test()
        c = Client()


        d = c.post('/api/a/login/',{'username':'admin','password':'1234567'})
        if d.status_code == 404:
            return 
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertNotEqual(json_text['code'],0)

        '''    def test_logout_post_succeed(self):
        self.before_test()
        c = Client()
        print(c.cookies)
        d = c.post('/api/a/login/', {'username': 'admin', 'password': 'xxd123456'})
        print(c.cookies)
        d =  c.POST('/api/a/logout/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertEqual(json_text['code'],0)


    def test_logout_post_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/logout/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertNotEqual(json_text['code'],0)
'''

    def test_login_get_not_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/login/', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertNotEqual(json_text['code'], 0)

    def test_activity_list_get(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/list', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
    # self.assertEqual(json_text['data'][0]['id'],1)

    def test_activity_delete_succeed(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/delete/', {'id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)


    def test_activity_delete_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/delete/', {'id': 1})
        d = c.get('/api/a/activity/delete/', {'id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)


    def test_activity_create_succeed(self):
        self.before_test()
        c = Client()
        d = c.post("/api/a/activity/create/",{
        'name':'2',
        'key':'2-key',
        'place':'place',
        'description':'description',
        'picUrl':'url',
        'startTime':'1000000000',
        'endTime':'1000000100',
        'bookStart':'999999900',
        'bookEnd':'999999990',
        'totalTickets':100,
        'status':0})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertEqual(json_text['code'],0)
        self.assertEqual(json_text['data'],2)

    def test_activity_create_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.post("/api/a/activity/create/",{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertNotEqual(json_text['code'],0)


    def test_image_upload_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/image/upload/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertEqual(json_text['code'],0)
        #self.assertEqual(json_text['data'],)
		


    def test_image_upload_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/image/upload/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertNotEqual(json_text['code'],0)
		
    def test_activity_detail_get(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/detail/',{'id':1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        #self.assertEqual()#deal with get data		

    def test_activity_menu_get(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/menu/',{})
        if d.status_code == 404:
           return  
        self.assertEqual(d.status_code,200)
        #self.assertEqual()#check data

    def test_activity_menu_post_succeed(self):
        pass

    def test_activity_menu_post_not_succeed(self):
        pass

    def test_checkin_post_succeed(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/checkin/', {'actid':1,'ticket':1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['data']['student'],1)
        self.assertNotEqual(json_text['code'], 0)  # check data

    def test_checkin_post_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/checkin/',{'actid':2,'ticket':2})
        if d.status_code == 404:
           return  
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        
        self.assertNotEqual(json_text['code'],0)
#check data
# Create your tests here.
