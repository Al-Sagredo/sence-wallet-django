from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion, Etiqueta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'email',
        'telefono',
        'user',
        'fecha_registro'
    )
    
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'telefono'
    )
    
@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'numero_cuenta',
        'saldo',
        'fecha_creacion'
    )
    
    search_fields = (
        'cliente',
        'numero_cuenta'
    )
    
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = (
        'cuenta',
        'tipo',
        'monto',
        'fecha'
    )
    
    search_fields = (
        'cuenta',
        'tipo'
    )

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
    )
    search_fields = (
            'nombre',
        )
    