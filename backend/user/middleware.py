from django.http import HttpResponse
from django.middleware.csrf import InvalidTokenFormat
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework.settings import api_settings


class JwtAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        white_list=['/user/login','/user/register','/user/session','/user/chat']
        path=request.path
        if path not in white_list:
            print("进行token验证")
            token = request.META.get('HTTP_AUTHORIZATION')
            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                return HttpResponse("token过期")
            except InvalidTokenError:
                return HttpResponse("token无效")
            except PyJWTError:
                return HttpResponse("token验证异常")
        else:
            print("白名单，不需要验证")
            return None