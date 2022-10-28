
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chat, Message
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Message)
def sendNotice(sender, instance, created, **kwargs):
    if created:
        author = instance.author
        chat_room = instance.chat_room
        room_name = chat_room.roomName
        is_group_chat = room_name and room_name != ''
        represent = room_name if is_group_chat == True else author.get_name()
        img_path = 'media/course_pic/default.png' if is_group_chat == True else author.avatar.name

        friend_name = ''
        friend_avatar = ''
        if is_group_chat == False:
            friend = chat_room.participants.exclude(pk = author.pk).first()
            friend_name = friend.get_name()
            friend_avatar = friend.avatar.name

        msg = {
            'command': 'notices',
            'id': instance.pk,
            'author': {
                'id': author.pk,
                'name': author.get_name(),
                'avatar': author.avatar.name
            },
            'content': instance.content,
            'timestamp': str(instance.timestamp),
            'chat': {
                'chatid': instance.chat_room.pk,
                'represent': represent,
                'img_path': img_path,
                'lastest_msg': instance.content
            },
            'others': {
                'is_group_chat': is_group_chat,
                'friend_name': friend_name,
                'friend_avatar': friend_avatar
            }
        }

        channel_layer = get_channel_layer()
        for user in chat_room.participants.all():
            async_to_sync(channel_layer.group_send)(
                'notice_%s' % user.pk, 
                {
                    'type': 'send_notice',
                    'message': msg
                }
            )