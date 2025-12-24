# menu/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import CategorieMenu, Plat, Commande


@admin.register(CategorieMenu)
class CategorieMenuAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre', 'plats_count', 'actif_badge', 'created_at']
    list_editable = ['ordre']
    list_filter = ['actif', 'created_at']
    search_fields = ['nom', 'description']
    ordering = ['ordre', 'nom']
    readonly_fields = ['created_at', 'updated_at', 'plats_disponibles_count']

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'ordre', 'actif')
        }),
        ('Statistiques', {
            'fields': ('plats_disponibles_count',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def plats_count(self, obj):
        """Nombre total de plats dans la catégorie"""
        return obj.plats.count()

    plats_count.short_description = 'Nombre de plats'

    def actif_badge(self, obj):
        """Badge visuel pour le statut actif"""
        if obj.actif:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 3px 12px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold;">✓ ACTIF</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 3px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">✗ INACTIF</span>'
        )

    actif_badge.short_description = 'Statut'

    actions = ['activate_categories', 'deactivate_categories']

    def activate_categories(self, request, queryset):
        updated = queryset.update(actif=True)
        self.message_user(request, f'{updated} catégorie(s) activée(s).')

    activate_categories.short_description = 'Activer les catégories sélectionnées'

    def deactivate_categories(self, request, queryset):
        updated = queryset.update(actif=False)
        self.message_user(request, f'{updated} catégorie(s) désactivée(s).')

    deactivate_categories.short_description = 'Désactiver les catégories sélectionnées'


@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    list_display = [
        'nom',
        'categorie',
        'prix_display',
        'stock_badge',
        'disponible_badge',
        'is_special',
        'commandes_count',
        'created_at',
        'stock'
    ]
    list_filter = [
        'disponible',
        'is_special',
        'categorie',
        'created_at',
        ('stock', admin.EmptyFieldListFilter),
    ]
    list_editable = ['stock', 'is_special']
    search_fields = ['nom', 'description', 'categorie__nom']
    readonly_fields = [
        'created_at',
        'updated_at',
        'is_available',
        'stock_status',
        'total_commandes',
        'revenue_generated'
    ]

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'categorie', 'image')
        }),
        ('Prix et disponibilité', {
            'fields': ('prix', 'stock', 'disponible', 'is_special')
        }),
        ('Statistiques', {
            'fields': ('is_available', 'stock_status', 'total_commandes', 'revenue_generated'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def prix_display(self, obj):
        """Affichage formaté du prix"""
        return format_html(
            '<strong style="color: #f97316;">{:,} FCFA</strong>',
            obj.prix
        )

    prix_display.short_description = 'Prix'
    prix_display.admin_order_field = 'prix'

    def stock_badge(self, obj):
        """Badge coloré selon le niveau de stock"""
        status = obj.stock_status
        if status == 'rupture':
            color = '#ef4444'
            text = f'RUPTURE ({obj.stock})'
        elif status == 'faible':
            color = '#f59e0b'
            text = f'FAIBLE ({obj.stock})'
        else:
            color = '#10b981'
            text = f'EN STOCK ({obj.stock})'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, text
        )

    stock_badge.short_description = 'Stock'
    stock_badge.admin_order_field = 'stock'

    def disponible_badge(self, obj):
        """Badge pour la disponibilité"""
        if obj.is_available:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 3px 10px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold;">✓ DISPO</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">✗ INDISPO</span>'
        )

    disponible_badge.short_description = 'Statut'

    def commandes_count(self, obj):
        """Nombre de commandes pour ce plat"""
        count = obj.commandes.count()
        if count > 0:
            return format_html('<strong>{}</strong>', count)
        return count

    commandes_count.short_description = 'Commandes'

    def total_commandes(self, obj):
        """Total des quantités commandées"""
        total = obj.commandes.aggregate(total=Sum('nbPlat'))['total'] or 0
        return f"{total} plat(s)"

    total_commandes.short_description = 'Total vendu'

    def revenue_generated(self, obj):
        """Revenu total généré par ce plat"""
        revenue = obj.commandes.filter(
            status='completed'
        ).aggregate(total=Sum('montant'))['total'] or 0
        return f"{revenue:,} FCFA"

    revenue_generated.short_description = 'Revenu généré'

    actions = [
        'mark_available',
        'mark_unavailable',
        'mark_as_special',
        'unmark_as_special',
        'add_stock_10',
        'add_stock_50'
    ]

    def mark_available(self, request, queryset):
        updated = queryset.update(disponible=True)
        self.message_user(request, f'{updated} plat(s) marqué(s) comme disponible(s).')

    mark_available.short_description = 'Marquer comme disponible'

    def mark_unavailable(self, request, queryset):
        updated = queryset.update(disponible=False)
        self.message_user(request, f'{updated} plat(s) marqué(s) comme indisponible(s).')

    mark_unavailable.short_description = 'Marquer comme indisponible'

    def mark_as_special(self, request, queryset):
        updated = queryset.update(is_special=True)
        self.message_user(request, f'{updated} plat(s) marqué(s) comme plat du jour.')

    mark_as_special.short_description = 'Marquer comme plat du jour'

    def unmark_as_special(self, request, queryset):
        updated = queryset.update(is_special=False)
        self.message_user(request, f'{updated} plat(s) retiré(s) des plats du jour.')

    unmark_as_special.short_description = 'Retirer des plats du jour'

    def add_stock_10(self, request, queryset):
        for plat in queryset:
            plat.stock += 10
            if plat.stock > 0:
                plat.disponible = True
            plat.save()
        self.message_user(request, f'Stock +10 ajouté à {queryset.count()} plat(s).')

    add_stock_10.short_description = 'Ajouter 10 au stock'

    def add_stock_50(self, request, queryset):
        for plat in queryset:
            plat.stock += 50
            if plat.stock > 0:
                plat.disponible = True
            plat.save()
        self.message_user(request, f'Stock +50 ajouté à {queryset.count()} plat(s).')

    add_stock_50.short_description = 'Ajouter 50 au stock'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = [
        'id_display',
        'client_link',
        'plat_nom',
        'nbPlat',
        'montant_display',
        'status_badge',
        'is_recent_badge',
        'created_at',
    ]
    list_filter = [
        'status',
        'created_at',
        ('client', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        'client__username',
        'client__email',
        'client__first_name',
        'client__last_name',
        'plats__nom'
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'total_amount',
        'can_be_cancelled',
        'can_be_reordered',
        'is_recent'
    ]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Informations de la commande', {
            'fields': ('client', 'plats', 'nbPlat', 'montant', 'status')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Propriétés', {
            'fields': ('total_amount', 'can_be_cancelled', 'can_be_reordered', 'is_recent'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def id_display(self, obj):
        """Affichage du numéro de commande"""
        return format_html('<strong>#{}</strong>', obj.pk)

    id_display.short_description = 'N°'
    id_display.admin_order_field = 'pk'

    def client_link(self, obj):
        """Lien cliquable vers le client"""
        return format_html(
            '<a href="/admin/auth/user/{}/change/">{}</a>',
            obj.client.pk,
            obj.client.username
        )

    client_link.short_description = 'Client'
    client_link.admin_order_field = 'client__username'

    def plat_nom(self, obj):
        """Nom du plat commandé"""
        return obj.plats.nom

    plat_nom.short_description = 'Plat'
    plat_nom.admin_order_field = 'plats__nom'

    def montant_display(self, obj):
        """Affichage formaté du montant"""
        return format_html(
            '<strong style="color: #f97316;">{:,} FCFA</strong>',
            obj.montant
        )

    montant_display.short_description = 'Montant'
    montant_display.admin_order_field = 'montant'

    def status_badge(self, obj):
        """Badge coloré selon le statut"""
        colors = {
            'pending': '#eab308',
            'preparing': '#3b82f6',
            'ready': '#8b5cf6',
            'delivering': '#06b6d4',
            'completed': '#10b981',
            'failed': '#ef4444'
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold; '
            'text-transform: uppercase;">{}</span>',
            color,
            obj.get_status_display()
        )

    status_badge.short_description = 'Statut'
    status_badge.admin_order_field = 'status'

    def is_recent_badge(self, obj):
        """Indicateur pour les commandes récentes"""
        if obj.is_recent:
            return format_html(
                '<span style="background-color: #ec4899; color: white; padding: 2px 8px; '
                'border-radius: 8px; font-size: 10px; font-weight: bold;">NOUVEAU</span>'
            )
        return ''

    is_recent_badge.short_description = '🆕'

    actions = [
        'mark_preparing',
        'mark_ready',
        'mark_delivering',
        'mark_completed',
        'mark_cancelled',
        'recalculate_montant'
    ]

    def mark_preparing(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='preparing')
        self.message_user(request, f'{updated} commande(s) marquée(s) en préparation.')

    mark_preparing.short_description = '👨‍🍳 Marquer en préparation'

    def mark_ready(self, request, queryset):
        updated = queryset.filter(status='preparing').update(status='ready')
        self.message_user(request, f'{updated} commande(s) marquée(s) comme prête(s).')

    mark_ready.short_description = '✅ Marquer comme prêt'

    def mark_delivering(self, request, queryset):
        updated = queryset.filter(status='ready').update(status='delivering')
        self.message_user(request, f'{updated} commande(s) en cours de livraison.')

    mark_delivering.short_description = '🚚 Marquer en livraison'

    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} commande(s) marquée(s) comme livrée(s).')

    mark_completed.short_description = '🎉 Marquer comme livrée'

    def mark_cancelled(self, request, queryset):
        # Restaurer le stock pour les commandes annulées
        count = 0
        for commande in queryset.filter(status__in=['pending', 'preparing']):
            plat = commande.plats
            plat.stock += commande.nbPlat
            plat.disponible = True
            plat.save()
            commande.status = 'failed'
            commande.save()
            count += 1

        self.message_user(
            request,
            f'{count} commande(s) annulée(s) et stock restauré.'
        )

    mark_cancelled.short_description = '❌ Annuler la commande'

    def recalculate_montant(self, request, queryset):
        """Recalcule le montant basé sur le prix actuel et la quantité"""
        for commande in queryset:
            commande.montant = commande.plats.prix * commande.nbPlat
            commande.save()
        self.message_user(
            request,
            f'{queryset.count()} montant(s) recalculé(s).'
        )

    recalculate_montant.short_description = '💰 Recalculer le montant'

    def get_queryset(self, request):
        """Optimisation des requêtes"""
        qs = super().get_queryset(request)
        return qs.select_related('client', 'plats', 'plats__categorie')


# Personnalisation du site admin
admin.site.site_header = "🍽️ Administration Restaurant"
admin.site.site_title = "Restaurant Admin"
admin.site.index_title = "Gestion du Restaurant"