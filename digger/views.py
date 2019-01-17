from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from decouple import config
import json, vk_api

# Create your views here.

secret_token = config('SECRET_TOKEN')
confirmation_token = config('CONFIRMATION_TOKEN')
token = config('TOKEN')

@csrf_exempt
def index(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        if (data['secret'] == secret_token):
            if (data['type'] == 'confirmation'):
                return HttpResponse(confirmation_token, content_type="text/plain", status=200)
            if (data['type'] == 'message_new'):
                vk_session = vk_api.VkApi(token=token,api_version=5.90)
                try:
                    vk_session.auth(token_only=True)
                except vk_api.AuthError as error_msg:
                    print(error_msg)
                    return
                vk = vk_api.get_api()
                user_id = data['object']['user_id']
                vk.masseges.send(access_token=token, user_id=str(user_id), message='Ответ бота')
                return HttpResponse('ok', content_type="text/plain", status=200)
    else:
        return HttpResponse('Сайт находится в разработке!')