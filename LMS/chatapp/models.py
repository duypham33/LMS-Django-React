from ast import mod
from django.db import models

# Create your models here.

class Contact(models.Model):
    user = models.ForeignKey('app.User', related_name='friends', 
                        on_delete = models.SET_NULL, null=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username



class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE, null = True)
    content = models.TextField(max_length = 500, blank = False, null=False)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Message id: {self.pk}, Author: {self.contact.user.get_name()}'

    class Meta:
        ordering = ["-pk"]   #Same -timestamp


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def last_10_messages(self):
        return self.messages.order_by('-pk').all()[:10]   #Same -timestamp

    def __str__(self):
        return "Chat-id<{}>".format(self.pk)