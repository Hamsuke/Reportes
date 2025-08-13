from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

from supabase import create_client
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from supabase.lib.client_options import ClientOptions

# Cargar variables de entorno
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL or Key is missing!")

# Conexión a Supabase
supabase = create_client(
    url,
    key,
    options=ClientOptions(schema="barriochico")
)

# Fecha de hace una semana
date_one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
# Fecha de hoy
date_today = datetime.now(timezone.utc).isoformat()

# Función para obtener datos de la última semana
def fetch_table_data_last_week(table_name):
    try:
        result = supabase.table(table_name).select("*").gte("fecha_creacion", date_one_week_ago).execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

ventas = fetch_table_data_last_week("ventas")

# Construir la lista de datos para la tabla PDF
data = [
    ["Nota", "Cliente", "Adeudo", "Pago", "Vendedor", "Fecha de registro", "Fecha de Pago", "Forma de Pago"]
]

for venta in ventas:
    # Formatear fecha y cantidades
    fecha_legible = ""
    if venta.get("fecha_pago"):
        try:
            fecha_legible = datetime.fromisoformat(venta["fecha_pago"]).strftime("%d/%m/%Y")
            fecha_legible2 = datetime.fromisoformat(venta["fecha_creacion"]).strftime("%d/%m/%Y")
        except Exception:
            fecha_legible = venta["fecha_pago"]  # Si no es ISO válido

    adeudo_fmt = f"${venta.get('adeudo', 0):,.2f}"
    pago_fmt = f"${venta.get('pago', 0):,.2f}"

    data.append([
        venta.get("nota", ""),
        venta.get("cliente", ""),
        adeudo_fmt,
        pago_fmt,
        venta.get("vendedor", ""),
        fecha_legible2,
        fecha_legible,
        venta.get("forma_pago", "")
    ])

# Función para crear el PDF
def crear_pdf_con_tabla(nombre_archivo, data):
    doc = SimpleDocTemplate(nombre_archivo)
    elementos = []

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

    elementos.append(tabla)
    doc.build(elementos)

nombreArchivo = "Movimientos semana del " + datetime.fromisoformat(date_one_week_ago).strftime("%d-%m-%Y") + " al " + datetime.fromisoformat(date_today).strftime("%d-%m-%Y") + ".pdf"

# Crear el PDF final
crear_pdf_con_tabla(str(nombreArchivo), data)

print("PDF generado: ventas_ultima_semana.pdf")
