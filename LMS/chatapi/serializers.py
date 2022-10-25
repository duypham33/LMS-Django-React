
from rest_framework import serializers
from .models import Chat



class ChatSerializer(serializers.ModelSerializer):
    represent = serializers.SerializerMethodField()
    img_path = serializers.SerializerMethodField()
    lastest_msg = serializers.SerializerMethodField()
    
    class Meta:
        model = Chat
        fields = ['chatid', 'represent', 'img_path', 'lastest_msg']

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