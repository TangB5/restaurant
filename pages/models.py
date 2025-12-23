from django.db import models

class Temoignage(models.Model):
    """Modèle pour les témoignages des clients à afficher sur la page d'accueil."""
    auteur = models.CharField(max_length=100)
    titre_plat = models.CharField(max_length=100, help_text="Plat commenté ou expérience.")
    texte = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"Témoignage de {self.auteur}"

class HorairesOuverture(models.Model):
    """Modèle pour afficher les heures d'ouverture du restaurants."""
    JOURS_CHOICES = [
        ('LUN', 'Lundi'),
        ('MAR', 'Mardi'),
        ('MER', 'Mercredi'),
        ('JEU', 'Jeudi'),
        ('VEN', 'Vendredi'),
        ('SAM', 'Samedi'),
        ('DIM', 'Dimanche'),
    ]
    jour = models.CharField(max_length=3, choices=JOURS_CHOICES, unique=True)
    heure_ouverture = models.TimeField()
    heure_fermeture = models.TimeField()
    est_ferme = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Horaires d'ouverture"
        ordering = ['id'] # Pour garantir l'ordre LUN, MAR, MER...

    def __str__(self):
        return f"{self.get_jour_display()} : {self.heure_ouverture.strftime('%H:%M')} - {self.heure_fermeture.strftime('%H:%M')}"