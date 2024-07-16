from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . models import Registry

# Register your models here.
class RegistryAdmin(admin.ModelAdmin):

    readonly_fields = ('created' , 'updated')
    list_display = ('project_name', 'user'  , 'created' , 'updated')
    search_fields = ('project_name' , 'user__username' , 'content')
    list_filter = ('user__username' , 'project_name')

admin.site.register(Registry , RegistryAdmin)