from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_form, name='reservation'),
    path('mes-reservations/', views.mes_reservations, name='mes_reservations'),
]