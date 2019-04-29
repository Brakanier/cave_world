from django.core.management.base import BaseCommand, CommandError
from ...models.player import Player


class Command(BaseCommand):
    help = 'Set max energy 30'

    def handle(self, *args, **options):
        players = Player.objects.all()
        for player in players:
            player.max_energy = 30
            player.save(update_fields=['max_energy'])
            self.stdout.write(player.nickname + ' - ok')
