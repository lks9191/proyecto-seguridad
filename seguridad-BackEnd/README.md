# Seguridad Proyecto - Backend (Flask)

Este es el servidor backend para el proyecto de seguridad, construido con **Flask**, **SQLAlchemy (PostgreSQL)**, **JWT** y **Bcrypt**. Incluye autenticación de dos factores (2FA) vía correo electrónico y gestión de roles (RBAC).

## Requisitos Previos

- **Python 3.10+** instalado.
- **PostgreSQL** instalado y corriendo.
- Una cuenta de Gmail con "Contraseña de Aplicación" para el envío de correos (opcional, pero necesario para 2FA).

## Pasos para Configuración Inicial

### 1. Clonar el repositorio y entrar a la carpeta
```bash
cd seguridad-BackEnd
```

### 2. Crear y activar el entorno virtual
En Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```
En Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
*Si `requirements.txt` no está actualizado, instala manualmente:*
```bash
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors psycopg2-binary bcrypt python-dotenv
```

### 4. Configurar variables de entorno (`.env`)
Crea un archivo llamado `.env` en la raíz de `seguridad-BackEnd` con el siguiente contenido (ajusta las credenciales):

```ini
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://USUARIO:CONTRASEÑA@localhost:5432/seguridad_proyecto
JWT_SECRET_KEY=tu-clave-secreta-para-jwt
TOTP_SECRET_KEY=tu-clave-secreta-para-totp

# Configuración de Correo (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
```

> [!IMPORTANT]
> Debes crear manualmente la base de datos `seguridad_proyecto` en PostgreSQL antes de continuar.

### 5. Inicializar la Base de Datos
Este script limpiará la base de datos, creará las tablas y añadirá los roles y usuarios por defecto (`admin`, `auditor`, `user`).
```bash
python init_db.py
```

### 6. Ejecutar el Servidor
```bash
python app.py
```
El servidor correrá por defecto en `http://127.0.0.1:5000`.

## Características Implementadas

- **RBAC:** Roles de ADMIN, AUDITOR y USER con rutas protegidas.
- **Seguridad:** Contraseñas hasheadas con Bcrypt.
- **2FA:** Segundo factor obligatorio vía correo electrónico (OTP de 6 dígitos).
- **Auditoría:** Registro de sesiones activas e historial de eventos en base de datos.
- **CORS:** Configurado para aceptar peticiones desde el frontend (Vite).

## Usuarios por defecto (creados por `init_db.py`)
- **Admin:** `admin@example.com` / `password123!`
- **Auditor:** `auditor@example.com` / `password123!`
- **User:** `user@example.com` / `password123!`
