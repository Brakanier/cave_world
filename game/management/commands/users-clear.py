from django.core.management.base import BaseCommand, CommandError

from ...models.player import Player
from system.models import Registration


class Command(BaseCommand):
    help = 'Delete users with level = 1'

    def handle(self, *args, **options):
        self.stdout.write('Start clearing')
        players = Player.objects.filter(lvl=1)
        for player in players:
            if player.build and player.build.stock:
                player.build.stock.delete()
            if player.build:
                player.build.delete()
            if player.war:
                player.war.delete()
            if player.inventory and player.inventory.trophy:
                player.inventory.trophy.all().delete()
            if player.inventory and player.inventory.chests:
                player.inventory.chests.all().delete()
            if player.inventory and player.inventory.items:
                player.inventory.items.all().delete()
            if player.inventory:
                player.inventory.delete()
            if player.cave_progress:
                player.cave_progress.delete()

            try:
                Registration.objects.get(user_id=player.user_id).delete()
            except:
                pass

            if player.products:
                player.products.all().delete()
            player.delete()
            mess = player.nickname + ' - deleted!'
            self.stdout.write(mess)
        registrations = Registration.objects.all()
        for reg in registrations:
            if Player.objects.filter(user_id=reg.user_id).exists():
                self.stdout.write(str(reg.user_id) + ' - pass')
            else:
                reg.delete()
                self.stdout.write(str(reg.user_id) + ' - deleted')





