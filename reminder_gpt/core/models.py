from django.db import models

# Create your models here.

class Registry(models.Model):

    created = models.DateField(auto_now_add = True , verbose_name = "Fecha de Registro")
    updated = models.DateTimeField(auto_now = True , verbose_name = "Última Actualización")
    project_name = models.CharField(max_length = 250)
    log = models.TextField(verbose_name = 'Log')
    state = models.BooleanField(default = 1)
    
    
    class Meta:
        
        verbose_name = "entrada"
        verbose_name_plural = 'entradas'
        
        ordering = ['-created']
        
    def __str__(self):
        
        return self.project_name
