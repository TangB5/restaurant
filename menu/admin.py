from django.contrib import admin
from .models import Plat, CategorieMenu,Commande
from django.utils.html import format_html  # Pour afficher les images dans list_display


# --- Modèle Plat (Adaptation FCFA) ---

@admin.register(Plat)
class PlatMenuAdmin(admin.ModelAdmin):
    list_display = (
        'nom',
        'categorie',
        'prix_fcfa',
        'stock',
        'is_special',
        'disponible',
        'image',
    )

    # Les champs par lesquels on peut filtrer la liste sur le côté
    list_filter = (
        'categorie',
        'disponible',
        'is_special'
    )

    # Les champs utilisés pour la recherche rapide dans la barre de recherche
    search_fields = (
        'nom',
        'description',
        'categorie__nom',  # Permet de chercher par nom de catégorie
    )

    # Les champs éditables directement depuis la vue liste (utile pour les booléens)
    list_editable = (
        'is_special',
        'disponible'
    )

    # Ordre des champs dans le formulaire d'édition
    fieldsets = (
        (None, {
            'fields': ('categorie', 'nom', 'description', 'prix','stock')
        }),
        ('Options Avancées', {
            'fields': ('image', 'disponible', 'is_special'),
            'classes': ('collapse',),  # Rendre cette section masquée par défaut
        }),
    )

    # Méthodes personnalisées pour l'affichage

    def prix_fcfa(self, obj):
        """Affiche le prix formaté en FCFA."""
        # Utilise le séparateur des milliers pour la lisibilité
        return f"{obj.prix:,.0f} FCFA".replace(',', ' ')

    prix_fcfa.short_description = 'Prix'  # Nom de la colonne

    # def apercu_image(self, obj):
    #     """Affiche une miniature de l'image si elle existe."""
    #     if obj.image:
    #         # Utiliser format_html pour afficher du HTML
    #         return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
    #     return "Pas d'image"
    #
    # apercu_image.short_description = 'Image'  # Nom de la colonne


# --- Modèle CatégorieMenu ---

@admin.register(CategorieMenu)
class CategorieMenuAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre', 'description', 'count_plats')
    list_editable = ('ordre',)
    ordering = ('ordre',)
    search_fields = ('nom',)

    def count_plats(self, obj):
        """Affiche le nombre de plats dans cette catégorie."""
        return obj.plats.count()  # Utilise le related_name='plats' défini dans Plat

    count_plats.short_description = 'Nb. Plats'

@admin.register(Commande)
class CommandAdmin(admin.ModelAdmin):
    list_display = (
        'plats',
        'client',
        'montant',
        'nbPlat',
        'status',
        'created_at'
    )
    search_fields = ( 'client', 'montant', 'status')