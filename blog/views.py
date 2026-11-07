from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Thought


def home(request):
    return render(request, "home.html", {"thoughts": Thought.published()[:3]})


def thoughts(request):
    sort = "oldest" if request.GET.get("sort") == "oldest" else "newest"
    order = "display_time" if sort == "oldest" else "-display_time"
    paginator = Paginator(Thought.published().order_by(order), settings.PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "thoughts.html", {"page": page, "sort": sort})


def thought_detail(request, pk):
    qs = Thought.objects.all() if request.user.is_staff else Thought.published()
    thought = get_object_or_404(qs, pk=pk)
    share_url = request.build_absolute_uri(thought.get_absolute_url())
    return render(request, "thought_detail.html", {"thought": thought, "share_url": share_url})


def about(request):
    return render(request, "about.html")


def _search(q):
    q = q.strip()
    if not q:
        return Thought.objects.none()
    return Thought.published().filter(Q(title__icontains=q) | Q(body__icontains=q))


def search(request):
    q = request.GET.get("q", "").strip()
    return render(request, "search.html", {"q": q, "results": _search(q)[:50]})


def search_live(request):
    items = _search(request.GET.get("q", ""))[:6]
    return JsonResponse({"results": [{"title": t.title, "url": t.get_absolute_url()} for t in items]})
