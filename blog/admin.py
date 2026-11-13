from django.contrib import admin
from django.utils.html import format_html

from .models import Thought, ThoughtMedia

admin.site.site_header = "Thoughts admin"
admin.site.site_title = "Thoughts admin"


class MediaInline(admin.StackedInline):
    model = ThoughtMedia
    extra = 1
    fields = ("file", "position", "caption", "snippet")
    readonly_fields = ("snippet",)

    @admin.display(description="Code to place it in the text")
    def snippet(self, obj):
        if not obj.pk:
            return "Save the thought first to get the code."
        code = f"![{obj.caption}]({obj.file.url})"
        return format_html('<input type="text" readonly size="70" value="{}" onclick="this.select()">', code)


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "display_time")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    fields = ("title", "body", "is_published", "display_time")
    readonly_fields = ("display_time",)
    inlines = [MediaInline]
