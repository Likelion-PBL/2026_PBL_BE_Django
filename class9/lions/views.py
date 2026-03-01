from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q
from .models import Lion, Task, LionProfile, Tag


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

    lions = lions.order_by("-created_at")
    count = lions.count()

    return render(request, "lions/list.html", {
        "lions": lions,
        "keyword": keyword,
        "track": track,
        "count": count,
    })


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

        # 기본 과제 3개 자동 생성 (1:N)
        Task.objects.create(lion=lion, title="기초 과제")
        Task.objects.create(lion=lion, title="중급 과제")
        Task.objects.create(lion=lion, title="심화 과제")

        # 프로필 자동 생성 (1:1) — Lion 생성과 동시에 빈 프로필도 만든다
        LionProfile.objects.create(lion=lion)

        return redirect("lion_list")

    return render(request, "lions/new.html")


def lion_detail(request, lion_id):
    lion = get_object_or_404(Lion, id=lion_id)

    # 1:N 역방향 접근: lion.tasks.all()
    status = request.GET.get("status", "")
    tasks_qs = lion.tasks.all()
    if status == "done":
        tasks_qs = tasks_qs.filter(completed=True)
    elif status == "todo":
        tasks_qs = tasks_qs.filter(completed=False)
    tasks_qs = tasks_qs.order_by("-created_at")

    # 1:1 역방향 접근: lion.profile (없으면 None)
    try:
        profile = lion.profile
    except LionProfile.DoesNotExist:
        profile = None

    # N:M 역방향 접근: lion.tags.all()
    tags = lion.tags.all()
    all_tags = Tag.objects.all()

    return render(request, "lions/detail.html", {
        "lion": lion,
        "tasks": tasks_qs,
        "status": status,
        "task_count": tasks_qs.count(),
        "profile": profile,
        "tags": tags,
        "all_tags": all_tags,
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


# ──────────────────────────────────────────────
# 1:1  LionProfile 뷰
# ──────────────────────────────────────────────
def profile_edit(request, lion_id):
    """
    Lion의 1:1 프로필을 수정한다.
    - get_or_create: 프로필이 없으면 새로 만들고, 있으면 가져온다.
    - 1:1 관계이므로 Lion당 프로필은 반드시 1개만 존재한다.
    """
    lion = get_object_or_404(Lion, id=lion_id)
    profile, _ = LionProfile.objects.get_or_create(lion=lion)

    if request.method == "POST":
        profile.github_url = request.POST.get("github_url", "").strip()
        profile.bio = request.POST.get("bio", "").strip()
        profile.save()
        return redirect("lion_detail", lion_id=lion_id)

    return render(request, "lions/profile_edit.html", {
        "lion": lion,
        "profile": profile,
    })


# ──────────────────────────────────────────────
# N:M  Tag 뷰
# ──────────────────────────────────────────────
def tag_toggle(request, lion_id, tag_id):
    """
    Lion에 Tag를 추가하거나 제거한다 (N:M 토글).
    - lion.tags.add(tag)    → 중간 테이블에 행 INSERT
    - lion.tags.remove(tag) → 중간 테이블에서 행 DELETE
    - Lion과 Tag 양쪽에서 서로를 조회할 수 있다 (양방향).
    """
    if request.method != "POST":
        return redirect("lion_detail", lion_id=lion_id)

    lion = get_object_or_404(Lion, id=lion_id)
    tag = get_object_or_404(Tag, id=tag_id)

    if tag in lion.tags.all():
        lion.tags.remove(tag)   # 이미 있으면 제거
    else:
        lion.tags.add(tag)      # 없으면 추가

    return redirect("lion_detail", lion_id=lion_id)
