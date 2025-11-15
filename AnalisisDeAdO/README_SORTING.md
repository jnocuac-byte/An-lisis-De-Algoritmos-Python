# Analizador de Algoritmos de Ordenamiento

Programa educativo para analizar y comparar el rendimiento de diferentes algoritmos de ordenamiento sobre conjuntos numéricos.

## 📋 Características

### Algoritmos Implementados
- **Bubble Sort** - O(n²)
- **Selection Sort** - O(n²)
- **Insertion Sort** - O(n²)
- **Merge Sort** - O(n log n)
- **Quick Sort** - O(n log n)
- **Counting Sort** - O(n + k)
- **Radix Sort** - O(d(n + k))

### Modos de Operación

#### 1. Generación Interna
- Seleccionar tamaño máximo: 1000, 5000, 10000 o personalizado
- Generar 15 subconjuntos balanceados automáticamente
- Elegir entre conjuntos ordenados o desordenados
- Análisis de crecimiento temporal con gráficas

#### 2. Carga desde Archivo
- Cargar datos desde archivo `.txt`
- Formato: números separados por comas (ej: `5,3,8,1,9,2`)
- Análisis sobre conjunto único
- Comparación directa de tiempos

## 🚀 Instalación y Uso

### Requisitos
```bash
pip install matplotlib numpy
```

### Estructura de Archivos
```
proyecto/
├── main_sorting.py           # Ejecutar este archivo
├── sorting_algorithms.py     # Implementación de algoritmos
├── dataset_manager.py        # Gestión de datasets
├── sorting_analyzer.py       # Análisis de rendimiento
├── sorting_gui.py           # Interfaz gráfica
└── README_SORTING.md        # Este archivo
```

### Ejecutar
```bash
python main_sorting.py
```

## 📊 Uso del Programa

### Modo Generación Interna

1. **Seleccionar "Generar conjuntos internamente"**
2. **Elegir tamaño máximo**: 1000, 5000, 10000 o personalizado
3. **Seleccionar estado inicial**: Ordenado o Desordenado
4. **Seleccionar algoritmos**: Marcar los algoritmos a comparar
5. **Iniciar análisis**: Click en "▶ Iniciar Análisis"

El programa generará 15 subconjuntos balanceados:
- Para 1000: [66, 132, 198, 264, ..., 1000]
- Para 5000: [333, 666, 999, 1332, ..., 5000]
- Para 10000: [666, 1332, 1998, 2664, ..., 10000]

### Modo Carga desde Archivo

1. **Seleccionar "Cargar desde archivo .txt"**
2. **Examinar y seleccionar archivo**
3. **Seleccionar algoritmos**
4. **Iniciar análisis**

Formato del archivo:
```
5,3,8,1,9,2,7,4,6
```

## 📈 Resultados

### Tabla de Resultados
- Muestra tiempos de ejecución por algoritmo y conjunto
- Complejidad temporal teórica
- Formato legible (µs, ms, s)

### Gráficas
- **Gráfica comparativa general**: Compara todos los algoritmos seleccionados
- **Gráficas individuales**: Análisis detallado por algoritmo
- **Exportación**: Guardar gráficos como PNG

### Exportación
- Exportar resultados a CSV
- Exportar gráficos de alta resolución

## ⚠️ Limitaciones y Seguridad

### Límites del Sistema
- **Tamaño máximo**: 100,000 elementos
- **Límite de recursión**: 100,000 (ajustado automáticamente)
- **Timeout**: 5 minutos por algoritmo

### Recomendaciones por Tamaño

| Tamaño | Algoritmos Recomendados |
|--------|-------------------------|
| < 1,000 | Todos |
| 1,000 - 5,000 | Todos excepto Bubble Sort |
| 5,000 - 10,000 | Merge Sort, Quick Sort, Counting Sort, Radix Sort |
| > 10,000 | Merge Sort, Counting Sort, Radix Sort |

### Casos Especiales

**Counting Sort y Radix Sort**:
- Óptimos para números enteros pequeños
- Counting Sort requiere rango limitado (máx 1,000,000)
- Pueden ser más lentos con rangos muy grandes

**Quick Sort**:
- Caso promedio O(n log n)
- Peor caso O(n²) con datos ya ordenados
- Implementación con pivote último elemento

**Merge Sort**:
- Siempre O(n log n)
- Requiere espacio adicional O(n)
- Estable y predecible

## 🎓 Uso Educativo

### Experimentos Sugeridos

1. **Comparar ordenados vs desordenados**
   - Ejecutar con datos ordenados
   - Ejecutar con datos desordenados
   - Comparar resultados

2. **Analizar escalabilidad**
   - Probar con 1000, 5000 y 10000 elementos
   - Observar cómo crece el tiempo

3. **Mejor/Peor caso**
   - Insertion Sort: mejor con ordenados
   - Quick Sort: peor con ordenados
   - Merge Sort: siempre igual

4. **Algoritmos especializados**
   - Counting Sort: rápido con números pequeños
   - Radix Sort: eficiente para enteros

## 🔧 Manejo de Errores

El programa maneja automáticamente:
- Límites de recursión
- Memoria insuficiente
- Timeouts
- Valores inválidos
- Archivos corruptos

Los errores se muestran claramente en la interfaz y no detienen el análisis de otros algoritmos.

## 📝 Formato de Archivo de Entrada

Crear archivo `datos.txt`:
```
45,23,67,12,89,34,56,78,90,11,22,33,44,55,66,77,88,99
```

Reglas:
- Solo números enteros
- Separados por comas
- Sin espacios innecesarios
- Una línea o múltiples líneas

## 💡 Tips de Uso

1. **Para análisis rápidos**: Usar tamaños pequeños (< 1000)
2. **Para análisis exhaustivos**: Usar tamaños grandes con algoritmos eficientes
3. **Seleccionar pocos algoritmos**: Para comparaciones más claras
4. **Exportar resultados**: Para análisis posterior o reportes
5. **Usar modo ordenado**: Para ver mejor/peor caso de algoritmos

## 🐛 Solución de Problemas

**El programa es muy lento:**
- Reducir tamaño del conjunto
- Seleccionar menos algoritmos
- Evitar algoritmos O(n²) con datos grandes

**Error de recursión:**
- El límite se ajusta automáticamente
- Si persiste, reducir tamaño del conjunto

**Counting Sort falla:**
- El rango de valores es muy grande
- Usar otros algoritmos para esos datos

## 📊 Interpretación de Resultados

### Gráfica de Crecimiento
- **Línea recta**: O(n)
- **Curva suave**: O(n log n)
- **Curva empinada**: O(n²)
- **Casi plana**: O(1) o O(log n)

### Tiempos Típicos (10,000 elementos)
- Merge Sort: ~10-20 ms
- Quick Sort: ~10-20 ms
- Insertion Sort: ~100-500 ms
- Bubble Sort: ~500-1000 ms
- Counting Sort: ~1-5 ms (rango pequeño)

## 🎯 Conclusión

Este programa es una herramienta educativa para:
- Entender complejidad temporal práctica
- Comparar algoritmos reales
- Visualizar rendimiento
- Aprender sobre estructuras de datos

¡Experimenta con diferentes configuraciones y algoritmos!