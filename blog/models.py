from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from .utils import media_html, render_markdown


def check_size(f):
    limit = settings.MAX_UPLOAD_MB * 1024 * 1024
    if f.size > limit:
        raise ValidationError(f"File is larger than {settings.MAX_UPLOAD_MB} MB.")


class Thought(models.Model):
    title = models.CharField(max_length=200, help_text="Shown on cards and in search. Not shown on the thought’s own page.")
    body = models.TextField(blank=True, help_text="Markdown supported. Can be empty if you only attach photos or videos below.")
    is_published = models.BooleanField(default=False, help_text="Untick to keep it as a draft.")
    display_time = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-display_time"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published:
            self.display_time = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("thought_detail", args=[self.pk])

    def rendered_body(self):
        # Files whose code isn't in the text are placed by their Position setting.
        unplaced = [m for m in self.media.all() if m.file.url not in self.body]
        top = "".join(media_html(m.file.url, m.caption) for m in unplaced if m.position == "top")
        bottom = "".join(media_html(m.file.url, m.caption) for m in unplaced if m.position != "top")
        return mark_safe(top + render_markdown(self.body) + bottom)

    @classmethod
    def published(cls):
        return cls.objects.filter(is_published=True)


class ThoughtMedia(models.Model):
    POSITIONS = [
        ("top", "Top (before the text)"),
        ("bottom", "Bottom (after the text)"),
    ]

    thought = models.ForeignKey(Thought, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(
        upload_to="thoughts/%Y/%m/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif", "webp", "mp4", "webm"]), check_size],
    )
    position = models.CharField(
        max_length=6, choices=POSITIONS, default="bottom",
        help_text="Used when you don’t paste this file’s code into the text.",
    )
    caption = models.CharField(max_length=200, blank=True, help_text="Short description, used as the image’s alt text.")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.file.name
