from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Temoignage(models.Model):
    auteur = models.CharField(max_length=100, verbose_name="Nom du client")
    titre_plat = models.CharField(max_length=100, blank=True, null=True, verbose_name="Plat dégusté")
    texte = models.TextField(verbose_name="Votre avis")
    note = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note (étoiles)"
    )
    image = models.ImageField(upload_to='temoignages/', blank=True, null=True, verbose_name="Photo (optionnel)")
    date_creation = models.DateTimeField(auto_now_add=True)

    # Important : Pour modérer les avis avant affichage
    est_valide = models.BooleanField(default=False, verbose_name="Publier sur le site")

    class Meta:
        ordering = ['-date_creation']  # Les plus récents en premier
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"{self.auteur} - {self.note}/5"