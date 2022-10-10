
from django.test import Client
from django.urls import reverse
from app.tests import testbase

class TestViews(testbase.TestBase):
    def setUp(self):
        self.client = Client()

        self.login_url = reverse('app:login')
        self.logout_url = reverse('app:logout')
        self.profile_url = reverse('app:profile')
        
        super().setUp()
    

    # def test_login_GET(self):
    #     response = self.client.get(self.login_url)
    #     #print(response)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')

    # def test_login_POST_with_username(self):
    #     user = self.create_user('1')
    #     response = self.client.post(self.login_url, {
    #         "account": user.username,
    #         "password": self.user["password"] #Since user.password was hashed
    #     })
    #     self.assertEquals(response.status_code, 302)
        

    # def test_login_POST_with_email(self):
    #     user = self.create_user('1')
    #     response = self.client.post(self.login_url, {
    #         "account": user.email,
    #         "password": self.user["password"] #Since user.password was hashed
    #     })
    #     self.assertEquals(response.status_code, 302)

    # def test_login_POST_wrong(self):
    #     user = self.create_user('1')
    #     response = self.client.post(self.login_url, {
    #         "account": user.email,
    #         "password": "wrong" #Wrong password
    #     })

    #     msgs = self.msg(response)

    #     self.assertIn('Your username, email, or password is incorrect!', msgs)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')


    # def test_login_logout(self):
    #     user = self.create_user('1')
    #     #Login
    #     response = self.client.post(self.login_url, {
    #         "account": user.email,
    #         "password": self.user["password"] #Since user.password was hashed
    #     })

    #     self.assertEquals(response.status_code, 302)

    #     #Logout
    #     response = self.client.get(self.logout_url)

    #     msgs = self.msg(response)

    #     self.assertIn('You logged out!', msgs)
    #     self.assertEquals(response.status_code, 302)


    # def test_profile_not_login_yet(self):
    #     response = self.client.get(self.profile_url)
    #     self.assertEquals(response.status_code, 302)


    # def test_profile_GET(self):
    #     user = self.create_user('1')
    #     #Login
    #     response = self.client.post(self.login_url, {
    #         "account": user.email,
    #         "password": self.user["password"] #Since user.password was hashed
    #     })

    #     self.assertEquals(response.status_code, 302)

    #     #Access profile page
    #     response = self.client.get(self.profile_url)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'profile.html')


    # def test_profile_POST(self):
    #     user = self.create_user('1')
    #     avatar = user.avatar
    #     #Login
    #     response = self.client.post(self.login_url, {
    #         "account": user.email,
    #         "password": self.user["password"] #Since user.password was hashed
    #     })

    #     self.assertEquals(response.status_code, 302)

    #     #Access profile page
    #     response = self.client.post(self.profile_url, {
    #         "avatar": '',
    #         "firstname": "Test",
    #         "lastname": "Name",
    #     })
    #     user.refresh_from_db()
    #     msgs = self.msg(response)
        
    #     self.assertIn('Your profile is updated!', msgs)
    #     self.assertEquals(response.status_code, 302)

    #     u = User.objects.get(id = 1)
    #     self.assertEquals(user.first_name, "Test")
    #     self.assertEquals(user.last_name, "Name")
    #     self.assertEquals(u.avatar, avatar)