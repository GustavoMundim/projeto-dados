from django.contrib import admin
from django.contrib.auth.models import User
from .models import Usuario, CriarAnotacao
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import admin as admin_auth_django
# Register your models here.




class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Adicionais do Usuário', {'fields': ('foto_usuario', 'nivel')}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(CriarAnotacao)