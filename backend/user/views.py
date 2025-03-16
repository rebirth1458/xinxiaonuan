import json
from datetime import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from django.views import View
from flask import session
from langchain_community.tools.edenai.image_objectdetection import ObjectDetectionInput
from rest_framework_jwt.settings import api_settings
from django.utils import timezone
from sqlalchemy.sql.sqltypes import NULLTYPE

from util.extract_ChatMessage import extract_ChatMessage, result
from user.models import User, UserSerializer, UserSession, Session
from util.ChatModel import chitchat

# Create your views here.
class TestView(View):
    def get(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != None and token != '':
            userList_obj=User.objects.all()
            userList_dict=userList_obj.values()
            userList = list(userList_dict)
            return JsonResponse({'code': 200, 'info': '测试！', 'data': userList})
        else:
            return JsonResponse({'code': 401, 'info': '没有访问权限！'})

class JwtTestView(View):
    def get(self, request):
        user=User.objects.get(username='admin',password='123456')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return JsonResponse({'code': 200, 'token': token})

class LoginView(View):
    def post(self, request):
        username=request.GET.get('username')
        password=request.GET.get('password')
        try:
            user=User.objects.get(username=username,password=password)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
        except Exception as e:
            return JsonResponse({'code': 500, 'info': '用户名或密码错误！'})
        return JsonResponse({'code': 200, 'token': token,'user': UserSerializer(user).data})

class RegisterView(View):
    def post(self, request):
        data=request.POST

        if not all(k in data for k in ('username', 'password')):
            return JsonResponse({"code": 400,"info": "缺少用户名或密码"})
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.create_time=timezone.now()
            user.update_time=timezone.now()
            user.save()

            return JsonResponse({'code': 200,'info': '注册成功'})
        else:
            return JsonResponse({'code': 500,'info': '注册失败'})

class GetSession(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        user_sessions= UserSession.objects.filter(user_id=user_id)
        chat_data_dict = {}
        for session in user_sessions:
            sessions = Session.objects.filter(session_id=session.session_id)
            for data in sessions:
                if data.session_id not in chat_data_dict:
                    chat_data_dict[data.session_id] = {
                        'session_id': data.session_id,
                        'session_data': []
                    }
                # 假设data.message是一个JSON字符串，需要解析以获取content和type
                message_content = extract_ChatMessage(data.message)
                chat_data_dict[data.session_id]['session_data'].append(message_content)

        # 将字典转换为列表格式
        chat_data = list(chat_data_dict.values())
        return JsonResponse({'code': 200,'info': '获取成功',"chat_data":chat_data})
    def delete(self,request):
        data=json.loads(request.body)
        user_id=data.get('user_id')
        session_id = data.get("session_id")
        user_session = UserSession.objects.get(session_id=session_id)
        user_session.delete()
        session = Session.objects.filter(session_id=session_id)
        session.delete()
        return JsonResponse({'code':200,"info":'删除成功'})
class Chat(View):
    def post(self, request):
        data=json.loads(request.body)
        input=data.get("input")
        session_id=data.get("session_id")
        user_id = data.get("user_id")
        if session_id=="new":
            max_id=Session.objects.aggregate(max_id=Max('session_id'))['max_id']#获取当前最大的session_id
            if max_id:
                session_id=max_id+1
            else:
                session_id=1
            user_session = UserSession(session_id=session_id, user_id=user_id)
            user_session.save()
            result = chitchat(session_id, input)
        else:
            result = chitchat(session_id, input)
        return JsonResponse({'code': 200,'info': '获取成功',"result":result})

