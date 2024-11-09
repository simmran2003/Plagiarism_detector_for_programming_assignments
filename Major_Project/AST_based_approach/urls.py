from django.urls import path
from . import views

urlpatterns = [
    path('', views.compare_code, name='compare_code'), 
]
