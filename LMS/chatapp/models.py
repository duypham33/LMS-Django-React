from django.db import models

# Create your models here.

class Message(models.Model):
    author = models.ForeignKey('app.User', related_name='messages', 
                        on_delete = models.SET_NULL, null=True)
    content = models.TextField(max_length = 500, blank = False, null=False)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Message id: {self.pk}, Author: {self.author.get_name()}'

    class Meta:
        ordering = ["-pk"]   #Same -timestamp