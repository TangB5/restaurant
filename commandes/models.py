from django.db import models
from django.conf import settings  # Pour référencer le modèle User (settings.AUTH_USER_MODEL)
from menu.models import Plat  # Lien avec l'application Menu


class Commande(models.Model):
    """Modèle pour une commande passée (livraison ou à emporter)."""
    STATUT_CHOICES = [
        ('PENDING', 'En attente'),
        ('PROCESSING', 'En préparation'),
        ('DELIVERED', 'Livrée/Retirée'),
        ('CANCELLED', 'Annulée'),
    ]

    # Lien vers l'utilisateur (si connecté) ou null pour les invités
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='commandes')

    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='PENDING')

    # Informations de livraison / retrait (même si non connecté)
    adresse_livraison = models.TextField(blank=True, null=True)
    nom_receveur = models.CharField(max_length=100)
    telephone_receveur = models.CharField(max_length=20)

    @property
    def get_total(self):
        """Calculer le prix total de la commande."""
        total = sum(item.get_total for item in self.articles_commande.all())
        return total

    def __str__(self):
        return f"Commande #{self.id} - Statut: {self.statut}"


class ArticleCommande(models.Model):
    """Représente un plat spécifique inclus dans une commande."""
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='articles_commande')
    plat = models.ForeignKey(Plat, on_delete=models.SET_NULL,
                             null=True)  # Si le plat est supprimé du menu, l'article reste
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=6, decimal_places=2)  # Prix au moment de la commande

    @property
    def get_total(self):
        """Calculer le prix total de cet article (quantité * prix)."""
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.quantite} x {self.plat.nom if self.plat else 'Plat Indisponible'}"