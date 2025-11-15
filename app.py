# app.py

from flask import Flask, render_template, Markup
import pandas as pd
import sys
import os

# Asegura que el directorio 'funciones' esté en el path para las importaciones relativas
# Si se ejecuta desde la raíz 'olap_web_app'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'funciones'))

# Importar las funciones (asumiendo que las funciones están en archivos separados en la carpeta 'funciones')
from generarDatos import generar_dataset
from crearCubo import cubo_base
from operacionesCubo import slice_por_anio, dice_subset

app = Flask(__name__)
df = generar_dataset() # Generar el dataset base

# --- Funciones de Soporte ---

def get_function_structure():
    """Genera la estructura de funciones para la tabla en la web."""
    # Nota: Se incluyen las funciones principales basadas en los archivos cargados
    return [
        {"Archivo": "generarDatos.py", "Función": "generar_dataset", "Descripción": "Genera el DataFrame de datos crudos."},
        {"Archivo": "crearCubo.py", "Función": "cubo_base", "Descripción": "Crea el Cubo OLAP base (Producto x Región x Año/Trimestre)."},
        {"Archivo": "crearCubo.py", "Función": "pivot_multimedidas", "Descripción": "Pivot con múltiples medidas (Ventas y Cantidad)."},
        {"Archivo": "operacionesCubo.py", "Función": "slice_por_anio", "Descripción": "Operación Slice: filtra el DataFrame por un Año."},
        {"Archivo": "operacionesCubo.py", "Función": "dice_subset", "Descripción": "Operación Dice: filtra por múltiples dimensiones (Año, Región, Producto)."},
        {"Archivo": "operacionesCubo.py", "Función": "rollup_por_anio", "Descripción": "Operación Roll-up: Agregación simple (Ventas totales por Año)."},
        {"Archivo": "operacionesCubo.py", "Función": "drilldown_producto_region", "Descripción": "Operación Drill-down: Detalle de ventas por Producto/Región hasta Mes."},
        # Se omiten otras funciones por brevedad en la tabla, pero están en el código.
    ]

def df_to_html(df_input: pd.DataFrame, title: str):
    """Convierte un DataFrame a HTML con estilo."""
    # Usar .head(10) para no sobrecargar el navegador con el dataset completo.
    html = df_input.head(10).to_html(classes='table table-striped table-bordered table-sm')
    return f"<h3>{title}</h3>{html}"


# --- Rutas de Flask ---

@app.route("/")
def index():
    # 1. Estructura de funciones
    estructura = get_function_structure()

    # 2. Cubo Completo
    cubo = cubo_base(df)
    cubo_completo_html = cubo.to_html(classes='table table-striped table-bordered table-sm')


    # 3. Una Cara del Cubo (Roll-up simple)
    # Total de Ventas por Producto
    cara_cubo_df = df.groupby("Producto")["Ventas"].sum().to_frame().reset_index()
    cara_cubo_html = df_to_html(cara_cubo_df, "Cara del Cubo (Ventas totales por Producto)")

    # 4. Una Sección del Cubo (Dice)
    # Ventas solo de 2024 en la Región Norte
    seccion_cubo_df = dice_subset(df, anios=[2024], regiones=["Norte"])
    seccion_cubo_html = df_to_html(seccion_cubo_df, "Sección del Cubo (Dice: Año 2024, Región Norte)")

    # 5. Datos que soportan a una celda del cubo (Drill-down a los datos crudos)
    # Tomamos la celda: Producto 'A', Región 'Norte', Año 2024. Buscamos el detalle por Mes.
    # Usamos el filtro 'dice' en los datos brutos y agrupamos por Mes y Canal.
    datos_celda_crudos = dice_subset(df, anios=[2024], regiones=["Norte"], productos=["A"])
    datos_celda_detalle = datos_celda_crudos.groupby(["Mes", "Canal"])["Ventas"].sum().to_frame()
    celda_html = df_to_html(datos_celda_detalle, "Datos que Soportan una Celda (Detalle: Producto A, Región Norte, 2024)")


    return render_template("index.html",
                           estructura=estructura,
                           # Usamos Markup para renderizar el HTML de Pandas sin escape
                           cubo_completo=Markup(f"<h3>Cubo Completo (Producto x Región x Año/Trimestre)</h3><div class='table-responsive'>{cubo_completo_html}</div>"),
                           cara_cubo=Markup(cara_cubo_html),
                           seccion_cubo=Markup(seccion_cubo_html),
                           celda_cubo=Markup(celda_html))

if __name__ == "__main__":
    # La ejecución de la aplicación web
    print("Iniciando la aplicación web Flask. Accede a http://127.0.0.1:5000/")
    app.run(debug=True)