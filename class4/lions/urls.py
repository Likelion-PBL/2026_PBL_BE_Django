from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('lions/', views.lion_list),
]
