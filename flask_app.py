from flask import Flask, render_template_string

app = Flask(__name__)

html_page = """
<!DOCTYPE html>
<html lang='es'>
<head>
<meta charset='UTF-8'>
<title>Dashboard OLAP</title>
<style>
 body { font-family: Arial; margin: 2rem; background:#f4f4f4; }
 .card { background:white; padding:1rem; margin:1rem 0; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,.1); }
 a.btn { display:inline-block; padding:8px 14px; background:#007bff; color:white; border-radius:5px; text-decoration:none; margin:4px; }
 a.btn:hover { background:#0056b3; }
</style>
</head>
<body>
<h1>Dashboard OLAP</h1>
<div class='card'>
<h2>Operaciones</h2>
<a class='btn' href='/cubo'>Cubo completo</a>
<a class='btn' href='/slice/2024'>Slice 2024</a>
<a class='btn' href='/dice?anios=2023,2024&regiones=Norte&productos=A'>Dice ejemplo</a>
<a class='btn' href='/rollup/anio'>Roll-up Año</a>
<a class='btn' href='/rollup/anio_trimestre'>Roll-up Año/Trimestre</a>
<a class='btn' href='/drilldown/A/Norte'>Drill-down A/Norte</a>
<a class='btn' href='/pivot/anio_region'>Pivot Año/Región</a>
</div>""" """
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
    df = generar_dataset()
    cubo = cubo_base(df)

    estructura = f"""
Dataset columnas: {list(df.columns)}

Tipos de datos:
{df.dtypes}

Dimensiones del cubo: {cubo.index.names}
Columnas del cubo: {list(cubo.columns)}
Forma del cubo: {cubo.shape}
"""

    tabla_html = cubo.head().to_html()

    return render_template_string(html_page + f"<h2>Estructura dinámica</h2><pre>{estructura}</pre><h2>Vista previa del cubo</h2>" + tabla_html)('/')
def index():
    return render_template_string(html_page)

# ====== NUEVOS ENDPOINTS OLAP ======
@app.route('/cubo')
def mostrar_cubo():
    df = generar_dataset()
    cubo = cubo_base(df)
    return cubo.to_html()

@app.route('/slice/<int:anio>')
def slice_anio(anio):
    df = generar_dataset()
    out = slice_por_anio(df, anio)
    return out.head(50).to_html()

@app.route('/dice')
def dice_view():
    from flask import request
    df = generar_dataset()
    anios = request.args.get('anios')
    regiones = request.args.get('regiones')
    productos = request.args.get('productos')

    anios = [int(a) for a in anios.split(',')] if anios else None
    regiones = regiones.split(',') if regiones else None
    productos = productos.split(',') if productos else None

    out = dice_subset(df, anios=anios, regiones=regiones, productos=productos)
    return out.head(50).to_html()

@app.route('/rollup/anio')
def rollup_anio():
    df = generar_dataset()
    return rollup_por_anio(df).to_html()

@app.route('/rollup/anio_trimestre')
def rollup_anio_trim():
    df = generar_dataset()
    return rollup_por_anio_trimestre(df).to_html()

@app.route('/drilldown/<producto>/<region>')
def drill(producto, region):
    df = generar_dataset()
    out = drilldown_producto_region(df, producto, region)
    return out.to_html()

@app.route('/pivot/anio_region')
def pivot_view():
    df = generar_dataset()
    out = pivot_anio_region(df)
    return out.to_html()

if __name__ == '__main__':
    app.run(debug=True)
