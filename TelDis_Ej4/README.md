# Ejercicio 4 — Generador de Rol de Guardias

Este ejercicio implementa un **sistema automatizado de turnos de guardia** para un equipo de 10 personas, distribuyendo equitativamente los 365 días del año y enviando reportes semanales por correo.


---


## Herramientas utilizadas
- **Python**: `datetime`, `csv`, `json`, `smtplib`, `argparse`, `dataclasses`
- **Estructuras**:
  - `dataclass WeekRole` → Representa una semana de guardia
  - `dataclass Absence` → Representa una ausencia

---

## Lógica general

**Cálculo de los lunes del año**
```python
def first_monday(year):
    d = date(year, 1, 1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return d
```
Se busca el primer lunes del año y se generan las semanas hasta fin de año

**Generar rol base**
Cada lunes asigna al siguiente miembro del equipo como titular:
```python
headline = team[(i - 1) % len(team)]
next = team[i % len(team)]
```
El resto queda en *stand-by*

**Ausencias**
Se aplican desde un JSON `ausencias.json` para reemplazar automáticamente al titular si coincide con la semana de ausencia.

Ejemplo:
```json
[
  {"person": "Luis de la Rosa", "start": "2025-07-01", "end": "2025-07-14"}
]
```

**Swaps**
Permite intercambiar semanas entre dos personas:
```json
[
  {"week": 20, "with_week": 22}
]
```

---

## Ejemplo de ejecución

### Generar rol base 2025
```bash
python work.py --year 2025 --export rol_2025.csv
```

### Aplicar ausencias
```bash
python work.py --year 2025 --absences ausencias.json --export rol_2025_ausencias.csv
```

### Aplicar swaps
```bash
python work.py --year 2025 --swaps swaps.json --export rol_2025_swaps.csv
```

### Vista previa del correo semanal
```bash
python work.py --year 2025 --preview-week
```

---

## Estructura del correo
Ejemplo generado por `build_email_body()`:
```
Semana 32 — Guardia de 04 de agosto de 2025 a 10 de agosto de 2025

Titular: Jorge Medrano
Siguiente guardia: Luis de la Rosa

En espera:
  - Norberto Diaz
  - Juan Carlos Soriano
  - Juan Chagoya
  - Cristóbal Andrade
  - Eugenio Ramírez
  - Isaac Viveros
  - Juan Jesús Trujano

Nota: La guardia cubre de lunes 00:00 a domingo 23:59.
```

---

## Ausencias y swaps
- Si un titular está ausente → el primero disponible en *standby* cubre su semana.
- Los *swaps* intercambian las guardias completas entre dos semanas.

---

## Resumen
- Se implementó la lógica completa de asignación semanal.
- Se manejan correctamente ausencias y cambios de rol.
- Se generan archivos CSV y se simula el envío de correo.

