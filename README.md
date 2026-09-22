
# Sence Wallet - Sistema de Gestion Financiera

Aplicacion web desarrollada con Django para la gestion de clientes, cuentas bancarias y operaciones financieras digitales (depositos, retiros y transferencias). El sistema cuenta con autenticacion de usuarios, integracion de logica transaccional atomica, panel de administracion personalizado y una interfaz unificada basada en componentes modulares.

---

## 1. Descripcion del Proyecto y Arquitectura

El sistema implementa una arquitectura orientada a modelos de datos relacionales vinculados estrechamente con el modulo nativo de autenticacion de Django (`django.contrib.auth`):

* **User - Cliente**: Relacion uno a uno (`OneToOneField`) que vincula las credenciales de acceso (usuario, nombre, apellido, correo) con el perfil especifico del cliente bancario.
* **Cliente - Cuenta**: Relacion uno a uno (`OneToOneField`) donde cada titular tiene asignada una cuenta con numero unico y control de saldo decimal.
* **Cuenta - Transaccion**: Relacion uno a muchos (`ForeignKey`) que almacena el historico de movimientos clasificados por tipo (Deposito, Retiro, Transferencia) vinculados a la cuenta de origen.
* **Cuenta - Etiqueta**: Relacion muchos a muchos (`ManyToManyField`) que permite clasificar y segmentar cuentas mediante categorias.

---

## 2. Requisitos Previos y Tecnologias

* **Python**: 3.10 o superior
* **Django**: 5.x o superior
* **Base de Datos**: SQLite (entorno local) o MySQL
* **Bootstrap**: 5.3.3 y Bootstrap Icons (componentes y soporte responsivo).
* **CSS Nativo**: Hoja de estilos personalizada (`style.css`) con variables centralizadas y modo oscuro.

---

## 3. Instalacion y Puesta en Marcha

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Al-Sagredo/sence-wallet-django.git
   cd sence-wallet



2. **Crear y activar el entorno virtual**:
  * En Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate




* En Linux/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate






3. **Instalar dependencias**:
    ```bash
    pip install django
    pip install -r requirements.txt
    
4. **Aplicar migraciones a la base de datos**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate



5. **Crear superusuario para el panel de administracion**:
    ```bash
    python manage.py createsuperuser




6. **Ejecutar el servidor de desarrollo**:
    ```bash
    python manage.py runserver



Acceder a `http://127.0.0.1:8000/` en el navegador.



---

## 4. Funcionalidades Implementadas

### Modulo de Autenticacion y Seguridad

* Registro publico de nuevos clientes con generacion automatica de cuenta bancaria.


* Inicio y cierre de sesion seguro mediante `django.contrib.auth`.


* Proteccion contra accesos no autorizados mediante `LoginRequiredMixin` en vistas protegidas.


* Formularios protegidos transversalmente con tokens `csrf_token`.



### Logica Financiera y Consultas ORM

* **Dashboard Financiero**: Visualizacion de metricas agregadas (`Sum`) de ingresos y egresos en tiempo real, junto con el listado de las transacciones mas recientes.


* **Operaciones Atomicas**: Ejecucion de movimientos bancarios protegidos con `transaction.atomic()` y `select_for_update()` para asegurar consistencia del saldo ante concurrencia.


* **Validacion de Fondos**: Rechazo automatico de retiros o transferencias cuyo importe exceda el saldo disponible en la cuenta.


* **Optimizacion de Consultas**: Uso de `select_related('user', 'cuenta')` para evitar el problema de consultas N+1 en listados.



### CRUD Completo de Clientes

* **Create**: Registro de clientes adicionales con creacion concurrente de usuario y cuenta.


* **Read**: Vista de tarjetas (`ClienteListView`) con detalle de titulares y balance actual.


* **Update**: Edicion sincronizada de datos de perfil (`User` y `Cliente`) reutilizando el formulario de manera dinamica.


* **Delete**: Eliminacion segura previa confirmacion visual.



### Django Admin Personalizado

* Registro de modelos con configuraciones avanzadas de administracion:
* `ClienteAdmin`: Columnas detalladas, orden cronologico y busqueda por nombres, correo y telefono.


* `CuentaAdmin`: Busqueda relacional por titular y numero de cuenta, filtros por fecha y widget `filter_horizontal` para etiquetas.


* `TransaccionAdmin`: Busqueda por numero de cuenta/descripcion y filtros laterales por tipo de transaccion y fecha.





---

## 5. Mapeo de Rutas y Endpoints

| Ruta | Vista Asociada | Metodo HTTP | Descripcion |
| --- | --- | --- | --- |
| `/` | `HomeView` | GET | Dashboard principal con saldo y resumen financiero
| `/login/` | `LoginView` | GET, POST | Inicio de sesion de usuarios
| `/logout/` | `LogoutView` | POST | Cierre de sesion seguro
| `/registro/` | `registro_usuario` | GET, POST | Formulario de auto-registro publico
| `/clientes/` | `ClienteListView` | GET | Listado general de titulares y saldos
| `/clientes/nuevo/` | `ClienteCreateView` | GET, POST | Creacion de nuevo cliente desde sesion
| `/clientes/<pk>/editar/` | `ClienteUpdateView` | GET, POST | Actualizacion de datos de cliente
| `/clientes/<pk>/eliminar/` | `ClienteDeleteView` | GET, POST | Confirmacion y eliminacion de cliente
| `/transacciones/` | `TransaccionListView` | GET | Historial completo de movimientos de la cuenta
| `/transacciones/nueva/` | `TransaccionCreateView` | GET, POST | Ejecucion de deposito, retiro o transferencia
| `/admin/` | Panel Django Admin | GET, POST | Modulo de gestion administrativa central

---

## 6. Estrategia de Control de Versiones (Git)

El desarrollo del proyecto se estructuro mediante ramas de trabajo funcionales:

* `main`: Rama de produccion con codigo depurado, funcional y probado.


* `feature/modelos`: Diseno de modelos, relaciones, validaciones y migraciones iniciales.


* `feature/crud`: Implementacion de vistas basadas en clases, logica financiera atomica, formularios y maquetacion CSS.



El repositorio cuenta con exclusion sistematica de entornos virtuales, archivos temporales y archivos locales de configuracion mediante `.gitignore`.

```

```
