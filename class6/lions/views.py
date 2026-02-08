from django.shortcuts import render, redirect
from django.http import Http404

LIONS = []
NEXT_ID = 1

def lion_list(request):
    # 조회 전용 (GET)
    keyword = request.GET.get('keyword', '').strip()

    lions = LIONS
    if keyword:
        lions = [l for l in LIONS if keyword.lower() in l['name'].lower()]

    return render(request, 'lions/list.html', {
        'lions': lions,
        'keyword': keyword,
    })



def lion_create(request):
    # 생성 (GET: 화면 / POST: 처리)
    global NEXT_ID

    if request.method == 'POST':
        name = request.POST.get('name')
        track = request.POST.get('track')

        if not name:
            return render(request, 'lions/new.html', {
                'error_message': '이름은 필수입니다.'
            })

        LIONS.append({
            'id': NEXT_ID,
            'name': name,
            'track': track,
        })
        NEXT_ID += 1

        return redirect('lion_list')

    return render(request, 'lions/new.html')


def lion_detail(request, lion_id):
    lion = next((l for l in LIONS if l['id'] == lion_id), None)
    if not lion:
        raise Http404

    return render(request, 'lions/detail.html', {
        'lion': lion
    })


def lion_edit(request, lion_id):
    # 수정 (GET: 화면 / POST: 처리)
    lion = next((l for l in LIONS if l['id'] == lion_id), None)
    if not lion:
        raise Http404

    if request.method == 'POST':
        name = request.POST.get('name')
        track = request.POST.get('track')

        if not name:
            return render(request, 'lions/edit.html', {
                'lion': lion,
                'error_message': '이름은 필수입니다.'
            })

        lion['name'] = name
        lion['track'] = track
        return redirect('lion_detail', lion_id=lion_id)

    return render(request, 'lions/edit.html', {
        'lion': lion
    })

def lion_delete(request, lion_id):
    # 삭제 (POST 전용)
    global LIONS

    lion = next((l for l in LIONS if l['id'] == lion_id), None)
    if not lion:
        raise Http404

    if request.method == 'POST':
        LIONS = [l for l in LIONS if l['id'] != lion_id]
        return redirect('lion_list')

    return redirect('lion_detail', lion_id=lion_id)

