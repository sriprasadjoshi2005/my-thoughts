import bleach
import markdown

TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "h1", "h2", "h3", "h4",
        "h5", "h6", "a", "blockquote", "code", "pre", "hr"]
ATTRS = {"a": ["href", "title"]}


def render_markdown(text):
    html = markdown.markdown(text or "", extensions=["nl2br", "fenced_code"])
    return bleach.clean(html, tags=TAGS, attributes=ATTRS,
                        protocols=["http", "https", "mailto"], strip=True)
