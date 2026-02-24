from .models import Lion, Task
from .services import create_lion_with_default_tasks
from .services import toggle_task
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView

def lion_list(request):
    keyword = request.GET.get("keyword", "")
    track = request.GET.get("track", "")

    lions = Lion.objects.all()

    if keyword:
        lions = lions.filter(
            Q(name__icontains=keyword) |
            Q(track__icontains=keyword)
        )

    if track:
        lions = lions.filter(track=track)

    context = {
        "lions": lions,
        "keyword": keyword,
        "track": track,
        "count": lions.count(),
    }

    return render(request, "lions/list.html", context)

class LionListView(ListView):
    model = Lion
    template_name = "lions/list.html"
    context_object_name = "lions"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword", "")
        track = self.request.GET.get("track", "")

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) |
                Q(track__icontains=keyword)
            )

        if track:
            queryset = queryset.filter(track=track)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["keyword"] = self.request.GET.get("keyword", "")
        context["track"] = self.request.GET.get("track", "")

        # 이미 계산된 paginator 사용
        context["count"] = context["paginator"].count

        return context

def lion_create(request):
    if request.method != "POST":
        return render(request, "lions/new.html")

    name = request.POST.get("name", "").strip()
    track = request.POST.get("track", "").strip()

    if not name or not track:
        return render(request, "lions/new.html", {
            "error_message": "이름과 트랙을 입력하세요."
        })

    create_lion_with_default_tasks(name, track)

    return redirect("lion_list")

def lion_detail(request, lion_id):
    lion = get_object_or_404(Lion, id=lion_id)

    status = request.GET.get("status", "")
    tasks = lion.tasks.all()

    if status == "done":
        tasks = tasks.filter(completed=True)
    elif status == "todo":
        tasks = tasks.filter(completed=False)

    context = {
        "lion": lion,
        "tasks": tasks,
        "status": status,
        "task_count": tasks.count(),
    }

    return render(request, "lions/detail.html", context)

def lion_edit(request, lion_id):
    lion = get_object_or_404(Lion, id=lion_id)

    if request.method != "POST":
        return render(request, "lions/edit.html", {"lion": lion})

    name = request.POST.get("name", "").strip()
    track = request.POST.get("track", "").strip()

    if not name or not track:
        return render(request, "lions/edit.html", {
            "lion": lion,
            "error_message": "이름과 트랙을 입력하세요."
        })

    lion.name = name
    lion.track = track
    lion.save(update_fields=["name", "track"])

    return redirect("lion_detail", lion_id=lion.id)

def lion_delete(request, lion_id):
    lion = get_object_or_404(Lion, id=lion_id)

    if request.method == "POST":
        lion.delete()
        return redirect("lion_list")

    return redirect("lion_detail", lion_id=lion_id)

def task_toggle(request, lion_id, task_id):
    if request.method != "POST":
        return redirect("lion_detail", lion_id=lion_id)

    task = get_object_or_404(Task, id=task_id, lion_id=lion_id)
    toggle_task(task)

    return redirect("lion_detail", lion_id=lion_id)