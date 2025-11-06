from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from supabase import create_client
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
date_one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
def fetch_table_data_last_week(table_name):
    try:
        result = supabase.table(table_name).select("*").gte("fecha_pago", date_one_week_ago).gte("estado", True).execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

def New_Payed_Notes():
    ventas = fetch_table_data_last_week("ventas")

    # Construir la lista de datos para la tabla PDF
    data = [
        ["Nota", "Cliente", "Pago", "Vendedor", "Fecha de Pago"]
    ]
    tmp = 0
    total1 = 0
    for venta in ventas:
        # Formatear fecha y cantidades
        fecha_legible = ""
        if venta.get("fecha_pago"):
            try:
                fecha_legible = datetime.fromisoformat(venta["fecha_pago"]).strftime("%d/%m/%Y")
            except Exception:
                fecha_legible = venta["fecha_pago"]
        adeudo_fmt = f"${venta.get('pago', 0):,.2f}"
        data.append([
            venta.get("nota", ""),
            venta.get("cliente", ""),
            adeudo_fmt,
            venta.get("vendedor", ""),
            fecha_legible,
        ])
        tmp += int(venta.get("pago", 0))
        total1 = f"${tmp:,.2f}"
    data.append(["", "total", total1, "", ""])
    return data