import os
import csv
from dotenv import load_dotenv
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
supabase = create_client(url, key, options=ClientOptions(schema="barriochico"))

date_one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

#Funcion que pide los numeros de las notas nuevas
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

def fetch_note(producto,numero_nota):
    try:
        result = supabase.table(producto).select("*").eq("nota", numero_nota).execute()
        if not result.data:
            print(f"No data returned for table {producto}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {producto}: {e}")
        return []

def Stock_tables():
    total_salidas_barril = 0
    total_salidas_botellas = 0
    botellas = fetch_recent_inventory("botellas")
    barriles = fetch_recent_inventory("barriles")
    #Solicitamos las notas de la semana
    notas = fetch_table_data_last_week("ventas")
    ListaBotellas = []
    ListaBarriles = []
    Save_Inventory(botellas, barriles)

    for linea in botellas:
        nbotellas = linea.get("nombre", "")
        #Creamos la lista de estilos basandonos en todos los registrados
        ListaBotellas.append([nbotellas, 0])

    #Revisamos las ventas segun el numero de nota
    for nota in notas:
        num_nota = nota.get("nota", "")
        #Pedimos las ventas de botellas vinculadas a la nota
        botellas_nota = fetch_note("salidasbotella", num_nota)
        #Si la respuesta es afirmativa procedemos a añadirlas a la tabla de salidas
        if botellas_nota:
            for estilo in enumerate(botellas_nota):
                for i, entrada in enumerate(ListaBotellas):
                    if entrada[0] == estilo[1]['nombre']:
                        ListaBotellas[i][1] += estilo[1]["cantidad"]
                        total_salidas_botellas += estilo[1]["cantidad"]

    for linea in barriles:
        nbarriles = linea.get("nombre", "")
        #Creamos la lista de estilos basandonos en todos los registrados
        ListaBarriles.append([nbarriles, 0])

    #Revisamos las ventas segun el numero de nota
    for nota in notas:
        num_nota = nota.get("nota", "")
        #Pedimos las ventas de botellas vinculadas a la nota
        barriles_nota = fetch_note("salidasbarril", num_nota)
        #Si la respuesta es afirmativa procedemos a añadirlas a la tabla de salidas
        if barriles_nota:
            for estilo in enumerate(barriles_nota):
                for i, entrada in enumerate(ListaBarriles):
                    if entrada[0] == estilo[1]['nombre']:
                        ListaBarriles[i][1] += estilo[1]["cantidad"]
                        total_salidas_barril += estilo[1]["cantidad"]
                        print("Espera")

    # Convertir estilo_inv a list[str]
    estilo_inv = [str(linea[0]) for linea in ListaBotellas]

    # Convertir botellas_inv a list[str]
    botellas_inv = [str(linea.get("cantidad", "")) for linea in botellas]

    # Convertir salidas_botellas a list[str]
    salidas_botellas = [str(linea[1]) for linea in ListaBotellas]

    # Convertir barriles_inv a list[str]
    barriles_inv = [str(linea.get("cantidad", "")) for linea in barriles]

    # Convertir salidas_barriles a list[str]
    salidas_barriles = [str(linea[1]) for linea in ListaBarriles]

    data = [["Estilo", "Botellas", "Salidas Botellas", "Barriles", "Salidas Barriles"],]

    for i in range(len(estilo_inv)):
        data.append([
            estilo_inv[i],
            botellas_inv[i],
            salidas_botellas[i],
            barriles_inv[i],
            salidas_barriles[i]
        ])

    data.append(["", "Total:", total_salidas_botellas, "Total:", total_salidas_barril])

    return data

Stock_tables()