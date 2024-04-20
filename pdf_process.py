import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import re
import numpy as np
import PyPDF2
from fpdf import FPDF
from math import sqrt

def preprocess(image):
    # Convertir a escala de grises
    img = image.convert('L')  

    # Aumentar contraste
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)

    # Reducir ruido 
    img = img.filter(ImageFilter.MedianFilter())
    # Mejora del contraste
    img = np.array(img)
    img = cv2.equalizeHist(img)

    # Eliminación de artefactos y manchas
    edges = cv2.Canny(img, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100:
            cv2.drawContours(img, [contour], -1, (0, 0, 0), -1)

    # Umbralizar
    thresh = 200
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

    return img

# Función para crear el PDF
def create_pdf(productos, total, fecha_transaccion, contacto, nit_contacto):
    # Crear un nuevo objeto PDF
    pdf = PDF()
    pdf.add_page()

    # Configurar estilo de fuente y tamaño
    pdf.set_fill_color(192)
    # pdf.rounded_rect(60, 160, 68, 46, 5, 'F', '1234')

    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, f'Fecha de emisión: {fecha_transaccion} | Razon social o nombre: {contacto} | RUC: {nit_contacto}', 0, 1)

    # Agregar los datos al PDF
    pdf.cell(20, 10, 'Cantidad', 'LTRB', ln=0)
    pdf.cell(80, 10, 'Producto', 'LTRB', ln=0)
    pdf.cell(40, 10, 'Precio Unitario', 'LTRB', ln=0)
    pdf.cell(40, 10, 'Valor', 'LTRB', ln=1)

    for producto in productos:
        pdf.cell(20, 10, producto['Cantidad'], 'LTRB', ln=0)
        pdf.cell(80, 10, producto['Producto'], 'LTRB', ln=0)
        pdf.cell(40, 10, f"{producto['Precio Unitario']}", 'LTRB', ln=0)
        pdf.cell(40, 10, f"{producto['Valor']}", 'LTRB', ln=1)

    # Agregar el total a la derecha
    pdf.cell(110)  # Espacio en blanco
    pdf.cell(40, 10, f'Total: {total}', 'LTRB', ln=1)
    
    pdf.ln()

    # Guardar el archivo PDF
    pdf.output('datos.pdf', 'F')



# def process_pdf(file):
#     pages = convert_from_path(file)
#     texto_completo = ''

#     for page in pages:
#         image = preprocess(page)
#         texto_pagina = pytesseract.image_to_string(image)
#         texto_completo += texto_pagina + '\n\n'
#     print('texto_completo', texto_completo)
#     nombres_productos = []
#      # Extraer toda la información de productos
#     productos_info_match = re.search(r"Productos Cantidad Precio unitario Valor\n([\s\S]+?)(?=\nTotal:)", texto_completo)
    
#     # print('productos_info_match', productos_info_match)
#     if productos_info_match:
#         productos_info = productos_info_match.group(1).strip().split("\n")
#         productos = []
#         for producto_info in productos_info:
#             # Asumiendo el formato: [Nombre] [Cantidad] $[Precio unitario] $[Valor]
#             # Se ajusta para manejar mejor los espacios inesperados
#             match = re.match(r"(.*?)\s+(\d+)\s*\$\s*([\d,]+)\s*\$\s*([\d,]+)", producto_info)

#             if match:
#                 productos.append({
#                     "Producto": match.group(1),
#                     "Cantidad": match.group(2),
#                     "Precio Unitario": match.group(3).replace(",", "").replace("$", ""),
#                     "Valor": match.group(4).replace(",", "").replace("$", "")
#                 })

#         # Imprimir detalles de productos
#         for producto in productos:
#             print(f"Producto: {producto['Producto']}, Cantidad: {producto['Cantidad']}, Precio Unitario: ${producto['Precio Unitario']}, Valor: ${producto['Valor']}")
#     else:
#         print("Información de productos no encontrada.")

