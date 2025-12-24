# commandes/admin.py
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Commande

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = [
        'id_display',
        'client_link',
        'plat_nom',
        'nbPlat',
        'montant_display',
        'status_badge',  # Affichage stylé
        'status',        # Champ réel pour édition
        'is_recent_badge',
        'created_at',
    ]
    list_editable = ['status']  # On peut éditer le champ réel status
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
    )

    # -------- Méthodes pour l'affichage --------
    def id_display(self, obj):
        return format_html('<strong>#{}</strong>', obj.pk)
    id_display.short_description = 'N°'
    id_display.admin_order_field = 'pk'

    def client_link(self, obj):
        return format_html(
            '<a href="/admin/auth/user/{}/change/">{}</a>',
            obj.client.pk,
            obj.client.username
        )
    client_link.short_description = 'Client'
    client_link.admin_order_field = 'client__username'

    def plat_nom(self, obj):
        return obj.plats.nom
    plat_nom.short_description = 'Plat'
    plat_nom.admin_order_field = 'plats__nom'

    def montant_display(self, obj):
        montant = obj.montant or 0
        montant_formate = f"{montant:,.0f}".replace(",", " ")
        return format_html('<strong style="color: #f97316;">{} FCFA</strong>', montant_formate)
    montant_display.short_description = 'Montant'
    montant_display.admin_order_field = 'montant'

    def status_badge(self, obj):
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
        if getattr(obj, 'is_recent', False):
            return mark_safe(
                '<span style="background-color: #ec4899; color: white; padding: 2px 8px; '
                'border-radius: 8px; font-size: 10px; font-weight: bold;">NOUVEAU</span>'
            )
        return ''
    is_recent_badge.short_description = '🆕'

    # -------- Actions Admin --------
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
        count = 0
        for commande in queryset.filter(status__in=['pending', 'preparing']):
            plat = commande.plats
            plat.stock += commande.nbPlat
            plat.disponible = True
            plat.save()
            commande.status = 'failed'
            commande.save()
            count += 1
        self.message_user(request, f'{count} commande(s) annulée(s) et stock restauré.')
    mark_cancelled.short_description = '❌ Annuler la commande'

    def recalculate_montant(self, request, queryset):
        for commande in queryset:
            commande.montant = commande.plats.prix * commande.nbPlat
            commande.save()
        self.message_user(request, f'{queryset.count()} montant(s) recalculé(s).')
    recalculate_montant.short_description = '💰 Recalculer le montant'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('client', 'plats', 'plats__categorie')


# -------- Personnalisation de l'admin --------
admin.site.site_header = "🍽️ Administration Restaurant"
admin.site.site_title = "Restaurant Admin"
admin.site.index_title = "Gestion du Restaurant"
