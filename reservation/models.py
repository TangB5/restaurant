from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Reservation(models.Model):
    """Modèle pour une demande de réservation de table."""
    STATUT_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('CANCELLED', 'Annulée'),
        ('COMPLETED', 'Terminée'),
    ]

    # AJOUT ESSENTIEL : Lien vers l'utilisateur connecté
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', null=True, blank=True)

    nom_client = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20)

    # Date et heure de la réservation
    date_reservation = models.DateField()
    heure_reservation = models.TimeField()

    # Détails de la table
    nb_personnes = models.IntegerField(default=1)
    note_speciale = models.TextField(blank=True, null=True, verbose_name="Notes spéciales")

    # Suivi
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-date_reservation', '-heure_reservation']  # Du plus récent au plus ancien

    def __str__(self):
        return f"Réservation de {self.nom_client} pour {self.nb_personnes} le {self.date_reservation}"

    # Méthode helper pour savoir si c'est passé
    @property
    def est_passee(self):
        # Combine date et heure pour comparer avec maintenant
        dt_resa = datetime.datetime.combine(self.date_reservation, self.heure_reservation)
        return dt_resa < datetime.datetime.now()