# Generated by Django 5.0.7 on 2024-07-30 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_profile_tfl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='tfl',
            new_name='tlf',
        ),
        migrations.DeleteModel(
            name='Registry',
        ),
    ]
