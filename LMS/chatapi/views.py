
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import ChatSerializer, ContactSerializer
from .models import Chat, Message
from app.models import User
from django.db.models import Q
from datetime import datetime
# Create your views here.


class GetChats(APIView):
    serializer_class = ChatSerializer
    
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            userid = user.pk
            user_info = {
                        "id": userid,
                        "name": user.get_name(),
                        "avatar": user.avatar.name
                    }
            
            chats = ChatSerializer(user.chats.all(), many = True, context = {'userid': userid}).data
            return Response({'user_info': user_info, 'chats': chats}, status=status.HTTP_200_OK)
        
        return JsonResponse({'Unauthorized': 'Unauthorized'}, status = status.HTTP_401_UNAUTHORIZED)
        

class FriendSearch(APIView):

    def get_knowns(self, user):
        if user.user_type == '2':
            return User.objects.filter(Q(teacher__staffs__user = user) |
                                        Q(student__staffs__user = user))
        elif user.user_type == '3':
            return User.objects.filter(Q(teacher__students__user = user) 
                                | Q(staff__students__user = user))
        return User.objects.filter(Q(student__teachers__user = user) | Q(staff__hosts__user = user))
        # if user.user_type == '1':
        #     return user.teacher.students | user.teacher.staffs
        # elif user.user_type == '2':
        #     return user.staff.students | user.staff.hosts
        # return user.student.teachers | user.student.staffs

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if request.data.get('command') == 'kw':
                kw = request.data.get('kw')
                knownsQuery = self.get_knowns(user)
                q = knownsQuery.filter(Q(first_name__icontains = str(kw)) 
                                    | Q(last_name__icontains = str(kw))).all()
                
                contacts = ContactSerializer(q, many = True, context = {'userid': user.pk}).data
                return Response({'contacts': contacts}, status=status.HTTP_200_OK)
            else:
                id = request.data.get('info_id')
                is_chatid = request.data.get('isChatID')
                
                if is_chatid == True:
                    c = user.chats.filter(pk = int(id)).first()
                    if c:
                        c = ChatSerializer(Chat.objects.get(pk = int(id)), context={'userid': user.pk}).data
                        represent = c["represent"]
                        img_path = c["img_path"]
                        return Response({'represent': represent, "img_path": img_path}, 
                        status=status.HTTP_200_OK)
                else:
                    knownsQuery = self.get_knowns(user)
                    u = knownsQuery.filter(pk = int(id)).first()
                    if u:
                        return Response({'represent': u.get_name(), "img_path": u.avatar.name}, 
                        status=status.HTTP_200_OK)

                return Response({'Bad Request': "Not have access!"}, status=status.HTTP_403_FORBIDDEN)
        
        return JsonResponse({'Unauthorized': 'Unauthorized'}, status = status.HTTP_401_UNAUTHORIZED)


class FirstSend(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            data = request.data
            friend = User.objects.get(pk = int(data.get('friendID')))
            msg = data.get('content')
            
            c = Chat.objects.create()
            c.participants.set([friend, request.user])
            first_msg = Message.objects.create(author = request.user, chat_room = c,
                        content = msg)
            c.latestSent = datetime.now()
            c.save()

            new_chat = {
                "chatid": c.pk,
                "represent": friend.get_name(),
                "img_path": friend.avatar.name,
                "lastest_msg": msg
            }

            return Response({'new_chat': new_chat}, status=status.HTTP_200_OK)

        return JsonResponse({'Unauthorized': 'Unauthorized'}, status = status.HTTP_401_UNAUTHORIZED)