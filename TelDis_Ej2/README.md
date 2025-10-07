# Ejercicio 2 — Formulario de Contacto en Django

Este ejercicio implementa un **formulario de contacto** simple en **Django**, con:
- Modelo `Contacto` para guardar nombre, email y mensaje.
- Form `ContactoForm` con validaciones.
- Vista `contacto_view` para mostrar/guardar el formulario.
- Template `contacto.html` para la UI.
- Migraciones y ejecución del server para pruebas locales.

---

## 1) Entorno virtual
```bat
mkdir C:\dev\TelDis_Ej2
cd C:\dev\TelDis_Ej2

python -m venv .venv
.\.venv\Scripts\activate

```

---

## 2) Instalación Django
```bat
python -m pip install --upgrade pip
python -m pip install django
python -m django --version
```

---

## 3) Crear proyecto y app
```bat
python -m django startproject DJTD .
python manage.py startapp contacto
```

Estructura:
```
TelDis_Ej2/
├─ manage.py
├─ DJTD/
│  ├─ settings.py
│  └─ urls.py
└─ contacto/
   ├─ models.py
   ├─ forms.py
   ├─ views.py
   └─ templates/
      └─ contacto.html
```

---


## 4) Registrar la app y la URL

### DJTD/settings.py
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "contacto",
]
```

### DJTD/urls.py
```python
from django.contrib import admin
from django.urls import path
from contacto.views import contacto_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contacto/", contacto_view, name="contacto"),
]
```

---

## 5) Migraciones y ejecución
```bat
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Abrir: **http://127.0.0.1:8000/contacto/**

---

## 6) Pruebas rápidas
- Dejar campos vacíos → deben aparecer errores.
- Email inválido → error de formato.
- Nombre < 3 caracteres → error.
- Mensaje < 10 caracteres → error.
- Caso válido → se guarda en BD y aparece el mensaje “Tu mensaje fue enviado correctamente.”

---

## 7) Resumen
- Se configuró un proyecto Django con app `contacto`
- Se implementó un formulario con validaciones básicas y persistencia
- Se incluyó una vista y template simples, con feedback al usuario
- Se ejecutaron migraciones y el proyecto corre en `runserver`
