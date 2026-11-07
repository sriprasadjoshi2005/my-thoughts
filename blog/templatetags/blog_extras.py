from django import template
from django.utils.safestring import mark_safe

from blog.utils import render_markdown

register = template.Library()


@register.filter
def markdown(value):
    return mark_safe(render_markdown(value))
