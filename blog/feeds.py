from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Thought
from .utils import render_markdown


class LatestThoughts(Feed):
    title = settings.SITE["name"]
    description = settings.SITE["tagline"]

    def link(self):
        return reverse("thoughts")

    def items(self):
        return Thought.published()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return render_markdown(item.body)

    def item_pubdate(self, item):
        return item.display_time
