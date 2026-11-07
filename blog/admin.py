from django.contrib import admin

from .models import Thought

admin.site.site_header = "Thoughts admin"
admin.site.site_title = "Thoughts admin"


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "display_time")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    fields = ("title", "body", "is_published", "display_time")
    readonly_fields = ("display_time",)
