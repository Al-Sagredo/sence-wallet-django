from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion, Etiqueta


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'email',
        'telefono',
        'user',
        'fecha_registro',
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'telefono',
    )
    list_filter = (
        'fecha_registro',
    )
    ordering = ('-fecha_registro',)


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_cuenta',
        'cliente',
        'saldo',
        'fecha_creacion',
    )
    search_fields = (
        'numero_cuenta',
        'cliente__user__first_name',
        'cliente__user__last_name',
        'cliente__user__username',
        'cliente__telefono',
    )
    list_filter = (
        'fecha_creacion',
        'etiquetas',
    )
    filter_horizontal = ('etiquetas',)


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = (
        'cuenta',
        'tipo',
        'monto',
        'fecha',
        'descripcion',
    )
    search_fields = (
        'cuenta__numero_cuenta',
        'descripcion',
    )
    list_filter = (
        'tipo',
        'fecha',
    )
    ordering = ('-fecha',)


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)