#     # Extraer el total de manera más flexible
#     total_match = re.search(r"Total:\s+\$([\d,]+)", texto_completo)
#     if total_match:
#         total = total_match.group(1).replace(',', '')
#         create_pdf(productos, total)
#         print(f"Total: ${total_match.group(1).replace(',', '')}")
#     else:
#         print("Total no encontrado.")
# def process_pdf(file):
    pages = convert_from_path(file)
    texto_completo = ''

    for page in pages:
        image = preprocess(page)
        texto_pagina = pytesseract.image_to_string(image)
        texto_completo += texto_pagina + '\n\n'
    print('texto_completo', texto_completo)
    nombres_productos = []
    cabecera_match = re.search(r"Fecha de transaccién (.*?)Contacto (.*?)NIT del Contacto (.*?)Vendedor (.*?)Método de pago (.*?)\n", texto_completo, re.DOTALL)
    if cabecera_match:
        fecha_transaccion = cabecera_match.group(1).strip()
        contacto = cabecera_match.group(2).strip()
        nit_contacto = cabecera_match.group(3).strip()
        vendedor = cabecera_match.group(4).strip()
        metodo_pago = cabecera_match.group(5).strip()

        print(f"Fecha de emision: {fecha_transaccion}")
        print(f"Nombre o Razon Social: {contacto}")
        print(f"Ruc: {nit_contacto}")
        # print(f"Vendedor: {vendedor}")
        print(f"Condicion de venta: {metodo_pago}")
    else:
        print("Información de la cabecera no encontrada.")
     # Extraer toda la información de productos
    productos_info_match = re.search(r"Productos Cantidad Precio unitario Valor\n([\s\S]+?)(?=\nTotal:)", texto_completo)
    
    # print('productos_info_match', productos_info_match)
    if productos_info_match:
        productos_info = productos_info_match.group(1).strip().split("\n")
        productos = []
        for producto_info in productos_info:
            # Asumiendo el formato: [Nombre] [Cantidad] $[Precio unitario] $[Valor]
            # Se ajusta para manejar mejor los espacios inesperados
            match = re.match(r"(.*?)\s+(\d+)\s*\$\s*([\d,]+)\s*\$\s*([\d,]+)", producto_info)
            if match:
                productos.append({
                    "Producto": match.group(1),
                    "Cantidad": match.group(2),
                    "Precio Unitario": match.group(3).replace(",", "").replace("$", ""),  # Eliminar símbolo de dólar
                    "Valor": match.group(4).replace(",", "").replace("$", "")  # Eliminar símbolo de dólar
                })

        # Imprimir detalles de productos
        for producto in productos:
            print(f"Producto: {producto['Producto']}, Cantidad: {producto['Cantidad']}, Precio Unitario: ${producto['Precio Unitario']}, Valor: ${producto['Valor']}")
    else:
        print("Información de productos no encontrada.")

    # Extraer el total de manera más flexible
    total_match = re.search(r"Total:\s+\$([\d,]+)", texto_completo)
    if total_match:
        total = total_match.group(1).replace(',', '').replace('$', '')
        create_pdf(productos, total, fecha_transaccion, contacto, nit_contacto)
        print(f"Total: ${total_match.group(1).replace(',', '')}")
    else:
        print("Total no encontrado.")
def process_pdf(file):
    pages = convert_from_path(file)
    texto_completo = ''
    data = {
        "fecha": "",
        "condicion": "",
        "razon_social": "",
        "ruc": "",
        "direccion": "",
        "telefono": "",
        "items": []
    }

    for page in pages:
        image = preprocess(page)
        texto_pagina = pytesseract.image_to_string(image)
        texto_completo += texto_pagina + '\n\n'
        print('texto_completo', texto_completo)
    nombres_productos = []

    cabecera_match = re.search(r"Fecha de transaccién (.*?)Contacto (.*?)NIT del Contacto (.*?)Vendedor (.*?)Método de pago (.*?)\n", texto_completo, re.DOTALL)
    if cabecera_match:
        fecha_transaccion = cabecera_match.group(1).strip()
        contacto = cabecera_match.group(2).strip()
        nit_contacto = cabecera_match.group(3).strip()
        vendedor = cabecera_match.group(4).strip()
        metodo_pago = cabecera_match.group(5).strip()

        data["fecha"] = fecha_transaccion
        data["condicion"] = metodo_pago
        data["razon_social"] = contacto
        data["ruc"] = nit_contacto

        print(f"Fecha de emision: {fecha_transaccion}")
        print(f"Nombre o Razon Social: {contacto}")
        print(f"Ruc: {nit_contacto}")
        # print(f"Vendedor: {vendedor}")
        print(f"Condicion de venta: {metodo_pago}")
    else:
        print("Información de la cabecera no encontrada.")

    # Extraer toda la información de productos
    productos_info_match = re.search(r"Productos Cantidad Precio unitario Valor\n([\s\S]+?)(?=\nTotal:)", texto_completo)

    if productos_info_match:
        productos_info = productos_info_match.group(1).strip().split("\n")
        productos = []
        for producto_info in productos_info:
            # Asumiendo el formato: [Nombre] [Cantidad] $[Precio unitario] $[Valor]
            # Se ajusta para manejar mejor los espacios inesperados
            match = re.match(r"(.*?)\s+(\d+)\s*\$\s*([\d,]+)\s*\$\s*([\d,]+)", producto_info)
            if match:
                descripcion = match.group(1)
                cantidad = int(match.group(2))
                precio_unitario = int(match.group(3).replace(",", "").replace("$", ""))
                total = int(match.group(4).replace(",", "").replace("$", ""))
                items = {
                    "descripcion": descripcion,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "total_10": 0,  # 10% si no hay enviar 0 pero enviar
                    "total_5": 0,  # 5% si no hay enviar 0 pero enviar
                    "total_0": total  # exentas
                }
                productos.append(items)

        data["items"] = productos
        print('dataaaa', data)
        # Imprimir detalles de productos
        for producto in productos:
            # print(f"Producto: {producto['Producto']}, Cantidad: {producto['Cantidad']}, Precio Unitario: ${producto['Precio Unitario']}, Valor: ${producto['Valor']}")
            return producto
    else:
        print("Información de productos no encontrada.")
    print('data', data)
    return data

process_pdf('test3.pdf')