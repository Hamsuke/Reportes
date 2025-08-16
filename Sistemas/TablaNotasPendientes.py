from dotenv import load_dotenv
import os
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
def fetch_Pending_Notes(table_name):
    try:
        result = supabase.table(table_name).select("*").gte("estado", False).execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

def Pending_Notes():
    result = supabase.table("ventas")
    print(result)
    return result

Pending_Notes()