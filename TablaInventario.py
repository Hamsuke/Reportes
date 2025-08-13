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
fecha_anterior = datetime.now(timezone.utc) - timedelta(days=7)
# Fecha de hoy
date_today = datetime.now(timezone.utc).isoformat()

NombreInventarioNuevo = "Inventario " + datetime.now().strftime("%d-%m-%Y") + ".csv"
NombreInventarioAnterior = "Inventario " + fecha_anterior.strftime("%d-%m-%Y") + ".csv"
nf = open(NombreInventarioNuevo, "w")
try:
    vf = open(NombreInventarioAnterior, "r")
except FileNotFoundError:
    print("No existe el archivo " + NombreInventarioAnterior)

def fetch_recent_inventory(table_name):
    try:
        result = supabase.table(table_name).select("*").execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

botellas = fetch_recent_inventory("botellas")
nf.writelines(botellas)
nf.close()
print(botellas)