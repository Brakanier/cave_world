from django.db import models
from ..actions.functions import *


class Product(models.Model):
    TYPES = (
        ('wood', 'Дерево'),
        ('stone', 'Камень'),
        ('iron', 'Железо'),
        ('diamond', 'Кристаллы')
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
    def get_products(player, type):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        try:
            products = Product.objects.filter(type=type).order_by('unit_price')[0:5]
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
            item.seller.build.stock.gold += item.price
            item.seller.build.stock.save(update_fields=['gold'])
            sell_mess = 'У вас купили ' + str(item.amount) + icon(item.type) + ' за ' + str(item.price) + icon('gold')
            item.send_seller(sell_mess)
            message = 'Вы купили ' + str(item.amount) + icon(item.type) + ' за ' + str(item.price) + icon('gold')
            item.delete()
        else:
            message = "Нехватает золота!"
        return message

    @staticmethod
    def sell(player, type, price):
        if player.build.market_lvl == 0:
            return 'Сначала постройте Торговый Пост!\nКоманда: Строить рынок'
        lots = player.products.count()
        if player.build.stock.res_check(type, 50) and lots < 10:
            item = Product.objects.create(seller=player, type=type, price=price, amount=50)
            item.save()
            player.build.stock.res_remove(type, 50)
            player.build.stock.save(update_fields=[type])
            message = 'Лот выставлен!\n' + \
                      'ID | Кол-во | Цена\n' + \
                      str(item.id) + ' | ' + str(item.amount) + icon(item.type) + ' | ' + str(item.price) + icon('gold')
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
        message = 'Вы сняли с продажи:\n' + \
                  'ID: ' + str(item.id) + ' | ' + str(item.amount) + icon(item.type) + ' | ' + str(item.price) + icon('gold')
        item.delete()
        return message

    @staticmethod
    def get_param(command):
        part = command.split()
        if len(part) == 3 and part[2].isdigit():
            return int(part[2])
        elif len(part) == 2 and part[1].isdigit():
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
                  'Продать [ресурс] [цена] - выставить на продажу 50 ресурса.\n' + \
                  'Отправить [ресурс] [кол-во] [ID-игрока] - отправить ресурсы.\n'

        return message
