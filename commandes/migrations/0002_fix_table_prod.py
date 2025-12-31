from django.db import migrations, models
from django.utils.timezone import now

class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0001_initial'),  # dernière migration appliquée
    ]

    operations = [
        # 1️⃣ Supprimer les colonnes inutiles si elles ne sont pas dans le modèle
        migrations.RunSQL(
            sql="""
                ALTER TABLE commandes_commande DROP COLUMN IF EXISTS "adresse_livraison";
                ALTER TABLE commandes_commande DROP COLUMN IF EXISTS "nom_receveur";
                ALTER TABLE commandes_commande DROP COLUMN IF EXISTS "telephone_receveur";
                ALTER TABLE commandes_commande DROP COLUMN IF EXISTS "date_commande";
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 2️⃣ Remplir les colonnes manquantes ou NULL pour les NOT NULL
        migrations.RunSQL(
            sql="""
                UPDATE commandes_commande
                SET "montant" = 0
                WHERE "montant" IS NULL;

                UPDATE commandes_commande
                SET "nbPlat" = 1
                WHERE "nbPlat" IS NULL;

                UPDATE commandes_commande
                SET "plats_id" = 1
                WHERE "plats_id" IS NULL;

                UPDATE commandes_commande
                SET "notes" = ''
                WHERE "notes" IS NULL;

                UPDATE commandes_commande
                SET "created_at" = NOW()
                WHERE "created_at" IS NULL;

                UPDATE commandes_commande
                SET "updated_at" = NOW()
                WHERE "updated_at" IS NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 3️⃣ AlterField pour s'assurer que Django gère les defaults
        migrations.AlterField(
            model_name='commande',
            name='montant',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='commande',
            name='nbPlat',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='commande',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='commande',
            name='created_at',
            field=models.DateTimeField(default=now),
        ),
        migrations.AlterField(
            model_name='commande',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='commande',
            name='plats',
            field=models.ForeignKey(to='menu.Plat', on_delete=models.CASCADE),
        ),
    ]
