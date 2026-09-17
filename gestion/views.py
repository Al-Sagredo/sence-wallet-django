from django.shortcuts import render, redirect
from .models import Cliente, Transaccion, Cuenta
from .forms import ClienteForm, RegistroClienteForm, TransaccionForm
from django.db import transaction
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.db.models import Sum

# ==========================================
# CRUD CLIENTES 
# ==========================================

class ClienteListView(LoginRequiredMixin,ListView):
    model = Cliente
    template_name = 'gestion/cliente_list.html'
    context_object_name = 'clientes'
    queryset = Cliente.objects.select_related('user', 'cuenta').all()
    
class ClienteCreateView(LoginRequiredMixin,CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cliente_form.html'
    success_url = reverse_lazy('cliente_list')
    
class ClienteUpdateView(LoginRequiredMixin,UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cliente_form.html'
    success_url = reverse_lazy('home')
    
class ClienteDeleteView(LoginRequiredMixin,DeleteView):
    model = Cliente
    template_name = 'gestion/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')
    context_object_name = 'cliente'

# ==========================================
# AUTENTICACIÓN Y DASHBOARD
# ==========================================

# CBV vista de home con mixin
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'gestion/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = getattr(self.request.user, 'cliente', None)
        cuenta = getattr(cliente, 'cuenta', None) if cliente else None

        total_ingresos = 0
        total_egresos = 0
        if cuenta:
            context['cliente'] = cliente
            context['cuenta'] = cuenta
            context['transacciones'] = cuenta.transacciones.order_by('-fecha')[:8] 

            # Suma de depósitos
            ingresos = cuenta.transacciones.filter(tipo='DEPOSITO').aggregate(total=Sum('monto'))
            total_ingresos = ingresos['total'] or 0

            # Suma de retiros/transferencias
            egresos = cuenta.transacciones.filter(tipo__in=['RETIRO', 'TRANSFERENCIA']).aggregate(total=Sum('monto'))
            total_egresos = egresos['total'] or 0

        context['total_ingresos'] = total_ingresos
        context['total_egresos'] = total_egresos
        return context

@login_required  # <-- Garantiza que solo ingresen con login previo
def dashboard_view(request):
    cliente = request.user.cliente
    cuenta = cliente.cuenta
    
    # 1. Consulta para el listado reciente
    transacciones_recientes = cuenta.transacciones.order_by('-fecha')[:8]
    
    # 2. Consultas avanzadas / agregaciones (Cumple con Lección 4: Consultas Personalizadas)
    total_ingresos = cuenta.transacciones.filter(tipo='DEPOSITO').aggregate(total=Sum('monto'))['total'] or 0
    total_egresos = cuenta.transacciones.filter(tipo__in=['RETIRO', 'TRANSFERENCIA']).aggregate(total=Sum('monto'))['total'] or 0

    context = {
        'cliente': cliente,
        'cuenta': cuenta,
        'transacciones': transacciones_recientes,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
    }
    return render(request, 'gestion/dashboard.html', context)

def registro_usuario(request): 
    if request.user.is_authenticated:
        return redirect('home')
    #si el usuario completa y envia el formulario
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.save()      # Guarda el usuario en la BD 
            login(request, usuario)    # Inicia sesión automáticamente
            return redirect('home')    # Redirige a la página principal
    # method GET
    else: 
        form = RegistroClienteForm()
    return render(request, 'registration/registro.html', {'form': form}) # sigue esta vía si el form.is_valid es false o si el metodo es GET

@login_required
def mi_cuenta_view(request):
    # Accedes a Cliente y Cuenta directamente desde el request.user:
    try:
        cliente = request.user.cliente
        cuenta = cliente.cuenta
        # Trae las transacciones ordenadas por las más recientes 
        transacciones = cuenta.transacciones.order_by('-fecha')[:10]
    except ObjectDoesNotExist:
        return render(request, 'dashboard.html', {'error_perfil': 'Tu usuario aún no tiene un perfil de cliente o cuenta bancaria asignada.'})
    
    return render(request, 'dashboard.html', {
        'cuenta': cuenta,
        'transacciones': transacciones
    })

# ==========================================
# CRUD TRANSACCIONES 
# ==========================================
class TransaccionListView(LoginRequiredMixin, ListView):
    model = Transaccion
    template_name = 'gestion/transaccion_list.html'
    context_object_name = 'transacciones'

    def get_queryset(self):
        # Solo muestra las transacciones de la cuenta del usuario
        return self.request.user.cliente.cuenta.transacciones.order_by('-fecha')

class TransaccionCreateView(LoginRequiredMixin, CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'gestion/transaction_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        cliente = getattr(self.request.user, 'cliente', None)
        
        # Verificamos si existe el cliente y su cuenta
        if not cliente or not hasattr(cliente, 'cuenta'):
            form.add_error(None, 'No tienes una cuenta bancaria asignada para realizar transacciones.')
            return self.form_invalid(form)

        cuenta = cliente.cuenta
        form.instance.cuenta = cuenta
        
        with transaction.atomic():
            # Actualizamos el saldo según el tipo de operación
            if form.instance.tipo == 'DEPOSITO':
                cuenta.saldo += form.instance.monto
            elif form.instance.tipo in ['RETIRO', 'TRANSFERENCIA']:
                if cuenta.saldo < form.instance.monto:
                    form.add_error('monto', 'Saldo insuficiente para realizar esta operación.')
                    return self.form_invalid(form)
                cuenta.saldo -= form.instance.monto
            cuenta.save()
            return super().form_valid(form)

