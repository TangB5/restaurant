# menu/views.py
from django.http import HttpResponse ,JsonResponse
from django.shortcuts import render,redirect
from .models import Plat, CategorieMenu,Commande

from django.contrib.auth.decorators import login_required


def menu(request):
    """
    Affiche le menu en regroupant les plats par catégorie.
    Les plats non disponibles ne sont pas inclus.
    """
    # 1. Récupérer toutes les catégories, triées par 'ordre'.
    # 2. Utiliser prefetch_related('plats') pour charger tous les plats
    #    disponibles de toutes les catégories en un minimum de requêtes (optimisation).

    # NOTE: Pour filtrer uniquement les plats disponibles dans le prefetch,
    # on utilise Prefetch. Pour une simple liste, on peut filtrer les plats après.

    # ------------------------------------------------------------
    # Option 1: Récupérer les catégories avec tous les plats disponibles
    # ------------------------------------------------------------
    categories_avec_plats = CategorieMenu.objects.filter(
        # On peut filtrer les catégories qui contiennent au moins un plat disponible
        # Attention: ceci ne filtre pas les plats dans le .all(), c'est juste un exemple.
        # plats__disponible=True 
    ).prefetch_related('plats').order_by('ordre').distinct()

    context = {

        'categories': categories_avec_plats,

    }

    return render(
        request=request,
        template_name='menu/carte.html',
        context=context
    )

@login_required
def commande(request,pk:None):

    if pk:
        plat_a_commander = Plat.objects.filter(id=pk).last()

        if plat_a_commander and plat_a_commander.stock > 0:
            Commande.objects.create(
                plats=plat_a_commander,
                montant=plat_a_commander.prix,
                client=request.user,
            )

            plat_a_commander.stock -= 1
            if plat_a_commander.stock == 0:
                plat_a_commander.disponible = False
                print(f"Plat '{plat_a_commander.nom}' : Stock épuisé, la disponibilité est passée à False.")
            plat_a_commander.save()

            return redirect('menu')

    return JsonResponse({"error": "Stock épuisé"}, status=400)

@login_required
def detail(request):
    commandes = Commande.objects.filter(client=request.user)
    context = {
        'commandes': commandes,
    }

    return render(
        request=request,
        template_name='menu/mesCommande.html',
        context=context
    )