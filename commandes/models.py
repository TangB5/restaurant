# menu/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from menu.models import Plat


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
        related_name='commandes'
    )

    plats = models.ForeignKey(
        Plat,
        on_delete=models.CASCADE,
        related_name='commandes'
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