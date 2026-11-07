import re

import bleach
import markdown
from django.utils.html import format_html

TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "h1", "h2", "h3", "h4",
        "h5", "h6", "a", "blockquote", "code", "pre", "hr", "img", "video"]
ATTRS = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
    "video": ["src", "controls", "preload"],
}
VIDEO_EXT = (".mp4", ".webm")
_VIDEO_IMG = re.compile(r'<img[^>]*?src="([^"]+\.(?:mp4|webm))"[^>]*>', re.I)


def render_markdown(text):
    html = markdown.markdown(text or "", extensions=["nl2br", "fenced_code"])
    html = _VIDEO_IMG.sub(r'<video controls preload="metadata" src="\1"></video>', html)
    return bleach.clean(html, tags=TAGS, attributes=ATTRS,
                        protocols=["http", "https", "mailto"], strip=True)


def media_html(url, alt=""):
    if url.lower().endswith(VIDEO_EXT):
        return format_html('<video controls preload="metadata" src="{}"></video>', url)
    return format_html('<img src="{}" alt="{}" loading="lazy">', url, alt)
