from flask import Flask, render_template

app = Flask(__name__)

# Función que define la estructura de las funciones OLAP
def get_function_structure():
    """Devuelve la lista de funciones OLAP y sus descripciones."""
    return [
        {
            "nombre": "cubo_base",
            "archivo": "crearCubo.py",
            "tipo": "Cubo / Pivot",
            "descripcion": "Crea el cubo OLAP base (Pivot Table) con Producto x Región x Año/Trimestre."
        },
        {
            "nombre": "pivot_multimedidas",
            "archivo": "crearCubo.py",
            "tipo": "Cubo / Pivot",
            "descripcion": "Crea un cubo que agrega múltiples medidas (Ventas y Cantidad) por Producto y Región."
        },
        {
            "nombre": "slice_por_anio",
            "archivo": "operacionesCubo.py",
            "tipo": "Slice",
            "descripcion": "Filtra el dataset para seleccionar los datos de un único año."
        },
        {
            "nombre": "dice_subset",
            "archivo": "operacionesCubo.py",
            "tipo": "Dice",
            "descripcion": "Aplica múltiples filtros (Año, Región, Producto) para obtener un subconjunto específico del cubo."
        },
        {
            "nombre": "rollup_por_anio",
            "archivo": "operacionesCubo.py",
            "tipo": "Roll-up",
            "descripcion": "Agrega las ventas a un nivel superior, mostrando el total por Año."
        },
        {
            "nombre": "rollup_por_anio_trimestre",
            "archivo": "operacionesCubo.py",
            "tipo": "Roll-up",
            "descripcion": "Agrega las ventas por Año y luego por Trimestre, mostrando la jerarquía de niveles."
        },
        {
            "nombre": "drilldown_producto_region",
            "archivo": "operacionesCubo.py",
            "tipo": "Drill-down",
            "descripcion": "Desciende al nivel de detalle de una celda específica (Producto y Región) mostrando Meses."
        },
        {
            "nombre": "pivot_anio_region",
            "archivo": "operacionesCubo.py",
            "tipo": "Pivot / Rotación",
            "descripcion": "Rota el cubo mostrando el total de Ventas con Año en filas y Región en columnas."
        }
    ]

@app.route('/')
def index():
    """Muestra la página principal con la estructura de funciones."""
    estructura = get_function_structure()
    return render_template('index.html', estructura=estructura)

if __name__ == '__main__':
    # Usar el modo de depuración para desarrollo. 
    # Usar gunicorn para producción.
    app.run(debug=True)
