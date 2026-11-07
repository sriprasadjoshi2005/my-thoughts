from django.db import models
from django.urls import reverse
from django.utils import timezone


class Thought(models.Model):
    title = models.CharField(max_length=200, help_text="Shown on cards and in search. Not shown on the thought’s own page.")
    body = models.TextField(help_text="Markdown supported: **bold**, *italic*, # headings, [links](https://example.com), - lists.")
    is_published = models.BooleanField(default=False, help_text="Untick to keep it as a draft.")
    display_time = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-display_time"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Publishing or editing a published thought sets its time to now.
        if self.is_published:
            self.display_time = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("thought_detail", args=[self.pk])

    @classmethod
    def published(cls):
        return cls.objects.filter(is_published=True)
