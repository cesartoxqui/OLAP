from flask import Flask, render_template_string
from funciones.generarDatos import generar_dataset
from funciones.crearCubo import cubo_base, pivot_multimedidas
from funciones.operacionesCubo import (
    slice_por_anio,
    dice_subset,
    rollup_por_anio,
    rollup_por_anio_trimestre,
    drilldown_producto_region,
    pivot_anio_region
)

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Estructura de Funciones</title>
<style>
body { font-family: Arial; margin: 40px; background:#f7f7f7; }
h1 { color: #222; }
.block { background:white; border:1px solid #ccc; padding:15px; margin-bottom:25px; border-radius:8px; }
pre { background:#f3f3f3; padding:10px; border-radius:5px; }
</style>
</head>
<body>

<h1>Estructura de Funciones del Proyecto OLAP</h1>

<div class="block">
<h2>Estructura de Funciones</h2>
<pre>
generar_dataset()                  → generarDatos.py
cubo_base()                         → crearCubo.py
pivot_multimedidas()                → crearCubo.py

slice_por_anio()                    → operacionesCubo.py
dice_subset()                       → operacionesCubo.py
rollup_por_anio()                   → operacionesCubo.py
rollup_por_anio_trimestre()         → operacionesCubo.py
drilldown_producto_region()         → operacionesCubo.py
pivot_anio_region()                 → operacionesCubo.py
</pre>
</div>

<div class="block">
<h2>Funcionamiento</h2>

<h3>Dataset generado (5 filas)</h3>
{{ df_html|safe }}

<h3>Cubo base (5 filas)</h3>
{{ cubo_html|safe }}

<h3>Slice por año 2024 (5 filas)</h3>
{{ slice_html|safe }}

<h3>Rollup por año</h3>
{{ rollup_html|safe }}
</div>

</body>
</html>
"""

@app.route("/")
def index():
    df = generar_dataset()
    cubo = cubo_base(df)
    slice2024 = slice_por_anio(df, 2024)
    rollup = rollup_por_anio(df)

    return render_template_string(
        html,
        df_html=df.head().to_html(),
        cubo_html=cubo.head().to_html(),
        slice_html=slice2024.head().to_html(),
        rollup_html=rollup.to_html()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
