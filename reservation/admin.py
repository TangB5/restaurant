from django.contrib import admin
from .models import Reservation


# Personnalisation de l'affichage pour le modèle Reservation
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # Les champs à afficher dans la liste des objets (tableau)
    list_display = (
        'nom_client',
        'date_reservation',
        'heure_reservation',
        'nb_personnes',
        'statut',
        'telephone'
    )

    # Les champs par lesquels on peut filtrer la liste
    list_filter = (
        'statut',
        'date_reservation',  # Filtrage par jour
        'nb_personnes'
    )

    # Les champs par lesquels on peut effectuer une recherche
    search_fields = (
        'nom_client',
        'telephone',
        'email',
        'note_speciale'
    )

    # Les champs modifiables directement depuis la liste des objets (pour changer rapidement le statut)
    list_editable = ('statut',)

    # Ordre d'affichage par défaut (utilisé si non défini dans Meta)
    ordering = ('date_reservation', 'heure_reservation')

    # Organisation des champs dans la page de détail de l'objet
    fieldsets = (
        ('Informations Client', {
            'fields': ('nom_client', 'telephone', 'email')
        }),
        ('Détails de la Réservation', {
            'fields': ('date_reservation', 'heure_reservation', 'nb_personnes', 'statut', 'note_speciale')
        }),
        ('Suivi', {
            'fields': ('date_demande',),
            # Rendre la date de demande non modifiable
            'classes': ('collapse',),  # Masquer par défaut pour l'historique
        }),
    )

    # Rendre certains champs non modifiables
    readonly_fields = ('date_demande',)