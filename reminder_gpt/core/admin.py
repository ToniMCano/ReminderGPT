from django.contrib import admin
from . models import Registry

# Register your models here.

class RegistryAdmin(admin.ModelAdmin):
    
    readonly_fields = ('created' , 'updated')
    
admin.site.register(Registry , RegistryAdmin)