from django.urls import path
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView, registro_usuario, HomeView, TransaccionCreateView, TransaccionListView

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='cliente_delete'),
    path('registro/', registro_usuario, name='registro'),
    path('', HomeView.as_view(), name='home'),
    path('transacciones/', TransaccionListView.as_view(), name='transaccion_list'),
    path('transacciones/nueva/', TransaccionCreateView.as_view(), name='transaccion_create'),
]
