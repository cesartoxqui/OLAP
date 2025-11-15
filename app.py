from flask import Flask, render_template_string
from funciones.generarDatos import generar_dataset
from funciones.crearCubo import cubo_base
from funciones.operacionesCubo import (
    slice_por_anio,
    rollup_por_anio
)

app = Flask(__name__)

def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as file:
        return file.read()

@app.route("/")
def index():

    code_generar = leer_archivo("funciones/generarDatos.py")
    code_cubo = leer_archivo("funciones/crearCubo.py")
    code_ops = leer_archivo("funciones/operacionesCubo.py")

    df = generar_dataset()
    cubo = cubo_base(df)
    slice2024 = slice_por_anio(df, 2024)
    rollup = rollup_por_anio(df)

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Estructura y Funcionamiento</title>

<style>
body {{
    font-family: Arial; 
    margin: 40px; 
    background:#f7f7f7;
}}

.tabs {{
    overflow: hidden;
    background: #333;
    display: flex;
}}

.tabs button {{
    flex: 1;
    padding: 14px;
    border: none;
    cursor: pointer;
    background: #444;
    color: white;
    font-size: 16px;
}}

.tabs button:hover {{
    background: #555;
}}

.tabs button.active {{
    background: #0088ff;
}}

.tab-content {{
    display: none;
    padding: 20px;
    background: white;
    border: 1px solid #ccc;
    border-top: none;
}}

pre {{
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
}}
</style>

<script>
function openTab(tabName, btn) {{
    var i, tabs, buttons;

    tabs = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabs.length; i++) {{
        tabs[i].style.display = "none";
    }}

    buttons = document.getElementsByClassName("tab-btn");
    for (i = 0; i < buttons.length; i++) {{
        buttons[i].classList.remove("active");
    }}

    document.getElementById(tabName).style.display = "block";
    btn.classList.add("active");
}}
</script>

</head>

<body>

<h1>Estructura y Funcionamiento</h1>

<div class="tabs">
    <button class="tab-btn active" onclick="openTab('generar', this)">generarDatos.py</button>
    <button class="tab-btn" onclick="openTab('cubo', this)">crearCubo.py</button>
    <button class="tab-btn" onclick="openTab('ops', this)">operacionesCubo.py</button>
    <button class="tab-btn" onclick="openTab('funcionamiento', this)">Funcionamiento</button>
</div>

<div id="generar" class="tab-content" style="display:block">
    <h2>Archivo: generarDatos.py</h2>
    <pre>{code_generar}</pre>
</div>

<div id="cubo" class="tab-content">
    <h2>Archivo: crearCubo.py</h2>
    <pre>{code_cubo}</pre>
</div>

<div id="ops" class="tab-content">
    <h2>Archivo: operacionesCubo.py</h2>
    <pre>{code_ops}</pre>
</div>

<div id="funcionamiento" class="tab-content">
    <h2>Funcionamiento/h2>

    <h3>Dataset generado (5 filas)</h3>
    {df.head().to_html()}

    <h3>Cubo base (5 filas)</h3>
    {cubo.head().to_html()}

    <h3>Slice por año 2024 (5 filas)</h3>
    {slice2024.head().to_html()}

    <h3>Rollup por año</h3>
    {rollup.to_html()}
</div>

</body>
</html>
"""
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

