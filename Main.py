from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from Sistemas.TablaNotasNuevas import New_Notes
from Sistemas.TablaNotasPendientes import Pending_Notes
from Sistemas.TablaNuevasNotasPagadas import New_Payed_Notes
from Sistemas.TablaInventario import Stock_tables


def crear_pdf_con_tabla(nombre_archivo, data1, data2, data3, data4):
    # Asegurar extensión PDF
    if not nombre_archivo.endswith(".pdf"):
        nombre_archivo += ".pdf"

    doc = SimpleDocTemplate(nombre_archivo)
    elementos = []
    estilos = getSampleStyleSheet()

    # Títulos de cada tabla
    titulos = ["Notas Nuevas", "Notas Pagadas", "Notas Pendientes", "Stock"]

    # Crear tablas con sus títulos
    tablas = [Table(data1), Table(data2), Table(data3), Table(data4)]

    # Estilo de las tablas
    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])

    # Agregar título + tabla + separación
    for titulo, tabla in zip(titulos, tablas):
        elementos.append(Paragraph(titulo, estilos["Heading2"]))
        tabla.setStyle(estilo)
        elementos.append(tabla)
        elementos.append(Spacer(1, 20))  # Espacio entre tablas

    # Generar PDF
    doc.build(elementos)

# Crear el PDF final
crear_pdf_con_tabla(
    "Test_Table",
    New_Notes(),
    New_Payed_Notes(),
    Pending_Notes(),
    Stock_tables(),
)
