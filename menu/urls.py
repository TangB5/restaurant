# menu/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('carte/', views.menu, name='menu'),

    path('commande/<int:pk>/', views.commande, name='commande'),

    path('mesCommande/', views.detail, name='Mes_commande'),

    path('reorder/<int:commande_id>/', views.reorder, name='reorder'),

    # Annuler une commande en attente
    path('cancel/<int:commande_id>/', views.cancel_commande, name='cancel_commande'),

    # AJAX - Récupérer les détails d'une commande (pour le modal)
    path('commande/<int:commande_id>/details/', views.commande_detail_ajax, name='commande_detail_ajax'),
]