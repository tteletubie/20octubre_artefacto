# Artefacto Bloque B: Gantt con línea base vs. real
Lee un CSV de cronograma, dibuja el Gantt con línea base y real superpuestas
y calcula la desviación por actividad.

## Requisitos
Python 3+ y `pip install -r requirements.txt`

## Ejecutar
    python gantt_linea_base.py datos_demo.csv

Salidas: `gantt_linea_base.png` y `desviaciones.csv`.

## Datos
- `datos_demo.csv`: DATOS DE EJEMPLO ilustrativos (no son del proyecto).
- `cronograma_plantilla.csv`: plantilla con las columnas esperadas; el equipo
  debe llenarla con sus fechas reales y ejecutar el script con ese archivo.

Columnas: id, actividad, responsable, inicio_base, fin_base, inicio_real,
fin_real, avance_pct (fechas AAAA-MM-DD; real vacío = aún no inicia/termina).

## Verificación manual
Desviación de fin = fin_real - fin_base (días). Ejemplo D2 del demo:
base 06-nov, real 09-nov -> 3 días corridos de atraso (el script lo reporta igual).
