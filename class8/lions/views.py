from .models import Lion
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

def lion_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        track = request.POST.get("track")

        if not name:
            return render(request, "lions/new.html", {
                "error_message": "이름은 필수입니다."
            })

        Lion.objects.create(
            name=name,
            track=track
        )

        return redirect("lion_list")

    return render(request, "lions/new.html")

def lion_detail(request, lion_id):
    lion = get_object_or_404(Lion, id=lion_id)
    return render(request, "lions/detail.html", {"lion": lion})


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