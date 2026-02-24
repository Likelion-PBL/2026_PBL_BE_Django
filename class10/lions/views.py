from .models import Lion, Task
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

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

@transaction.atomic
def lion_create(request):
    if request.method != "POST":
        return render(request, "lions/new.html")

    name = request.POST.get("name", "").strip()
    track = request.POST.get("track", "").strip()

    if not name or not track:
        return render(request, "lions/new.html", {
            "error_message": "이름과 트랙을 입력하세요."
        })

    lion = Lion.objects.create(name=name, track=track)

    default_tasks = ["기초 과제", "중급 과제", "심화 과제"]

    for title in default_tasks:
        Task.objects.create(lion=lion, title=title)

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
    task.completed = not task.completed
    task.save(update_fields=["completed"])

    return redirect("lion_detail", lion_id=lion_id)