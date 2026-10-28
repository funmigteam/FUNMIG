from django.apps import apps
from django.core.management.base import BaseCommand

from core.images import IMAGE_FIELDS, optimize_instance


class Command(BaseCommand):
    help = 'Resize and recompress stored images that are larger than needed.'

    def add_arguments(self, parser):
        parser.add_argument('--model', help='Only process one model, e.g. Post')

    def handle(self, *args, **options):
        saved = 0
        processed = 0
        for (app_label, model_name), (field_name, _) in IMAGE_FIELDS.items():
            if options['model'] and options['model'] != model_name:
                continue
            model = apps.get_model(app_label, model_name)
            queryset = model.objects.exclude(**{field_name: ''}).exclude(**{f'{field_name}__isnull': True})
            for instance in queryset.iterator():
                result = optimize_instance(instance)
                if result:
                    processed += 1
                    saved += result['before'] - result['after']
                    self.stdout.write(f"{model_name} #{instance.pk}: {result['before'] // 1024}KB -> {result['after'] // 1024}KB")
        self.stdout.write(self.style.SUCCESS(f'{processed} images optimized, {saved / 1024 / 1024:.1f} MB saved'))
