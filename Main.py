from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from supabase import create_client
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL or Key is missing!")

supabase = create_client(url, key)

date_one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

def fetch_table_data_last_week(table_name):
    try:
        result = supabase.table(table_name).select("*").gte("fecha_pago", date_one_week_ago).execute()
        if not result.data:
            raise Exception(f"No data returned for table {table_name} or an error occurred.")
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return None

ventas = fetch_table_data_last_week("ventas")

print("Ventas (last week):", ventas)

ganancias = 0

test = []

for venta in ventas:
    print(venta)
    ganancias += venta["pago"]
    print(ganancias)
    test.append(venta["nota"], venta["cliente"], venta["costo"], venta["pago"], venta["vendedor"], venta["fecha_pago"])

def crear_pdf_con_tabla(nombre_archivo):
    doc = SimpleDocTemplate(nombre_archivo)
    elementos = []

    # Datos de la tabla
    data = [
        ["Nota", "Cliente", "Adeudo", "Pago", 'Vendedor', "Fecha de Pago", "Forma de Pago"],
        ["Juan", "25", "Madrid"],
        ["Ana", "30", "Barcelona"],
        ["Luis", "35", "Valencia"],
    ]

    # Crear tabla
    tabla = Table(data)

    # Estilo de la tabla
    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])
    tabla.setStyle(estilo)

    # Agregar tabla al documento
    elementos.append(tabla)

    # Generar el PDF
    doc.build(elementos)


# Crear el PDF
crear_pdf_con_tabla("ejemplo_con_tabla.pdf")

