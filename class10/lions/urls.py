from django.urls import path
from . import views
from .views import LionListView

urlpatterns = [
    path("", LionListView.as_view(), name="lion_list"),                                          # 목록 (CBV)
    path('new/', views.lion_create, name='lion_create'),                                          # 등록
    path('<int:lion_id>/', views.lion_detail, name='lion_detail'),                                # 상세
    path('<int:lion_id>/edit/', views.lion_edit, name='lion_edit'),                               # 수정
    path('<int:lion_id>/delete/', views.lion_delete, name='lion_delete'),                          # 삭제
    path("<int:lion_id>/tasks/<int:task_id>/toggle/", views.task_toggle, name="task_toggle"),     # task 완료 토글
]
