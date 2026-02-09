from django.shortcuts import render, redirect
from django.http import Http404
from .models import Lion

def lion_list(request):
    keyword = request.GET.get('keyword', '').strip()
    track = request.GET.get('track', '').strip()

    lions = Lion.objects.all()

    if keyword:
        lions = lions.filter(name__icontains=keyword)

    if track:
        lions = lions.filter(track=track)

    return render(request, 'lions/list.html', {
        'lions': lions,
        'keyword': keyword,
        'track': track,
    })


def lion_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        track = request.POST.get('track')

        if not name:
            return render(request, 'lions/new.html', {
                'error_message': '이름은 필수입니다.'
            })

        Lion.objects.create(
            name=name,
            track=track
        )

        return redirect('lion_list')

    return render(request, 'lions/new.html')

def lion_detail(request, lion_id):
    try:
        lion = Lion.objects.get(id=lion_id)
    except Lion.DoesNotExist:
        raise Http404

    return render(request, 'lions/detail.html', {
        'lion': lion
    })

def lion_edit(request, lion_id):
    try:
        lion = Lion.objects.get(id=lion_id)
    except Lion.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        name = request.POST.get('name')
        track = request.POST.get('track')

        if not name:
            return render(request, 'lions/edit.html', {
                'lion': lion,
                'error_message': '이름은 필수입니다.'
            })

        lion.name = name
        lion.track = track
        lion.save()

        return redirect('lion_detail', lion_id=lion.id)

    return render(request, 'lions/edit.html', {
        'lion': lion
    })

def lion_delete(request, lion_id):
    if request.method != 'POST':
        return redirect('lion_detail', lion_id=lion_id)

    try:
        lion = Lion.objects.get(id=lion_id)
    except Lion.DoesNotExist:
        raise Http404

    lion.delete()
    return redirect('lion_list')
