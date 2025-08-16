from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from Sistemas.TablaNotasNuevas import New_Notes
def crear_pdf_con_tabla(nombre_archivo, data1, data2, data3, data4):
    doc = SimpleDocTemplate(nombre_archivo)
    elementos = []

    # Crear tabla
    tabla1 = Table(data1)
    tabla2 = Table(data2)
    tabla3 = Table(data3)
    tabla4 = Table(data4)

    # Estilo de la tabla
    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])
    tabla1.setStyle(estilo)
    tabla2.setStyle(estilo)
    tabla3.setStyle(estilo)
    tabla4.setStyle(estilo)

    elementos.append(tabla1)
    elementos.append(tabla2)
    elementos.append(tabla3)
    elementos.append(tabla4)

    doc.build(elementos)

# Crear el PDF final\
TablaFinal = crear_pdf_con_tabla(New_Notes(),Pending_Notes(), )

crear_pdf_con_tabla("ventas_ultima_semana.pdf", TablaFinal)