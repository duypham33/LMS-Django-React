
from django.db import models


# Create your models here.

class Chat(models.Model):
    chatid = models.AutoField(primary_key = True)
    participants = models.ManyToManyField('app.User', related_name='chats')
    roomName = models.CharField(max_length = 100, null = True, blank = True)
    latestSent = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return f"Chat-id {self.chatid}"

    def last_10_messages(self):
        return self.messages.order_by('-pk').all()[:9]   #Same -timestamp
    
    class Meta:
         ordering = ["-latestSent"]  


class Message(models.Model):
    author = models.ForeignKey('app.User', related_name='messages',
                     on_delete = models.SET_NULL, null=True)
    chat_room = models.ForeignKey('Chat', related_name='messages', on_delete = models.CASCADE)
    content = models.TextField(max_length = 500, blank = False, null = False)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
         return f'Message id: {self.pk}, Author: {self.author.get_name()}'

    class Meta:
         ordering = ["-pk"]   #Same -timestamp



