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


def Save_Inventory(botellas, barriles):
    # Construir ruta segura dentro del directorio de trabajo
    inventario_path = os.path.join(os.getcwd(), "Tablas", "inventario.csv")
    os.makedirs(os.path.dirname(inventario_path), exist_ok=True)

    # Verificar si el archivo existe y elegir modo
    file_exists = os.path.exists(inventario_path)
    mode = "a" if file_exists else "w"

    # Fecha de registro
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    registros = []

    # Crear diccionario de botellas {nombre: cantidad}
    botellas_dict = {item.get("nombre", ""): item.get("cantidad", 0) for item in botellas}

    # Recorremos los barriles y armamos la fila con ambos datos
    for item in barriles:
        estilo = item.get("nombre", "")
        cantidad_barriles = item.get("cantidad", 0)
        cantidad_botellas = botellas_dict.get(estilo, 0)

        registros.append({
            "fecha": fecha_hoy,
            "nombre": estilo,
            "barril": cantidad_barriles,
            "botella": cantidad_botellas
        })

    # Definir columnas fijas
    fieldnames = ["fecha", "nombre", "barril", "botella"]

    # Guardar en CSV
    with open(inventario_path, mode, newline="", encoding="utf-8") as nf:
        writer = csv.DictWriter(nf, fieldnames=fieldnames)

        # Si el archivo no existía, escribimos encabezado
        if not file_exists:
            writer.writeheader()

        # Escribir los datos
        writer.writerows(registros)

def Stock_tables():
    botellas = fetch_recent_inventory("botellas")
    barriles = fetch_recent_inventory("barriles")

    data = [
        ["Estilo", "Botellas","Salidas Botellas", "Barriles", "Salidas Barriles"]
    ]

    # Convertimos botellas a diccionario {nombre: cantidad}
    botellas_dict = {item.get("nombre", ""): item.get("cantidad", 0) for item in botellas}

    # Recorremos los barriles y agregamos la fila con ambos datos
    for item in barriles:
        estilo = item.get("nombre", "")
        cantidad_barriles = item.get("cantidad", 0)
        cantidad_botellas = botellas_dict.get(estilo, 0)

        data.append([estilo, cantidad_botellas, cantidad_barriles])

    return data

botellas = fetch_recent_inventory("botellas")
barriles = fetch_recent_inventory("barriles")

Save_Inventory(botellas, barriles)