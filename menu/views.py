# menu/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.contrib import messages
from .models import Plat, CategorieMenu, Commande


def menu(request):
    """
    Affiche le menu en regroupant les plats par catégorie.
    Les plats non disponibles ne sont pas inclus.
    """
    categories_avec_plats = CategorieMenu.objects.filter(
        plats__disponible=True
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
def commande(request, pk: int = None):
    """
    Gère la création d'une nouvelle commande pour un plat spécifique.
    """
    if not pk:
        messages.error(request, "Aucun plat spécifié.")
        return redirect('menu')

    plat_a_commander = get_object_or_404(Plat, id=pk)

    # Vérifier la disponibilité et le stock
    if not plat_a_commander.disponible:
        messages.error(request, f"Le plat '{plat_a_commander.nom}' n'est plus disponible.")
        return redirect('menu')

    if plat_a_commander.stock <= 0:
        plat_a_commander.disponible = False
        plat_a_commander.save()
        messages.error(request, f"Le plat '{plat_a_commander.nom}' est en rupture de stock.")
        return redirect('menu')

    # Créer la commande
    try:
        nouvelle_commande = Commande.objects.create(
            plats=plat_a_commander,
            montant=plat_a_commander.prix,
            client=request.user,
            status='pending'  # Statut initial
        )

        # Mettre à jour le stock
        plat_a_commander.stock -= 1
        if plat_a_commander.stock == 0:
            plat_a_commander.disponible = False
        plat_a_commander.save()

        messages.success(
            request,
            f"Votre commande #{nouvelle_commande.pk} a été créée avec succès ! "
            f"Le plat '{plat_a_commander.nom}' est en préparation."
        )
        return redirect('Mes_commande')

    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors de la commande : {str(e)}")
        return redirect('menu')


@login_required
def detail(request):
    """
    Affiche l'historique des commandes du client avec filtres, statistiques et pagination.
    """
    # Récupérer les paramètres de filtrage
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '').strip()

    # Base queryset avec optimisation
    commandes = Commande.objects.filter(
        client=request.user
    ).select_related('plats').order_by('-created_at')

    # Appliquer le filtre de statut
    if status_filter and status_filter != 'all':
        commandes = commandes.filter(status=status_filter)

    # Appliquer le filtre de recherche (par nom de plat ou numéro de commande)
    if search_query:
        commandes = commandes.filter(
            Q(plats__nom__icontains=search_query) |
            Q(pk__icontains=search_query)
        )

    # Calculer les statistiques globales
    stats = Commande.objects.filter(client=request.user).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='completed')),
        pending=Count('id', filter=Q(status='pending')),
        failed=Count('id', filter=Q(status='failed')),
        total_spent=Sum('montant')
    )

    # Pagination (10 commandes par page)
    paginator = Paginator(commandes, 10)
    page_number = request.GET.get('page', 1)
    commandes_page = paginator.get_page(page_number)

    context = {
        'commandes': commandes_page,
        'stats': stats,
        'current_filter': status_filter,
        'search_query': search_query,
        'paginator': paginator,
    }

    return render(
        request=request,
        template_name='menu/mesCommande.html',
        context=context
    )


@login_required
def reorder(request, commande_id: int):
    """
    Permet de recommander un plat à partir d'une commande précédente.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    # Récupérer la commande originale
    commande_originale = get_object_or_404(
        Commande,
        id=commande_id,
        client=request.user
    )

    plat = commande_originale.plats

    # Vérifier la disponibilité
    if not plat.disponible or plat.stock <= 0:
        messages.error(
            request,
            f"Désolé, le plat '{plat.nom}' n'est plus disponible actuellement."
        )
        return redirect('Mes_commande')

    # Créer la nouvelle commande
    try:
        nouvelle_commande = Commande.objects.create(
            plats=plat,
            montant=plat.prix,
            client=request.user,
            status='pending'
        )

        # Mettre à jour le stock
        plat.stock -= 1
        if plat.stock == 0:
            plat.disponible = False
        plat.save()

        messages.success(
            request,
            f"Votre commande #{nouvelle_commande.pk} a été créée ! "
            f"Vous avez recommandé '{plat.nom}'."
        )

    except Exception as e:
        messages.error(request, f"Erreur lors de la recommande : {str(e)}")

    return redirect('Mes_commande')


@login_required
def commande_detail_ajax(request, commande_id: int):
    """
    Retourne les détails d'une commande en JSON pour affichage dans un modal.
    """
    commande = get_object_or_404(
        Commande,
        id=commande_id,
        client=request.user
    )

    data = {
        'id': commande.pk,
        'status': commande.status,
        'status_display': commande.get_status_display(),
        'created_at': commande.created_at.strftime('%d %B %Y à %H:%M'),
        'montant': float(commande.montant),
        'plat': {
            'nom': commande.plats.nom,
            'description': commande.plats.description,
            'prix': float(commande.plats.prix),
            'categorie': commande.plats.categorie.nom if commande.plats.categorie else None,
        }
    }

    return JsonResponse(data)


@login_required
def cancel_commande(request, commande_id: int):
    """
    Permet d'annuler une commande si elle est encore en attente.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    commande = get_object_or_404(
        Commande,
        id=commande_id,
        client=request.user
    )

    # Vérifier que la commande peut être annulée
    if commande.status != 'pending':
        messages.error(
            request,
            "Cette commande ne peut plus être annulée car elle n'est plus en attente."
        )
        return redirect('Mes_commande')

    try:
        # Annuler la commande
        commande.status = 'failed'
        commande.save()

        # Remettre le stock
        plat = commande.plats
        plat.stock += 1
        plat.disponible = True
        plat.save()

        messages.success(
            request,
            f"La commande #{commande.pk} a été annulée avec succès. Le stock a été restauré."
        )

    except Exception as e:
        messages.error(request, f"Erreur lors de l'annulation : {str(e)}")

    return redirect('Mes_commande')