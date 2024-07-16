from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User



class Registry(models.Model):

    project_name = models.CharField(verbose_name = "Nombre del Proyecto", max_length=50)
    user = models.ForeignKey(User , verbose_name = "Usuario" , on_delete = models.CASCADE , default = None)
    Log = models.TextField(verbose_name = "Log" , default = None)
    created = models.DateField(auto_now_add = True , verbose_name = 'Fecha de Creación')
    updated = models.DateField(auto_now = True , verbose_name = 'Fecha de Actualización')

    class Meta:

        verbose_name = "registro"
        verbose_name_plural = "registros"

        ordering = ["project_name"]

    def __str__(self):

        return self.project_name