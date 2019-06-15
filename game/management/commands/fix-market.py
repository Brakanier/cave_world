from django.core.management.base import BaseCommand, CommandError
from ...models.market import Product


class Command(BaseCommand):
    help = 'Send message for all users and chats'

    def handle(self, *args, **options):
        self.stdout.write('Start clearing market')
        products = Product.objects.filter(unit_price__gte=5).exclude(type='skull').all()
        for item in products:
            Product.del_lot(item.seller, item.id)
            self.stdout.write('Remove - ' + item.seller.nickname + ' | ' + str(item.id) + ' | ' + str(item.price))

        skulls = Product.objects.filter(unit_price__gte=250, type='skull').all()
        for skull in skulls:
            Product.del_lot(skull.seller, skull.id)
            self.stdout.write('Remove - ' + skull.seller.nickname + ' | ' + str(skull.id) + ' | ' + str(skull.price))

        self.stdout.write('End clear')

