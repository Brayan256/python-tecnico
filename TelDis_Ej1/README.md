# Ejercicio 1

### Descripción general

Este análisis se basa en el archivo **`Ejercicio_Sitios_Acceso.xlsx`**, el cual contiene tres hojas:
- **dep_leg** → Sitios con dependencia legal  
- **sin_acceso** → Sitios sin acceso y tipo de problema  
- **Directores x estado** → Director responsable por estado


---

## Proceso general de análisis

1. **Limpieza de datos**
   - Se revisaran las tres hojas.
   - Se eliminarán duplicados basados en combinación de *Nombre del Sitio + Estado*.

2. **Herramientas a utilizar**
   - **Python (pandas)** para análisis de las hojas.  
   - **Excel** para revisión manual de datos.  
   - **Power BI** para presentación ejecutiva.

---

## Resultados por inciso

### i. Sitios con Dependencia Legal
- Se contará el número de sitios únicos de la hoja `dep_leg` con `nunique()`.  
- **Resultado esperado:** número de sitios con dependencia legal.

```python
dep_leg["CODIGO"].nunique()
```

---

### ii. Sitios sin acceso y tipo de problema más recurrente
- Se eliminan duplicados por *Nombre y Estado*.
- Se obtendrá el conteo de cada tipo de problema con `value_counts()`.  
- El más frecuente corresponde al tipo de incidencia más recurrente.

```python
sin_acceso["PROBLEMA"].value_counts().idxmax()
```

---

### iii. Sitios con problema por estado y dirección
- Se unen las hojas `sin_acceso` y `Directores x estado` usando el campo `Estado`.
- Luego se agrupan los datos con `groupby(["Estado","Directores"])`.

```python
merged = sin_acceso.merge(directores, on="Estado", how="left")
merged.groupby(["Estado","Directores"])["NOMBRE"].nunique()
```

---

### iv. Validación de tickets generados
- Se verifica si todos los sitios tenían valores en la columna `Tickets`.
- Se suma el total de tickets generados.

```python
sin_acceso["TICKETS"].sum()
```

Resultado: Todos los sitios tienen al menos un ticket asignado.

---

### v. Sitios “en atención” / “cerrados” por owner
- Se agrupan los sitios por `OWNER` y `ESTATUS`.

```python
sin_acceso.groupby(["OWNER","ESTATUS"])["NOMBRE"].nunique()
```

---

## Conclusion

- El análisis permitió identificar la distribución de sitios con dependencia legal, los problemas más frecuentes y los estados con más incidencias
- Se confirmó que todos los sitios cuentan con seguimiento mediante ticket
- El desglose por *Owner* permite permite priorizar los seguimientos pendientes y verificar la carga de trabajo
