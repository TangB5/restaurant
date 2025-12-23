from django.contrib import admin
from .models import Temoignage, HorairesOuverture


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'titre_plat', 'date_ajout', 'visible')

    list_filter = ('visible', 'date_ajout')

    search_fields = ('auteur', 'titre_plat', 'texte')

    list_editable = ('visible',)

    # Ordre d'affichage par défaut (du plus récent au plus ancien)
    ordering = ('-date_ajout',)


# Personnalisation de l'affichage pour le modèle HorairesOuverture
@admin.register(HorairesOuverture)
class HorairesOuvertureAdmin(admin.ModelAdmin):
    # Les champs à afficher dans la liste des objets (tableau)
    list_display = ('jour', 'heure_ouverture', 'heure_fermeture', 'est_ferme')

    # Les champs modifiables directement depuis la liste des objets
    list_editable = ('heure_ouverture', 'heure_fermeture', 'est_ferme')

    # Les champs par lesquels on peut filtrer la liste
    list_filter = ('est_ferme',)

    # La liste des champs est ordonnée naturellement par l'id grâce à Meta.ordering

    # Pour ne pas avoir à cliquer sur un élément pour modifier les heures
    # On peut opter pour une vue 'Change List' très rapide (facultatif mais utile ici)
    def has_add_permission(self, request):
        """Désactive l'ajout si tous les jours sont déjà présents (7 entrées)."""
        if self.model.objects.count() >= 7:
            return False
        return True