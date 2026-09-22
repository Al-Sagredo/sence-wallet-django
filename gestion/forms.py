from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Cliente, User, Transaccion, Cuenta
import random
from django.db import transaction

class ClienteForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'aw-btn-outline', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        label="Apellido",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'aw-btn-outline', 'placeholder': 'Apellido'})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'aw-btn-outline', 'placeholder': 'correo@ejemplo.com'})
    )

    class Meta:
        model = Cliente
        fields = ['telefono']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'aw-btn-outline', 'placeholder': '+56 9 ...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Precargar los datos actuales del usuario asociado al cliente
        if self.instance and self.instance.pk and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
            cliente = super().save(commit=False)
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            email = self.cleaned_data['email']

            with transaction.atomic():
                # CASO 1: El cliente ya existe y tiene usuario (Edición)
                if cliente.user:
                    cliente.user.first_name = first_name
                    cliente.user.last_name = last_name
                    cliente.user.email = email
                    if commit:
                        cliente.user.save()
                        cliente.save()
                # CASO 2: Creación de un cliente nuevo
                else:
                    # Generamos un username único a partir del email o nombre
                    base_username = email.split('@')[0]
                    username = base_username
                    contador = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{contador}"
                        contador += 1

                    # Creamos el usuario sin contraseña utilizable (o una por defecto)
                    nuevo_user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )
                    nuevo_user.set_unusable_password()
                    nuevo_user.save()

                    cliente.user = nuevo_user
                    if commit:
                        cliente.save()

                        # Creamos automáticamente su Cuenta bancaria inicial
                        numero_cuenta = random.randint(100000, 999999)
                        Cuenta.objects.create(
                            cliente=cliente,
                            numero_cuenta=numero_cuenta,
                            saldo=0
                        )
            return cliente
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Usuario'
            }
        )
    )
    password = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Contrasena'
                }
            )
        )

class RegistroClienteForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=100, required=True)
    last_name = forms.CharField(label="Apellido", max_length=100, required=True)
    email = forms.EmailField(required= True)
    telefono = forms.CharField(label="Teléfono", max_length=20, required=False)

    class Meta(UserCreationForm.Meta): #UserCreationForm.Meta adjunta  los dos campos de contraseña.
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            cliente = Cliente.objects.create(
                user=user,
                telefono= self.cleaned_data.get('telefono')
            )
        # Generamos una cuenta automática con saldo inicial 0
            numero_generado = random.randint(100000, 999999)
            Cuenta.objects.create(
                cliente=cliente,
                numero_cuenta=numero_generado,
                saldo=0
            )
        return user




class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'aw-btn-outline', 'style': 'width: 100%;'}),
            'monto': forms.NumberInput(attrs={'class': 'aw-btn-outline', 'style': 'width: 100%;', 'placeholder': 'Ej: 15000'}),
            'descripcion': forms.TextInput(attrs={'class': 'aw-btn-outline', 'style': 'width: 100%;', 'placeholder': 'Motivo o detalle'}),
        }