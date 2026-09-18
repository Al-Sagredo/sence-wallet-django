from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


# Relación Muchos a Muchos 
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente',null=True, blank=True) # 1 usuario 1 cliente
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    @property
    def nombre(self):
        if self.user:
            nombre_completo = f"{self.user.first_name} {self.user.last_name}".strip()
            return nombre_completo if nombre_completo else self.user.username
        return "Sin usuario"

    @property
    def email(self):
        return self.user.email if self.user else ""
    
    def __str__(self):
        return self.nombre

    
class Cuenta(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='cuenta')
    numero_cuenta = models.CharField(max_length=20, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='cuentas')
    
    def __str__(self):
        return f'Cuenta: {self.numero_cuenta} - {self.cliente.nombre}'
    
class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('DEPOSITO', 'Deposito'),
        ('RETIRO', 'Retiro'),
        ('TRANSFERENCIA', 'Transferencia')
    ]
    
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='transacciones')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))] # Validación de monto positivo
    )
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-fecha'] # Las más recientes primero
    
    def __str__(self):
        return f'{self.tipo} de ${self.monto} en {self.cuenta.numero_cuenta}'