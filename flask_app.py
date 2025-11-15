from flask import Flask, render_template_string

app = Flask(__name__)

html_page = """
<!DOCTYPE html>
<html lang='es'>
<head>
<meta charset='UTF-8'>
<title>Estructura de Funciones</title>
<style>
 body { font-family: Arial, sans-serif; margin: 2rem; }
 h1 { color: #333; }
 .block { margin-bottom: 2rem; padding: 1rem; border: 1px solid #ddd; border-radius: 8px; }
 pre { background: #f8f8f8; padding: 1rem; border-radius: 6px; overflow-x: auto; }
</style>
</head>
<body>
<h1>Estructura de Funciones del Proyecto</h1>
<div class='block'>
  <h2>generarDatos.py</h2>
  <pre>func generar_dataset(seed: int = 42) -> DataFrame</pre>
</div>
<div class='block'>
  <h2>crearCubo.py</h2>
  <pre>
func cubo_base(df: DataFrame)
func pivot_multimedidas(df: DataFrame)
  </pre>
</div>
<div class='block'>
  <h2>operacionesCubo.py</h2>
  <pre>
func slice_por_anio(df, anio)
func dice_subset(df, anios, regiones, productos, canales)
func rollup_por_anio(df)
func rollup_por_anio_trimestre(df)
func drilldown_producto_region(df, producto, region)
func pivot_anio_region(df)
  </pre>
</div>
<div class='block'>
  <h2>usocubos.py</h2>
  <pre>Archivo principal que ejecuta todas las operaciones del cubo.</pre>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_page)

if __name__ == '__main__':
    app.run(debug=True)
