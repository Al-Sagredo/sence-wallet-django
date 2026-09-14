from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'email',
            'telefono'
        ]
        widgets = {
            'nombre': forms.TelInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Nombre completo'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'correo@ejemplo.com'
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'+56 9 1234 5678'
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