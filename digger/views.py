from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from decouple import config
import json
import vk_api


from .models import Player, Stock, Build, Forge, Army, War

from .function.build import *
from .function.place import *
from .function.action import *
from .function.menu import *
from .function.war import *

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
                player = check_models(player=player)
                if reg == 'new':
                    player.place = 'reg'
                    player.save()
                    vk.messages.send(
                        access_token=token,
                        user_id=str(user_id),
                        message='Добро пожаловать в Cave World!\nВведите свой ник:',
                        keyboard=get_keyboard(player=player),
                        random_id=get_random_id()
                    )
                    return HttpResponse('ok', content_type="text/plain", status=200)
                elif reg == 'old':
                    if player.place == 'reg':
                        nick = data['object']['text']
                        player.nickname = nick
                        player.place = 'cave'
                        player.save()
                        message = 'Ваш ник - ' + player.nickname
                        vk.messages.send(
                            access_token=token,
                            user_id=str(user_id),
                            message=message,
                            keyboard=get_keyboard(player=player),
                            random_id=get_random_id()
                        )
                    elif 'payload' in data['object']:
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
        army = Army.objects.create(user_id=user_id)
        war = War.objects.create(user_id=user_id)
        forge = Forge.objects.create(user_id=user_id)
        stock = Stock.objects.create(user_id=user_id)
        build = Build.objects.create(user_id=user_id)
        player = Player.objects.create(user_id=user_id,
                                       stock=stock,
                                       build=build,
                                       forge=forge,
                                       army=army,
                                       war=war,
                                       )
        user = vk.users.get(user_ids=str(user_id))
        user = user[0]
        if user['first_name']:
            player.first_name = user['first_name']
        if user['last_name']:
            player.last_name = user['last_name']
        player.save()
        return 'new'
    return 'old'


def check_models(player):
    if not player.forge:
        forge = Forge.objects.create(user_id=player.user_id)
        player.forge = forge
        player.forge.save()
    if not player.stock:
        stock = Stock.objects.create(user_id=player.user_id)
        player.stock = stock
        player.stock.save()
    if not player.build:
        build = Build.objects.create(user_id=player.user_id)
        player.build = build
        player.build.save()
    if not player.army:
        army = Army.objects.create(user_id=player.user_id)
        player.army = army
        player.army.save()
    if not player.war:
        war = War.objects.create(user_id=player.user_id)
        player.war = war
        player.war.save()
    return player


def action(vk, command, player, action_time):

    # Инфо

    if command.lower() == 'profile':
        profile(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'bonus':
        bonus(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'stock':
        stock(vk=vk, player=player, token=token)
    elif command.lower() == 'army':
        army(vk=vk, player=player, token=token)

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
    elif command.lower() == 'build_gate':
        build_gate(vk=vk, player=player, token=token)

    # Кузница

    elif command.lower() == 'forge':
        forge(vk=vk, player=player, token=token)
    elif command.lower() == 'forge_pickaxe':
        forge_pickaxe(vk=vk, player=player, token=token)
    elif command.lower() == 'forge_pickaxe_info':
        forge_pickaxe_info(vk=vk, player=player, token=token)
    elif command.lower() == 'craft_pickaxe_stone':
        craft_pickaxe_stone(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'craft_pickaxe_iron':
        craft_pickaxe_iron(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'craft_pickaxe_diamond':
        craft_pickaxe_diamond(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'forge_kit':
        forge_kit(vk=vk, player=player, token=token)
    elif command.lower() == 'forge_kit_info':
        forge_kit_info(vk=vk, player=player, token=token)
    elif command.lower() == 'craft_sword':
        craft_sword(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'craft_bow':
        craft_bow(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'craft_orb':
        craft_orb(vk=vk, player=player, action_time=action_time, token=token)

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

    # Таверна

    elif command.lower() == 'tavern':
        tavern(vk=vk, player=player, token=token)
    elif command.lower() == 'buy_warrior':
        buy_warrior(vk=vk, player=player, token=token)
    elif command.lower() == 'buy_archer':
        buy_archer(vk=vk, player=player, token=token)
    elif command.lower() == 'buy_wizard':
        buy_wizard(vk=vk, player=player, token=token)

    # Земли

    elif command.lower() == 'land':
        land(vk=vk, player=player, token=token)
    elif command.lower() == 'cut_wood':
        cut_wood(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'land_build':
        land_build(vk=vk, player=player, token=token)
    elif command.lower() == 'build_tower':
        build_tower(vk=vk, player=player, token=token)
    elif command.lower() == 'build_wall':
        build_wall(vk=vk, player=player, token=token)

    # Война
    elif command.lower() == 'war':
        war(vk=vk, player=player, token=token)
    elif command.lower() == 'find_enemy':
        find_enemy(vk=vk, player=player, action_time=action_time, token=token)
    elif command.lower() == 'attack':
        attack(vk=vk, player=player, action_time=action_time, token=token)
