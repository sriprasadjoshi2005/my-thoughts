import json

from django.core.management.base import BaseCommand

from blog.models import Thought


class Command(BaseCommand):
    help = "Export all thoughts (including drafts) to a JSON file."

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", default="thoughts_backup.json")

    def handle(self, *args, **options):
        data = [
            {
                "title": t.title,
                "body": t.body,
                "is_published": t.is_published,
                "display_time": t.display_time.isoformat() if t.display_time else None,
            }
            for t in Thought.objects.order_by("id")
        ]
        with open(options["path"], "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.stdout.write(f"Exported {len(data)} thoughts to {options['path']}")
