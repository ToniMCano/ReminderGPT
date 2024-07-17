from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_registry_email'),  # Asegúrate de que estás referenciando la migración anterior correctamente
    ]

    operations = [
        migrations.AlterField(
            model_name='registry',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True, default='temp@example.com'),  # Agrega un valor por defecto temporal
            preserve_default=False,
        ),
    ]