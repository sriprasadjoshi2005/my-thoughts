import json

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from blog.models import Thought


class Command(BaseCommand):
    help = "Import thoughts from a JSON file made by export_thoughts (run on an empty database)."

    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, *args, **options):
        with open(options["path"], encoding="utf-8") as f:
            data = json.load(f)
        # bulk_create skips save(), so original times are kept.
        Thought.objects.bulk_create(
            Thought(
                title=d["title"],
                body=d["body"],
                is_published=d["is_published"],
                display_time=parse_datetime(d["display_time"]) if d["display_time"] else None,
            )
            for d in data
        )
        self.stdout.write(f"Imported {len(data)} thoughts.")
