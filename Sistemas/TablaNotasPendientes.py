from dotenv import load_dotenv
import os
from supabase import create_client
from supabase.lib.client_options import ClientOptions
from datetime import datetime

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


def fetch_Pending_Notes(table_name):
    call = False
    try:
        result = supabase.table(table_name).select("*").eq("estado", call).execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []


def Pending_Notes():
    notas = fetch_Pending_Notes("ventas")

    # Construir la lista de datos para la tabla PDF
    data = [
        ["Nota", "Cliente", "Pago", "Adeudo", "Vendedor", "Fecha de Creación", "Fecha de Pago"]
    ]

    for nota in notas:
        # Formatear fecha de pago
        fecha_pago_legible = ""
        if nota.get("fecha_pago"):
            try:
                fecha_pago_legible = datetime.fromisoformat(nota["fecha_pago"]).strftime("%d/%m/%Y")
            except Exception:
                fecha_pago_legible = str(nota["fecha_pago"])  # fallback

        # Formatear fecha de creación
        fecha_creacion_legible = ""
        if nota.get("fecha_creacion"):
            try:
                fecha_creacion_legible = datetime.fromisoformat(nota["fecha_creacion"]).strftime("%d/%m/%Y")
            except Exception:
                fecha_creacion_legible = str(nota["fecha_creacion"])

        adeudo_fmt = f"${nota.get('costo', 0):,.2f}"
        pago_fmt = f"${nota.get('pago', 0):,.2f}"
        data.append([
            nota.get("nota", ""),
            nota.get("cliente", ""),
            pago_fmt,
            adeudo_fmt,
        nota.get("vendedor", ""),
            fecha_creacion_legible,
            fecha_pago_legible
        ])
    return data