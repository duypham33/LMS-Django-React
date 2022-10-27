
from rest_framework import serializers
from .models import Chat
from django.db.models import Q
from app.models import User

class ChatSerializer(serializers.ModelSerializer):
    represent = serializers.SerializerMethodField()
    img_path = serializers.SerializerMethodField()
    lastest_msg = serializers.SerializerMethodField()
    
    class Meta:
        model = Chat
        fields = ['chatid', 'represent', 'img_path', 'lastest_msg']

    # def get_chatid(self, obj):
    #     if "friendid" in self.context:
    #         userid = self.context.get("userid")
    #         friendid = self.context.get("friendid")
    #         if Chat.objects.filter(Q(participants__pk = userid) & Q(participants__pk = friendid)).first():
    #             return 

    def get_represent(self, obj):
        if obj.participants: 
            if obj.participants.count() > 2:
                return obj.roomName
            
            friend = obj.participants.exclude(pk = self.context.get("userid")).first()
            return friend.get_name()


    def get_img_path(self, obj):
        if obj.participants: 
            if obj.participants.count() > 2:
                return 'media/course_pic/default.png'
            
            friend = obj.participants.exclude(pk =  self.context.get("userid")).first()
            return friend.avatar.name

    def get_lastest_msg(self, obj):
        if obj.messages and obj.messages.count() > 0:
            msg = obj.messages.first()
            return msg.content
        return ''


    # def create(self, validate_data):
    #     userid = validate_data.pop("userid", None)
    #     self.userid = userid
    #     return super().create(validate_data)


class ContactSerializer(serializers.ModelSerializer):
    chatid = serializers.SerializerMethodField()
    represent = serializers.SerializerMethodField()
    img_path = serializers.SerializerMethodField()
    lastest_msg = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['chatid', 'represent', 'img_path', 'lastest_msg']

    def find_chat(self, obj):
        userid = self.context.get("userid")
        c = Chat.objects.filter(participants__pk = userid).filter(participants__pk = obj.pk)
        return c.filter(roomName = None).first()

    def get_chatid(self, obj):
        chat = self.find_chat(obj)
        return chat.chatid if chat else f'0_{obj.pk}'

    def get_represent(self, obj):
        return obj.get_name()

    def get_img_path(self, obj):
        return obj.avatar.name
    
    def get_lastest_msg(self, obj):
        chat = self.find_chat(obj)
        if chat and chat.messages and chat.messages.count() > 0:
            return chat.messages.first().content

        return ''
        