from django.urls import path
from . import views

urlpatterns = [
    # C'est la ligne qui définit le nom 'menu'
    path('carte/', views.menu, name='menu'),
    path('commande/<int:pk>/', views.commande, name='commande'),
    path('mesCommande/', views.detail, name='Mes_commande'),
]
