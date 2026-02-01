from django.shortcuts import render, redirect

# 임시 저장소
LIONS = []

def lion_list(request):
    return render(request, 'lions/list.html', {
        'lions': LIONS
    })

# 기본 PBL 코드
# def lion_create(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')

#         if name:
#             LIONS.append(name)

#         # 핵심: POST 후 Redirect
#         return redirect('lion_list')

#     # GET 요청일 때만 폼 화면
#     return render(request, 'lions/new.html')

# Bonus PBL 코드
def lion_create(request):
    error_message = None

    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            error_message = '이름을 입력해주세요.'
        else:
            LIONS.append(name)
            return redirect('lion_list')

    return render(request, 'lions/new.html', {
        'error_message': error_message
    })