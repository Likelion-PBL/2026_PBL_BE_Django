from .models import Lion, Task
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

def lion_list(request):
    keyword = request.GET.get("keyword", "")
    track = request.GET.get("track", "")

    lions = Lion.objects.all()

    # Q 객체 복합 검색
    if keyword:
        lions = lions.filter(
            Q(name__icontains=keyword) |
            Q(track__icontains=keyword)
        )

    if track:
        lions = lions.filter(track=track)

    # 최신순 정렬 (Meta에 있으면 없어도 됨)
    lions = lions.order_by("-created_at")

    # 개수 계산
    count = lions.count()

    context = {
        "lions": lions,
        "keyword": keyword,
        "track": track,
        "count": count,
    }

    return render(request, "lions/list.html", context)

@transaction.atomic
def lion_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        track = request.POST.get("track")

        if not name or not track:
            return render(request, "lions/new.html", {
                "error_message": "이름과 트랙을 입력하세요."
            })

        lion = Lion.objects.create(name=name, track=track)

        # 기본 과제 자동 생성
        Task.objects.create(lion=lion, title="기초 과제")
        Task.objects.create(lion=lion, title="중급 과제")
        Task.objects.create(lion=lion, title="심화 과제")

        return redirect("lion_list")

    return render(request, "lions/new.html")

def lion_detail(request, lion_id):
    lion = get_object_or_404(Lion, id=lion_id)

    status = request.GET.get("status", "")

    tasks_qs = lion.tasks.all()

    if status == "done":
        tasks_qs = tasks_qs.filter(completed=True)
    elif status == "todo":
        tasks_qs = tasks_qs.filter(completed=False)

    tasks_qs = tasks_qs.order_by("-created_at")
    task_count = tasks_qs.count()

    return render(request, "lions/detail.html", {
        "lion": lion,
        "tasks": tasks_qs,
        "status": status,
        "task_count": task_count,
    })

def lion_edit(request, lion_id):
    lion = get_object_or_404(Lion, id=lion_id)

    if request.method == "POST":
        lion.name = request.POST.get("name")
        lion.track = request.POST.get("track")
        lion.save()

        return redirect("lion_detail", lion_id=lion.id)

    return render(request, "lions/edit.html", {"lion": lion})


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