from django.conf import settings


def site(request):
    bg = settings.SITE.get("background", "")
    return {"SITE": settings.SITE, "BG_IS_GIF": bg.lower().endswith(".gif")}
