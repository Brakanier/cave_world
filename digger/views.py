from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from decouple import config
import json
import vk_api


from .models import Player, Stock, Build, Forge

from .function.build import *
from .function.place import *
from .function.action import *
from .function.menu import *

# Create your views here.

secret_token = config('SECRET_TOKEN')
confirmation_token = config('CONFIRMATION_TOKEN')
token = config('TOKEN')


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
                player = Player.objects.get(user_id=user_id)
                if reg == 'new':
                    vk.messages.send(
                        access_token=token,
                        user_id=str(user_id),
                        message='Добро пожаловать в Cave World!',
                        keyboard=get_keyboard(player=player),
                        random_id=get_random_id()
                    )
                    return HttpResponse('ok', content_type="text/plain", status=200)
                elif reg == 'old':
                    if 'payload' in data['object']:
                        payload = json.loads(data['object']['payload'])
                        command = payload['command']
                        action_time = data['object']['date']
                        action(vk=vk, command=command, player=player, action_time=action_time)
                    else:
                        text = data['object']['text']
                        text = text.split()
                        if len(text):
                            s = text[0]
                            if s.lower() == 'ник':
                                player.nickname = text[1]
                                player.save()
                                message = 'Ваш ник - ' + player.nickname
                                vk.messages.send(
                                    access_token=token,
                                    user_id=str(user_id),
                                    message=message,
                                    keyboard=get_keyboard(player=player),
                                    random_id=get_random_id()
                                )
                            else:
                                vk.messages.send(
                                    access_token=token,
                                    user_id=str(user_id),
                                    message='Используйте кнопки для управления!',
                                    keyboard=get_keyboard(player=player),
                                    random_id=get_random_id()
                                )
                    return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('Ошибка - неверный type')
        else:
            return HttpResponse('Ошибка - неверный secret key')
    else:
        return HttpResponse('Сайт находится в разработке!')


def register(vk, user_id):
    if not Player.objects.filter(user_id=user_id).exists():
        forge = Forge.objects.create(user_id=user_id)
        stock = Stock.objects.create(user_id=user_id)
        build = Build.objects.create(user_id=user_id)
        player = Player.objects.create(user_id=user_id, stock=stock, build=build, forge=forge)
        user = vk.users.get(user_ids=str(user_id))
        user = user[0]
        if user['first_name']:
            player.first_name = user['first_name']
        if user['last_name']:
            player.last_name = user['last_name']
        player.save()
        return 'new'
    return 'old'


def action(vk, command, player, action_time):

    # Инфо

    if command.lower() == 'profile':
        profile(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'stock':
        stock(vk=vk, player=player, token=token)

    # Подземелье

    elif command.lower() == 'cave':
        cave(vk=vk, player=player, token=token)
    elif command.lower() == 'cave_build':
        cave_build(vk=vk, player=player, token=token)
    elif command.lower() == 'build_forge':
        build_forge(vk=vk, player=player, token=token)
    elif command.lower() == 'build_tavern':
        build_tavern(vk=vk, player=player, token=token)
    elif command.lower() == 'build_stock':
        build_stock(vk=vk, player=player, token=token)

    # Кузница

    elif command.lower() == 'forge':
        forge(vk=vk, player=player, token=token)
    elif command.lower() == 'forge_pickaxe':
        forge_pickaxe(vk=vk, player=player, token=token)
    elif command.lower() == 'forge_kit':
        forge_kit(vk=vk, player=player, token=token)

    # Шахта

    elif command.lower() == 'mine':
        mine(vk=vk, player=player, token=token)
    elif command.lower() == 'dig_stone':
        dig_stone(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'dig_iron':
        dig_iron(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'dig_gold':
        dig_gold(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'dig_diamond':
        dig_diamond(vk=vk, player=player, action_time=action_time, token=token)
