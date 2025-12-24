from django.contrib import admin
from django.utils.html import format_html
from .models import Plat, CategorieMenu  # ✅ On n'importe que les modèles de menu


# --- Modèle Plat ---

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

    list_filter = (
        'categorie',
        'disponible',
        'is_special'
    )

    search_fields = (
        'nom',
        'description',
        'categorie__nom',
    )

    list_editable = (
        'is_special',
        'disponible'
    )

    fieldsets = (
        (None, {
            'fields': ('categorie', 'nom', 'description', 'prix','stock')
        }),
        ('Options Avancées', {
            'fields': ('image', 'disponible', 'is_special'),
            'classes': ('collapse',),
        }),
    )

    def prix_fcfa(self, obj):
        """Affiche le prix formaté en FCFA."""
        return format_html('<strong style="color: #f97316;">{} FCFA</strong>', f"{obj.prix:,.0f}".replace(',', ' '))

    prix_fcfa.short_description = 'Prix'


# --- Modèle CategorieMenu ---

@admin.register(CategorieMenu)
class CategorieMenuAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre', 'description', 'count_plats')
    list_editable = ('ordre',)
    ordering = ('ordre',)
    search_fields = ('nom',)

    def count_plats(self, obj):
        """Affiche le nombre de plats dans cette catégorie."""
        return obj.plats.count()

    count_plats.short_description = 'Nb. Plats'
