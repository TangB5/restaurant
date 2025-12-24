from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

DELEVRY_STATUS_CHOICES = (
('pending','Pending'),
('failed','Failed'),
('completed','Completed'),
)
class CategorieMenu(models.Model):
    """Modèle pour regrouper les plats (ex: Entrées, Plats principaux, Desserts)."""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage sur le menu.")

    class Meta:
        verbose_name_plural = "Catégories de Menu"
        ordering = ['ordre']

    def __str__(self):
        return self.nom


class Plat(models.Model):
    """Modèle pour un plat individuel du menu."""
    categorie = models.ForeignKey(CategorieMenu, on_delete=models.CASCADE, related_name='plats')
    nom = models.CharField(max_length=150)
    description = models.TextField(help_text="Ingrédients et détails du plat.")
    prix = models.PositiveIntegerField(help_text="Prix en FCFA")
    image = models.ImageField(upload_to='image/',default='image/default.jpg')
    stock = models.IntegerField('stock',default=0)
    disponible = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False, help_text="Est-ce le plat du jour ?")

    class Meta:
        ordering = ['nom']
        verbose_name_plural = "Plats"

    def __str__(self):
        return f"[{self.categorie.nom}] {self.nom} ({self.prix} FCFA)]"

