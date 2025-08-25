import os
import csv
from dotenv import load_dotenv
from datetime import datetime, timedelta
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

# Guardar una copia a nivel local
def Save_Inventory(botellas, barriles):
    # Construir ruta segura dentro del directorio de trabajo
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nombre = "Inventario " + fecha_hoy + ".csv"
    inventario_path = os.path.join(os.getcwd(), "Tablas", nombre)
    os.makedirs(os.path.dirname(inventario_path), exist_ok=True)

    # Verificar si el archivo existe y elegir modo
    file_exists = os.path.exists(inventario_path)
    mode = "a" if file_exists else "w"

    registros = []

    # Crear diccionario de botellas {nombre: cantidad}
    botellas_dict = {item.get("nombre", ""): item.get("cantidad", 0) for item in botellas}

    # Recorremos los barriles y armamos la fila con ambos datos
    for item in barriles:
        estilo = item.get("nombre", "")
        cantidad_barriles = item.get("cantidad", 0)
        cantidad_botellas = botellas_dict.get(estilo, 0)

        registros.append({
            "nombre": estilo,
            "barril": cantidad_barriles,
            "botella": cantidad_botellas
        })

    # Definir columnas fijas
    fieldnames = ["nombre", "barril", "botella"]

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
    Save_Inventory(botellas, barriles)
    Old_Stock = Access_Old_Inventory()

    data = [
        ["Estilo", "Botellas","Salidas Botellas", "Barriles", "Salidas Barriles"]
    ]

    # Convertimos botellas a diccionario {nombre: cantidad}
    botellas_dict = {item.get("nombre", ""): item.get("cantidad", 0) for item in botellas}

    # Recorremos los barriles y agregamos la fila con ambos datos
    total_botellas = 0
    total_barriles = 0
    for item in barriles:
        estilo = item.get("nombre", "")
        cantidad_barriles = item.get("cantidad", 0)
        cantidad_botellas = botellas_dict.get(estilo, 0)

        old_record = next((row for row in Old_Stock if row[0] == estilo), None)

        if old_record:
            old_barriles = int(old_record[1])
            old_botellas = int(old_record[2])
            salidas_botellas = old_botellas - cantidad_botellas
            salidas_barriles = old_barriles - cantidad_barriles
            if salidas_barriles > 0 and salidas_botellas > 0:
                total_botellas += salidas_botellas
                total_barriles += salidas_barriles
        else:
            salidas_botellas = 0
            salidas_barriles = 0

        data.append([
            estilo,
            cantidad_botellas,
            salidas_botellas,
            cantidad_barriles,
            salidas_barriles
        ])
    data.append(["", "Total", total_botellas, "Total", total_barriles])
    return data

def Access_Old_Inventory():
    date_one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    file_name = "Tablas/Inventario " + date_one_week_ago + ".csv"
    with open(file_name, "r", newline="", encoding="utf-8") as nf:
        readed_file = csv.reader(nf)
        next(readed_file, None)  # Saltar encabezado
        return list(readed_file)