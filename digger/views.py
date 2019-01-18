from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from decouple import config
import json, vk_api
import random

# Create your views here.

secret_token = config('SECRET_TOKEN')
confirmation_token = config('CONFIRMATION_TOKEN')
token = config('TOKEN')

def get_random_id():
    """ Get random int32 number (signed) """
    return random.getrandbits(31) * random.choice([-1, 1])

@csrf_exempt
def index(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode("utf-8"))
        if (data['secret'] == secret_token):
            if (data['type'] == 'confirmation'):
                return HttpResponse(confirmation_token, content_type="text/plain", status=200)
            if (data['type'] == 'message_new'):
                vk_session = vk_api.VkApi(token=token)
                vk = vk_session.get_api()
                '''
                try:
                    vk_session.auth(token_only=True)
                except vk_api.AuthError as error_msg:
                    print(error_msg)
                    return HttpResponse(error_msg , content_type="text/plain", status=200)
                '''
                user_id = data['object']['from_id']
                vk.messages.send(access_token=token, user_id=str(user_id), message='Ответ бота', random_id = get_random_id())
                return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('Ошибка - неверный type')
        else:
            return HttpResponse('Ошибка - неверный secret key')
    else:
        return HttpResponse('Сайт находится в разработке!')