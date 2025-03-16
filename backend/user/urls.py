from django.urls import path, include

from user.views import TestView, JwtTestView, LoginView, RegisterView, GetSession, Chat

urlpatterns = [
    path('test',TestView.as_view(), name='test'), # 用户模块
    path('jwt_test', JwtTestView.as_view(), name='jwt_test'),
    path('login', LoginView.as_view(), name='login'), # 登录
    path('register', RegisterView.as_view(), name='register'), # 注册
    path("session",GetSession.as_view(),name="session"),
    path("chat",Chat.as_view(),name="chat")
]
