from django.urls import path
from . import views

urlpatterns = [
    path('test_total/', views.test_total, name='test_total'),
    path('health/', views.health_check, name='health_check'),
]
