from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import ReservationForm
from .models import Reservation


def reservation_form(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)

            # 2. Si l'utilisateur est connecté, on l'associe à la réservation
            if request.user.is_authenticated:
                reservation.client = request.user

            # 3. On sauvegarde définitivement
            reservation.save()

            messages.success(request,
                             "Votre demande de réservation a été envoyée ! Nous vous contacterons pour la confirmer.")
            return redirect('home')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    else:
        # UX PREMIUM : Pré-remplir le formulaire si l'utilisateur est connecté
        initial_data = {}
        if request.user.is_authenticated:
            # On essaie de construire le nom complet, sinon on prend le username
            nom_complet = f"{request.user.last_name} {request.user.first_name}".strip()
            if not nom_complet:
                nom_complet = request.user.username

            initial_data = {
                'nom_client': nom_complet,
                'email': request.user.email
            }

        form = ReservationForm(initial=initial_data)

    context = {
        'form': form,
        'title': "Réserver votre table",
    }
    return render(request, 'reservation.html', context)


@login_required
def mes_reservations(request):
    # Obtenir la date d'aujourd'hui
    today = timezone.now().date()

    # Récupérer toutes les réservations du client connecté
    mes_resas = Reservation.objects.filter(client=request.user)

    # 1. Réservations à venir (Date >= aujourd'hui ET non annulées)
    # On trie par date croissante (la plus proche en premier)
    reservations_a_venir = mes_resas.filter(
        date_reservation__gte=today
    ).exclude(statut='CANCELLED').order_by('date_reservation', 'heure_reservation')

    # 2. Historique (Date < aujourd'hui OU annulées)
    # On trie par date décroissante (la plus récente en premier)
    reservations_passees = mes_resas.filter(
        date_reservation__lt=today
    ) | mes_resas.filter(statut='CANCELLED')

    reservations_passees = reservations_passees.order_by('-date_reservation', '-heure_reservation')

    context = {
        'reservations_a_venir': reservations_a_venir,
        'reservations_passees': reservations_passees,
    }

    # Assurez-vous que le chemin du template correspond à votre structure
    return render(request=request, template_name='reservation/mesReservation.html', context=context)