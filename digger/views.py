from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from decouple import config
import json, vk_api
import random

from .models import Player

# Create your views here.

secret_token = config('SECRET_TOKEN')
confirmation_token = config('CONFIRMATION_TOKEN')
token = config('TOKEN')


def get_random_id():
    """ Get random int32 number (signed) """
    return random.getrandbits(31) * random.choice([-1, 1])


@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if data['secret'] == secret_token:
            if data['type'] == 'confirmation':
                return HttpResponse(confirmation_token, content_type="text/plain", status=200)
            if data['type'] == 'message_new':
                vk_session = vk_api.VkApi(token=token)
                vk = vk_session.get_api()
                user_id = data['object']['from_id']
                reg = register(vk=vk, user_id=user_id)
                if reg == 'new':
                    vk.messages.send(
                        access_token=token,
                        user_id=str(user_id),
                        message='Добро пожаловать в Cave World!',
                        random_id=get_random_id()
                    )
                    return HttpResponse('ok', content_type="text/plain", status=200)
                elif reg == 'old':
                    command(vk=vk, text=data['object']['text'], user_id=user_id)
                    return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('Ошибка - неверный type')
        else:
            return HttpResponse('Ошибка - неверный secret key')
    else:
        return HttpResponse('Сайт находится в разработке!')


def register(vk, user_id):
    if not Player.objects.filter(user_id=user_id).exists():
        player = Player.objects.create(user_id=user_id)
        user = vk.users.get(user_ids=str(user_id))
        user = user[0]
        if user['first_name']:
            player.first_name = user['first_name']
        if user['last_name']:
            player.last_name = user['last_name']
            player.save()
        return 'new'
    return 'old'


def command(vk, text, user_id):
    if text.lower() == 'профиль':
        profile(vk=vk, user_id=user_id)



def profile(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    message = 'Имя: ' + player.first_name + "\n" + 'Фамилия: ' + player.last_name + "\n" + 'ID: ' + str(player.user_id)
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        message=message,
        random_id=get_random_id()
    )
