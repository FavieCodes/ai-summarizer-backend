from django.urls import path
from . import views

urlpatterns = [
    path('summarize/', views.summarize_page, name='summarize'),
    path('health/', views.health_check, name='health'),
]