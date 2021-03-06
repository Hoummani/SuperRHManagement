# Generated by Django 2.0.4 on 2018-08-20 11:30

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('congemanagement', '0004_auto_20180817_1639'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='applicationconge',
            managers=[
                ('app_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='employe',
            managers=[
                ('emp_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='conge',
            old_name='date_sortie_conge',
            new_name='date_debut_conge',
        ),
        migrations.RenameField(
            model_name='conge',
            old_name='date_entre_conge',
            new_name='date_fin_conge',
        ),
    ]
