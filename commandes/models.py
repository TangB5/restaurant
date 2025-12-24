# menu/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class CategorieMenu(models.Model):
    """Modèle pour regrouper les plats (ex: Entrées, Plats principaux, Desserts)."""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    ordre = models.IntegerField(
        default=0,
        help_text="Ordre d'affichage sur le menu.",
        verbose_name="Ordre"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Catégorie active",
        help_text="Décochez pour masquer cette catégorie du menu"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créée le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifiée le")

    class Meta:
        verbose_name = "Catégorie de Menu"
        verbose_name_plural = "Catégories de Menu"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    @property
    def plats_disponibles_count(self):
        """Retourne le nombre de plats disponibles dans cette catégorie"""
        return self.plats.filter(disponible=True, stock__gt=0).count()


class Plat(models.Model):
    """Modèle pour un plat individuel du menu."""
    categorie = models.ForeignKey(
        CategorieMenu,
        on_delete=models.CASCADE,
        related_name='plats',
        verbose_name="Catégorie"
    )
    nom = models.CharField(max_length=150, verbose_name="Nom du plat")
    description = models.TextField(
        help_text="Ingrédients et détails du plat.",
        verbose_name="Description"
    )
    prix = models.PositiveIntegerField(
        help_text="Prix en FCFA",
        validators=[MinValueValidator(0)],
        verbose_name="Prix (FCFA)"
    )
    image = models.ImageField(
        upload_to='image/',
        default='image/default.jpg',
        verbose_name="Image du plat"
    )
    stock = models.IntegerField(
        'Stock disponible',
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Nombre d'unités disponibles"
    )
    disponible = models.BooleanField(
        default=True,
        verbose_name="Disponible",
        help_text="Décochez pour retirer temporairement du menu"
    )
    is_special = models.BooleanField(
        default=False,
        help_text="Est-ce le plat du jour ?",
        verbose_name="Plat du jour"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ['categorie__ordre', 'nom']
        verbose_name = "Plat"
        verbose_name_plural = "Plats"
        indexes = [
            models.Index(fields=['disponible', 'stock']),
            models.Index(fields=['categorie', 'disponible']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.prix} FCFA)"

    def save(self, *args, **kwargs):
        """Synchroniser automatiquement disponibilité et stock"""
        if self.stock <= 0:
            self.disponible = False
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        """Vérifie si le plat est disponible à la commande"""
        return self.disponible and self.stock > 0

    @property
    def stock_status(self):
        """Retourne le statut du stock (en stock, stock faible, rupture)"""
        if self.stock == 0:
            return "rupture"
        elif self.stock <= 5:
            return "faible"
        return "normal"


class Commande(models.Model):
    """Modèle pour une commande client."""

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', _('En attente')
        PREPARING = 'preparing', _('En préparation')
        READY = 'ready', _('Prêt')
        DELIVERING = 'delivering', _('En livraison')
        COMPLETED = 'completed', _('Livrée')
        FAILED = 'failed', _('Annulée')

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commandes',
        verbose_name="Client"
    )
    plats = models.ForeignKey(
        Plat,
        on_delete=models.CASCADE,
        related_name='commandes',
        verbose_name="Plat"
    )
    montant = models.PositiveIntegerField(
        'Montant de la commande (FCFA)',
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Montant total en FCFA"
    )
    nbPlat = models.PositiveIntegerField(
        'Nombre de plats',
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Quantité commandée"
    )
    status = models.CharField(
        'Statut de la commande',
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        max_length=20
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes/Instructions",
        help_text="Instructions spéciales pour cette commande"
    )
    created_at = models.DateTimeField(
        'Commandée le',
        default=now,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['client', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Commande #{self.pk} - {self.client.username} - {self.get_status_display()}"

    @property
    def can_be_cancelled(self):
        """Vérifie si la commande peut être annulée"""
        return self.status in [
            self.StatusChoices.PENDING,
            self.StatusChoices.PREPARING
        ]

    @property
    def can_be_reordered(self):
        """Vérifie si la commande peut être recommandée"""
        return (
                self.status in [self.StatusChoices.COMPLETED, self.StatusChoices.FAILED]
                and self.plats.is_available
                and self.plats.stock >= self.nbPlat
        )

    @property
    def total_amount(self):
        """Calcule le montant total (peut être utilisé pour validation)"""
        return self.plats.prix * self.nbPlat

    def save(self, *args, **kwargs):
        """Calcule automatiquement le montant si non défini"""
        if not self.montant or self.montant == 0:
            self.montant = self.plats.prix * self.nbPlat
        super().save(*args, **kwargs)

    @property
    def status_color(self):
        """Retourne la couleur associée au statut (pour les templates)"""
        colors = {
            self.StatusChoices.PENDING: 'yellow',
            self.StatusChoices.PREPARING: 'blue',
            self.StatusChoices.READY: 'purple',
            self.StatusChoices.DELIVERING: 'cyan',
            self.StatusChoices.COMPLETED: 'green',
            self.StatusChoices.FAILED: 'red',
        }
        return colors.get(self.status, 'gray')

    @property
    def is_recent(self):
        """Vérifie si la commande a moins de 24h"""
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at > timezone.now() - timedelta(hours=24)