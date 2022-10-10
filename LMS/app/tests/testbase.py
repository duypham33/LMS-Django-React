
from django.test import TestCase
from app.models import User
from django.contrib.messages import get_messages

class TestBase(TestCase):
    def setUp(self):
        self.user = {
            "username": "test name",
            "email": "test@gmail.com",
            "password": "123456"
        }
        super().setUp()

    def create_user(self, user_type):
        user = User.objects.create(username=self.user["username"], email=self.user["email"], 
        user_type = str(user_type), password = self.user["password"])

        #Have reason, there are two same users but different passwords (one hashed by signal, other not)
        u = User.objects.get(username = user.username)  
        u.set_password(self.user["password"])
        u.save()

        return user

    def msg(self, response):
        msg_storage = get_messages(response.wsgi_request)
        return list(map((lambda x: x.message), msg_storage))