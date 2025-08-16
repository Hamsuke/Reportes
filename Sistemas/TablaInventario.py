import os
import csv
from datetime import datetime
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
supabase = create_client(url, key, options=ClientOptions(schema="barriochico"))

# Función para obtener inventario
def fetch_recent_inventory(table_name):
    try:
        result = supabase.table(table_name).select("*").execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return sorted(result.data, key=lambda x: x["id"])
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

def generate_inventory():
    botellas = fetch_recent_inventory("botellas")

    # Construir ruta segura
    inventario_path = os.path.join(os.getcwd(), "Inventarios", "inventario.csv")
    os.makedirs(os.path.dirname(inventario_path), exist_ok=True)

    # Verificar si el archivo existe y elegir modo
    file_exists = os.path.exists(inventario_path)
    mode = "a" if file_exists else "w"

    # Abrir y escribir
    with open(inventario_path, mode, newline="", encoding="utf-8") as nf:
        # Agregar la columna fecha a cada registro
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        for item in botellas:
            item["fecha"] = fecha_hoy

        # Asegurar que fecha sea la primera columna
        fieldnames = ["fecha"] + [col for col in botellas[0].keys() if col != "fecha"]

        writer = csv.DictWriter(nf, fieldnames=fieldnames)

        # Si el archivo no existía, escribimos encabezado
        if not file_exists:
            writer.writeheader()

        # Escribir los datos
        writer.writerows(botellas)