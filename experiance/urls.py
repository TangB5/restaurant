from django.urls import path
from . import views

urlpatterns = [
    path('', views.laisser_avis, name='laisser_avis'),
]