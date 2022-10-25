
from django.db import models


# Create your models here.

class Chat(models.Model):
    chatID = models.SmallAutoField(primary_key = True)
    participants = models.ManyToManyField('app.User', related_name='chats')
    
    def last_10_messages(self):
        return self.messages.order_by('-pk').all()[:10]   #Same -timestamp

    def __str__(self):
        return f"Chat-id {self.chatID}"


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


