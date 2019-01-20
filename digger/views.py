from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from decouple import config
import json
import vk_api
import random
import time
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


from .models import Player, Stock, Build

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
                        action(vk=vk, command=command, user_id=user_id, action_time=action_time)
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
        stock = Stock.objects.create(user_id=user_id)
        build = Build.objects.create(user_id=user_id)
        player = Player.objects.create(user_id=user_id, stock=stock, build=build)
        user = vk.users.get(user_ids=str(user_id))
        user = user[0]
        if user['first_name']:
            player.first_name = user['first_name']
        if user['last_name']:
            player.last_name = user['last_name']
        player.save()
        return 'new'
    return 'old'


def action(vk, command, user_id, action_time):
    if command.lower() == 'profile':
        profile(vk=vk, user_id=user_id)
    elif command.lower() == 'stock':
        stock(vk=vk, user_id=user_id)
    elif command.lower() == 'mine':
        mine(vk=vk, user_id=user_id)
    elif command.lower() == 'cave':
        cave(vk=vk, user_id=user_id)
    elif command.lower() == 'cave_build':
        cave_build(vk=vk, user_id=user_id)
    elif command.lower() == 'build_forge':
        build_forge(vk=vk, user_id=user_id)
    elif command.lower() == 'build_tavern':
        build_tavern(vk=vk,user_id=user_id)
    elif command.lower() == 'dig':
        dig(vk=vk, user_id=user_id, action_time=action_time)


def profile(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    message = 'Имя: ' + player.first_name + "\n" + \
              'Фамилия: ' + player.last_name + "\n" + \
              'ID: ' + str(player.user_id) + "\n" + \
              'Местоположение: ' + player.place
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def stock(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    stock = player.stock
    message = 'Склад - ' + str(stock.lvl) + ' ур.' + '\n' + \
              'Камень: ' + str(stock.stone) + '/' + str(stock.stone_max) + '\n' + \
              'Железная руда: ' + str(stock.ore_iron) + '/' + str(stock.ore_iron_max) + '\n' + \
              'Золотая руда: ' + str(stock.ore_gold) + '/' + str(stock.ore_gold_max) + '\n' + \
              'Слитки железа: ' + str(stock.ingot_iron) + '/' + str(stock.ingot_iron_max) + '\n' + \
              'Слитки золота: ' + str(stock.ingot_gold) + '/' + str(stock.ingot_gold_max) + '\n' + \
              'Черепа: ' + str(stock.skull) + ' 💀'
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def mine(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    if player.place == 'mine':
        message = 'Вы уже в шахте'
    else:
        player.place = 'mine'
        player.save()
        message = 'Вы спустили в шахту'
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def cave(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    if player.place == 'cave':
        message = 'Вы уже в подземелье'
    else:
        player.place = 'cave'
        player.save()
        message = 'Вы вернулись в подземелье'
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def cave_build(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    if player.place == 'cave_build':
        message = 'Выберите постройку'
    else:
        player.place = 'cave_build'
        player.save()
        message = 'Выберите здание для строительства или улучшения'
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_forge(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    if not player.build.forge:
        player.build.forge = True
        player.build.save()
        message = 'Кузница построена'
    else:
        message = 'У вас уже есть Кузница'
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_tavern(vk, user_id):
    player = Player.objects.get(user_id=user_id)
    if not player.build.tavern:
        player.build.tavern = True
        player.build.save()
        message = 'Таверна построена'
    else:
        message = 'У вас уже есть Таверна'
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )





def get_keyboard(player):
    keyboard = VkKeyboard()
    if player.place == 'cave':
        if player.build.lift:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('Шахта', color=VkKeyboardColor.PRIMARY, payload={"command": "mine"})
        keyboard.add_line()
        keyboard.add_button('Здания', color=VkKeyboardColor.DEFAULT, payload={"command": "cave_build"})
        if player.build.forge:
            keyboard.add_button('⚒ Изготовить', color=VkKeyboardColor.DEFAULT)
        if player.build.tavern:
            keyboard.add_button('Нанять', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('Профиль', color=VkKeyboardColor.DEFAULT, payload={"command": "profile"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
    if player.place == 'cave_build':
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "build_stock"})
        keyboard.add_button('Печь', color=VkKeyboardColor.DEFAULT, payload={"command": "build_furnace"})
        keyboard.add_line()
        if not player.build.forge:
            keyboard.add_button('Кузница', color=VkKeyboardColor.DEFAULT, payload={"command": "build_forge"})
        if not player.build.tavern:
            keyboard.add_button('Таверна', color=VkKeyboardColor.DEFAULT, payload={"command": "build_tavern"})
        if not player.build.lift:
            keyboard.add_button('Лифт', color=VkKeyboardColor.DEFAULT, payload={"command": "build_lift"})
        keyboard.add_line()
        keyboard.add_button('Меню подземелья', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
    if player.place == 'mine':
        keyboard.add_button('Вернуться в подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('⛏ Добыть', color=VkKeyboardColor.POSITIVE, payload={"command": "dig"})
        keyboard.add_line()
        keyboard.add_button('Профиль', color=VkKeyboardColor.DEFAULT, payload={"command": "profile"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
    return keyboard.get_keyboard()


def dig(vk, user_id, action_time):
    need_energy = 1
    player = Player.objects.get(user_id=user_id)
    player = energy(player=player, action_time=action_time)
    if player.energy > need_energy:
        player.energy = player.energy - need_energy
        player.stock.stone = player.stock.stone + 2
        player.stock.save()
        player.save()
        message = 'Добыто: Камень 2шт.'
    else:
        message = 'Недостаточно энергии'
    vk.messages.send(
        access_token=token,
        user_id=str(user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def energy(player, action_time):
    delta = action_time - player.last_energy_action
    delta = delta//60
    if delta >= 10:
        energy_new = (delta//10)*player.energy_regen
        energy_max = energy_new + player.energy
        player.energy = min(energy_max, player.max_energy)
        player.last_energy_action = player.last_energy_action + (energy_new*600)
    return player
