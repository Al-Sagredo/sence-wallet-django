from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Cliente, User, Transaccion, Cuenta
import random

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [  
            'telefono'
        ]
        widgets = {
            'telefono': forms.TextInput(
                attrs={
                    'class': 'aw-btn-outline',
                    'placeholder':'Teléfono'
                }
            )
        }
        
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