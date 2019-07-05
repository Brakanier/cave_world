from django.db import models
from ..actions.functions import *


class Product(models.Model):
    TYPES = (
        ('wood', 'Дерево'),
        ('stone', 'Камень'),
        ('iron', 'Железо'),
        ('diamond', 'Кристаллы'),
        ('skull', 'Черепа')
    )
    type = models.CharField(
        max_length=30,
        choices=TYPES,
    )
    seller = models.ForeignKey(
        'game.Player',
        on_delete=models.SET(None),
        null=True,
        related_name='products',
    )
    amount = models.IntegerField()
    price = models.IntegerField()
    unit_price = models.FloatField(
        blank=True,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        self.unit_price = self.price / self.amount
        super(Product, self).save(*args, **kwargs)

    def send_seller(self, message):
        try:
            send_info = {
                'user_id': self.seller.user_id,
                'chat_id': self.seller.user_id,
            }
            send(send_info, message)
        except:
            if self.seller.chat_id != self.seller.user_id:
                send_info = {
                    'user_id': self.seller.user_id,
                    'peer_id': self.seller.chat_id,
                    'chat_id': self.seller.chat_id - 2000000000,
                    'nick': self.seller.nickname,
                }
                try:
                    send(send_info, message)
                except:
                    pass

    @staticmethod
    def market_res(player, type):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        try:
            products = Product.objects.filter(type=type).order_by('unit_price')
            all_price = 0
            all_amount = 0
            for item in products:
                all_price += item.price
                all_amount += item.amount

            avr = all_price / all_amount
            avr = int(avr * 100) / 100

            head = 'ID | Кол-во | Цена\n'
            items = head

            for item in products[0:10]:
                items += str(item.id) + ' | ' + str(item.amount) + icon(item.type) + ' | ' + str(item.price) + icon('gold')
                if item.seller == player:
                    items += ' (Ваш)\n'
                else:
                    items += '\n'

            items += '\nСр. цена за 1 ' + icon(type) + ' = ' + str(avr) + ' ✨\n' + "Купить [ID] - купить лот."

            player.keyboard = Product._market_keyboard(player, products[0:5])

            return items

        except Product.DoesNotExist:

            return "Товаров не найдено"

    @staticmethod
    def _market_keyboard(player, items):
        keyboard = VkKeyboard()

        keyboard.add_button('⬅ Назад', color=VkKeyboardColor.DEFAULT, payload={"command": "рынок"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})

        for item in items:
            if item.seller == player:
                your = ' (Ваш)'
            else:
                your = ''
            command = 'купить ' + str(item.id)
            text = '(ID: ' + str(item.id) + ') ' + 'Купить ' + str(item.amount) + icon(item.type) + \
                   ' за ' + str(item.price) + icon('gold') + your
            keyboard.add_line()
            keyboard.add_button(text, color=VkKeyboardColor.POSITIVE, payload={"command": command})

        keyboard.add_line()
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})

        return keyboard.get_keyboard()

    @staticmethod
    def get_products(player, type):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        try:
            products = Product.objects.filter(type=type).order_by('unit_price')[0:10]
        except Product.DoesNotExist:
            return "Товаров не найдено"
        head = "ID | Кол-во | Цена\n"
        items = head
        for item in products:
            items += str(item.id) + ' | ' + str(item.amount) + icon(item.type) + ' | ' + str(item.price) + icon('gold')
            if item.seller == player:
                items += ' (Ваш)\n'
            else:
                items += '\n'
        items += "Купить [ID] - купить лот."
        return items

    @staticmethod
    def buy(player, id):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        try:
            item = Product.objects.get(id=id)
            item_type = item.type
        except Product.DoesNotExist:
            return "Лот не найден!"
        if player.build.stock.res_check('gold', item.price):
            if item.type == 'wood':
                player.build.stock.wood = min(player.build.stock.wood + item.amount, player.build.stock.max)
                player.build.stock.res_remove('gold', item.price)
                player.build.stock.save(update_fields=['wood', 'gold'])
            elif item.type == 'stone':
                player.build.stock.stone = min(player.build.stock.stone + item.amount, player.build.stock.max)
                player.build.stock.res_remove('gold', item.price)
                player.build.stock.save(update_fields=['stone', 'gold'])
            elif item.type == 'iron':
                player.build.stock.iron = min(player.build.stock.iron + item.amount, player.build.stock.max)
                player.build.stock.res_remove('gold', item.price)
                player.build.stock.save(update_fields=['iron', 'gold'])
            elif item.type == 'diamond':
                player.build.stock.diamond = min(player.build.stock.diamond + item.amount, player.build.stock.max)
                player.build.stock.res_remove('gold', item.price)
                player.build.stock.save(update_fields=['diamond', 'gold'])
            elif item.type == 'skull':
                player.build.stock.skull += item.amount
                player.build.stock.res_remove('gold', item.price)
                player.build.stock.save(update_fields=['skull', 'gold'])
            item.seller.build.stock.gold += item.price
            item.seller.build.stock.save(update_fields=['gold'])
            sell_mess = 'У вас купили ' + str(item.amount) + icon(item.type) + ' за ' + str(item.price) + icon('gold')
            item.send_seller(sell_mess)
            message = 'Вы купили ' + str(item.amount) + icon(item.type) + ' за ' + str(item.price) + icon('gold')
            item.delete()
        else:
            message = "Нехватает золота!"

        try:
            items = Product.objects.filter(type=item_type).order_by('unit_price')[0:5]
            player.keyboard = Product._market_keyboard(player, items)
        except Product.DoesNotExist:
            return "Товаров не найдено"

        return message

    @staticmethod
    def sell(player, type, amount, price):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        lots = player.products.count()
        max_amount = player.build.market_lvl * 50
        if amount > max_amount:
            amount = max_amount
        if player.build.stock.res_check(type, amount) and lots < 10:
            result, min_price, max_price = Product.check_price(type, amount, price)
            if result:
                item = Product.objects.create(seller=player, type=type, price=price, amount=amount)
                item.save()
                player.build.stock.res_remove(type, amount)
                player.build.stock.save(update_fields=[type])
                message = 'Лот выставлен!\n' + \
                          'ID | Кол-во | Цена\n' + \
                          str(item.id) + ' | ' \
                          + str(item.amount) + icon(item.type) + ' | ' \
                          + str(item.price) + icon('gold')

            else:
                message = 'Вы указали слишком большую или маленькую цену!\n' + \
                          'Указанная цена: ' + str(price) + icon('gold') + '\n' \
                          'Мин. цена: ' + str(min_price) + icon('gold') + '\n' \
                          'Макс. цена: ' + str(max_price) + icon('gold') + '\n'

        else:
            message = 'Нехватает' + icon(type) + ' или у вас больше 10 лотов!'
        return message

    @staticmethod
    def del_lot(player, id):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        try:
            item = player.products.get(id=id)
        except Product.DoesNotExist:
            return "Лот не найден!"
        if item.type == 'wood':
            player.build.stock.wood = min(player.build.stock.wood + item.amount, player.build.stock.max)
            player.build.stock.save(update_fields=['wood'])
        elif item.type == 'stone':
            player.build.stock.stone = min(player.build.stock.stone + item.amount, player.build.stock.max)
            player.build.stock.save(update_fields=['stone'])
        elif item.type == 'iron':
            player.build.stock.iron = min(player.build.stock.iron + item.amount, player.build.stock.max)
            player.build.stock.save(update_fields=['iron'])
        elif item.type == 'diamond':
            player.build.stock.diamond = min(player.build.stock.diamond + item.amount, player.build.stock.max)
            player.build.stock.save(update_fields=['diamond'])
        elif item.type == 'skull':
            player.build.stock.skull += item.amount
            player.build.stock.save(update_fields=['skull'])
        message = 'Вы сняли с продажи:\n' + \
                  'ID: ' + str(item.id) + ' | ' + str(item.amount) + icon(item.type) + ' | ' + str(item.price) + icon('gold')
        item.delete()
        return message

    @staticmethod
    def get_param(command):
        part = command.split()
        if len(part) == 4 and part[2].isdigit() and part[3].isdigit():
            count = int(part[2])
            price = int(part[3])
            return count, price
        else:
            return None, None

    @staticmethod
    def get_id(command):
        part = command.split()
        if len(part) == 2 and part[1].isdigit():
            return int(part[1])
        else:
            return None

    @staticmethod
    def my_lots(player):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        products = player.products.all()
        head = "Ваши лоты:\n" + "ID | Кол-во | Цена\n"
        items = head
        for item in products:
            items += str(item.id) + ' | ' + str(item.amount) + icon(item.type) + ' | ' + str(item.price) + icon('gold') + '\n'
        return items

    @staticmethod
    def info(player):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        player.place = 'market'
        player.save(update_fields=['place'])
        message = 'Рынок\n' + \
                  'Команды:\n' + \
                  'Мои лоты - список ваших лотов в продаже.\n' + \
                  'Снять [ID] - снимает с продажи ваш лот номер [ID].\n' + \
                  'Купить [ID] - купить лот номер [ID].\n' + \
                  'Рынок [ресурс] - список лотов для покупки.\n' + \
                  'Продать [ресурс] [кол-во] [цена] - выставить на продажу ресурс.\n' + \
                  'Отправить [ресурс] [кол-во] [ID-игрока] - отправить ресурсы.\n'

        return message

    @staticmethod
    def check_price(type, amount, price):
        avr = Product.get_average_price(type)
        range_price = avr * 0.5
        max_price = int((avr + range_price) * amount)
        min_price = int((avr - range_price) * amount)

        if price < min_price or price > max_price:
            result = False
        else:
            result = True

        return result, min_price, max_price

    @staticmethod
    def get_average_price(type):
        products = Product.objects.filter(type=type).all()
        all_price = 0
        all_amount = 0
        for item in products:
            all_price += item.price
            all_amount += item.amount

        avr = all_price / all_amount
        print(type)
        print(all_price)
        print(all_amount)
        if len(products) < 3:
            avr = 2
        if len(products) < 3 and type == 'skull':
            avr = 200

        print(avr)

        return avr

    @staticmethod
    def admin_del_lot(id):
        try:
            item = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return "Лот не найден!"
        if item.type == 'wood':
            item.seller.build.stock.wood += item.amount
            item.seller.build.stock.save(update_fields=['wood'])
        elif item.type == 'stone':
            item.seller.build.stock.stone += item.amount
            item.seller.build.stock.save(update_fields=['stone'])
        elif item.type == 'iron':
            item.seller.build.stock.iron += item.amount
            item.seller.build.stock.save(update_fields=['iron'])
        elif item.type == 'diamond':
            item.seller.build.stock.diamond += item.amount
            item.seller.build.stock.save(update_fields=['diamond'])
        elif item.type == 'skull':
            item.seller.build.stock.skull += item.amount
            item.seller.build.stock.save(update_fields=['skull'])
        message = 'Вы сняли с продажи:\n' + \
                  'ID: ' + str(item.id) + ' | ' + str(item.amount) + icon(item.type) + ' | ' + str(item.price) + icon('gold')
        item.delete()
        return message
