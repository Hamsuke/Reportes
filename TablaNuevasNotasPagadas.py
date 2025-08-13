import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
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

# Fecha de hace una semana
date_one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
# Fecha de hoy
date_today = datetime.now(timezone.utc).isoformat()

def fetch_Pending_Notes(table_name):
    try:
        result = supabase.table(table_name).select("*").gte("estado", True).gte("fecha_pago", date_one_week_ago).execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

NotasPagadas = fetch_Pending_Notes("ventas")

for venta in NotasPagadas:
    print(venta)