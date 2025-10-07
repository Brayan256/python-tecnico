# Ejercicio 3 — Eliminar Duplicados de un Arreglo

Este ejercicio implementa la función **`removeDuplicates`** que elimina **in place** los duplicados en un arreglo **ordenado ascendente** y devuelve **k**, el número de elementos únicos. Los **primeros k** elementos de `nums` deben quedar con los valores únicos en el **mismo orden**.

---

## Enfoque (dos punteros)
Se usan dos índices:
- `i`: última posición con valor **único**.
- `j`: recorre el arreglo desde `1` hasta `n-1`.
Si `nums[j] != nums[i]`, encontramos un nuevo valor único → incrementamos `i` y copiamos `nums[j]` en `nums[i]`.

---

## Pruebas locales

```python
if __name__ == "__main__":
    sol = Solution()

    nums = [1, 1, 2]
    k = sol.removeDuplicates(nums)
    print("Salida:", k, "Lista:", nums[:k])

    nums = [0,0,1,1,1,2,2,3,3,4]
    k = sol.removeDuplicates(nums)
    print("Salida:", k, "Lista:", nums[:k])
```

Ejecuta:
```bash
python solution.py
```

Salida:
```bash
Salida: 2 Lista: [1, 2]
Salida: 5 Lista: [0, 1, 2, 3, 4]
```

---

## Ejemplos del enunciado

1) `nums = [1,1,2]` → salida: `k = 2`, `nums = [1,2,_]`  
2) `nums = [0,0,1,1,1,2,2,3,3,4]` → salida: `k = 5`, `nums = [0,1,2,3,4,_,_,_,_,_]`

---

## Resumen
- La implementación sigue el patrón estándar de dos punteros
- Se mantiene `O(1)` espacio adicional