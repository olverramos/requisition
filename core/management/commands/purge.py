from django.core.management.base import BaseCommand, CommandError

from modules.needs.models import Need

class Command(BaseCommand):
    help = "Reinicia el sistema sin necesidades creadas"

    def handle(self, *args, **options):
        try:
            Need.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Sistema reiniciado sin necesidades')
            )
        except Exception as exc:
             raise CommandError(f'Error al reiniciar la base: {exc}')
