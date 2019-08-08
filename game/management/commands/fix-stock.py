from django.core.management.base import BaseCommand, CommandError

from ...actions.constant import *
from ...models.build import Stock

class Command(BaseCommand):
    help = 'New stocks for all'

    def handle(self, *args, **options):
        self.stdout.write('Start fix stocks')
        count = 0
        stocks = Stock.objects.all()
        for stock in stocks:
            print(stock.max)
            stock.max = (STOCK_MAX_X + ((stock.lvl // 10) * 20)) * stock.lvl
            stock.save(update_fields=['max'])
            print(stock.max)
            self.stdout.write(str(stock.user_id) + ' fixed!')
            count += 1
        self.stdout.write('End fix stocks')
        self.stdout.write(str(count) + ' stocks has been fixed!')