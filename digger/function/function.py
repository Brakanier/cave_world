import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_random_id():
    """ Get random int32 number (signed) """
    return random.getrandbits(31) * random.choice([-1, 1])


def energy(player, action_time):
    delta = action_time - player.last_energy_action
    delta = delta//60
    if delta >= 10:
        energy_new = (delta//10)*player.energy_regen
        energy_max = energy_new + player.energy
        player.energy = min(energy_max, player.max_energy)
        player.last_energy_action = player.last_energy_action + (energy_new*600)
    return player


def exp(vk, player, token, exp):
    current_exp = player.exp + exp
    if current_exp >= player.exp_need:
        more_exp = player.exp_need - current_exp
        player.lvl = player.lvl + 1
        player.exp = more_exp
        player.exp_need = player.lvl * (9 + player.lvl)
        message = 'Поздравляю! Вы теперь ' + str(player.lvl) + ' ур.'
        vk.messages.send(
            access_token=token,
            user_id=str(player.user_id),
            keyboard=get_keyboard(player=player),
            message=message,
            random_id=get_random_id()
        )
    else:
        player.exp = current_exp
    return player


def get_keyboard(player):
    keyboard = VkKeyboard()
    if player.place == 'profile':
        keyboard.add_button('Профиль', color=VkKeyboardColor.DEFAULT, payload={"command": "profile"})
        keyboard.add_line()
        keyboard.add_button('Меню подземелья', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
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
