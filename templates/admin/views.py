# admin_dashboard/views.py
# Create this file to provide real statistics to your admin dashboard

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta, datetime
from menu.models import Commande, Plat, CategorieMenu
from django.contrib.auth import get_user_model

User = get_user_model()


@staff_member_required
def admin_dashboard_stats(request):
    """
    Provides real-time statistics for the admin dashboard
    """
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)

    # ========== COMMANDES AUJOURD'HUI ==========
    commandes_today = Commande.objects.filter(
        created_at__date=today
    )
    commandes_yesterday = Commande.objects.filter(
        created_at__date=yesterday
    )

    count_today = commandes_today.count()
    count_yesterday = commandes_yesterday.count()

    # Calcul du pourcentage de changement
    if count_yesterday > 0:
        commandes_change = ((count_today - count_yesterday) / count_yesterday) * 100
    else:
        commandes_change = 100 if count_today > 0 else 0

    # ========== CHIFFRE D'AFFAIRES ==========
    ca_today = commandes_today.filter(
        status='completed'
    ).aggregate(total=Sum('montant'))['total'] or 0

    ca_yesterday = commandes_yesterday.filter(
        status='completed'
    ).aggregate(total=Sum('montant'))['total'] or 0

    if ca_yesterday > 0:
        ca_change = ((ca_today - ca_yesterday) / ca_yesterday) * 100
    else:
        ca_change = 100 if ca_today > 0 else 0

    # ========== PLATS EN CUISINE ==========
    plats_en_cuisine = Commande.objects.filter(
        status__in=['pending', 'preparing']
    ).count()

    # ========== CLIENTS ACTIFS ==========
    # Clients ayant commandé ce mois
    clients_actifs_ce_mois = Commande.objects.filter(
        created_at__gte=this_month_start
    ).values('client').distinct().count()

    clients_actifs_mois_dernier = Commande.objects.filter(
        created_at__gte=last_month_start,
        created_at__lt=this_month_start
    ).values('client').distinct().count()

    if clients_actifs_mois_dernier > 0:
        clients_change = ((clients_actifs_ce_mois - clients_actifs_mois_dernier) /
                          clients_actifs_mois_dernier) * 100
    else:
        clients_change = 100 if clients_actifs_ce_mois > 0 else 0

    # ========== STATISTIQUES ADDITIONNELLES ==========
    # Plats en rupture de stock
    plats_rupture = Plat.objects.filter(stock=0).count()

    # Plats à faible stock (moins de 5)
    plats_faible_stock = Plat.objects.filter(stock__lte=5, stock__gt=0).count()

    # Commandes en attente
    commandes_en_attente = Commande.objects.filter(status='pending').count()

    # Top 5 plats les plus commandés (ce mois)
    top_plats = Commande.objects.filter(
        created_at__gte=this_month_start
    ).values(
        'plats__nom'
    ).annotate(
        total_commandes=Count('id'),
        total_quantite=Sum('nbPlat')
    ).order_by('-total_commandes')[:5]

    # Revenus par semaine (4 dernières semaines)
    weekly_revenue = []
    for i in range(4):
        week_start = today - timedelta(days=(i + 1) * 7)
        week_end = today - timedelta(days=i * 7)
        revenue = Commande.objects.filter(
            created_at__date__range=[week_start, week_end],
            status='completed'
        ).aggregate(total=Sum('montant'))['total'] or 0
        weekly_revenue.append({
            'week': f"Semaine {4 - i}",
            'revenue': revenue
        })

    context = {
        'stats': {
            'commandes_today': count_today,
            'commandes_change': round(commandes_change, 1),
            'commandes_direction': 'up' if commandes_change >= 0 else 'down',

            'ca_today': ca_today,
            'ca_change': round(ca_change, 1),
            'ca_direction': 'up' if ca_change >= 0 else 'down',

            'plats_en_cuisine': plats_en_cuisine,

            'clients_actifs': clients_actifs_ce_mois,
            'clients_change': round(clients_change, 1),
            'clients_direction': 'up' if clients_change >= 0 else 'down',
        },
        'additional_stats': {
            'plats_rupture': plats_rupture,
            'plats_faible_stock': plats_faible_stock,
            'commandes_en_attente': commandes_en_attente,
        },
        'top_plats': top_plats,
        'weekly_revenue': weekly_revenue,
    }

    return context


# ========== CUSTOM ADMIN INDEX VIEW ==========
# You can override the default admin index view to include these stats

from django.contrib import admin
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    """
    Custom Admin Site with enhanced dashboard
    """
    site_header = "🍽️ Administration Restaurant"
    site_title = "Restaurant Admin"
    index_title = "Tableau de Bord"

    def index(self, request, extra_context=None):
        """
        Override the default index view to add statistics
        """
        extra_context = extra_context or {}

        # Get statistics
        stats_context = admin_dashboard_stats(request)
        extra_context.update(stats_context)

        return super().index(request, extra_context)

# ========== USAGE IN YOUR PROJECT ==========
# In your main urls.py or admin.py:
#
# from admin_dashboard.views import CustomAdminSite
#
# admin.site.__class__ = CustomAdminSite
#
# OR create a new admin site:
#
# custom_admin_site = CustomAdminSite(name='custom_admin')
#
# Then register your models with custom_admin_site instead of admin.site