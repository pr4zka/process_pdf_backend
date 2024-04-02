import fitz  # PyMuPDF

def extract_data_from_pdf(pdf_file):
    print("Extrayendo datos del PDF...", pdf_file)
    data = {}
    
    doc = fitz.open(pdf_file)
    page = doc[0]  # Suponiendo que la información está en la primera página
    
    text = page.get_text()
    
    # Extraer los datos clave-valor
    lines = text.split('\n')
    for line in lines:
        if line.startswith('Nombre del cliente'):
            data['nombre_cliente'] = line.split(': ')[1]
        elif line.startswith('NIT del cliente'):
            data['nit_cliente'] = line.split(': ')[1]
        elif line.startswith('Correo electrónico'):
            data['correo_electronico'] = line.split(': ')[1]
        elif line.startswith('Fecha de transacción'):
            data['fecha_transaccion'] = line.split(': ')[1]
        elif line.startswith('Contacto'):
            data['contacto'] = line.split(': ')[1]
        elif line.startswith('NIT del Contacto'):
            data['nit_contacto'] = line.split(': ')[1]
        elif line.startswith('Vendedor'):
            data['vendedor'] = line.split(': ')[1]
        elif line.startswith('Método de pago'):
            data['metodo_pago'] = line.split(': ')[1]
        elif line.startswith('Estado'):
            data['estado'] = line.split(': ')[1]
        elif line.startswith('Numerodetransaccion'):
            data['numero_transaccion'] = int(line.split(': ')[1])
        elif line.startswith('ProductosCantidadValor'):
            # Extraer detalles del producto
            product_info = lines[lines.index(line) + 1].split()
            data['detalles_producto'] = {
                'producto': ' '.join(product_info[:-2]),
                'cantidad': int(product_info[-2]),
                'valor_unitario': product_info[-1]
            }
        elif line.startswith('Total:'):
            data['total'] = line.split(': ')[1]
        elif line.startswith('Creado por'):
            data['creado_por'] = line.split(': ')[1]
    
    doc.close()
    
    return data

# Procesar el PDF y extraer los datos
pdf_file = 'factura3.pdf'
datos_extraidos = extract_data_from_pdf(pdf_file)
print(datos_extraidos)
# Imprimir los datos extraídos
for key, value in datos_extraidos.items():
    print(f"{key}: {value}")
















# def process_pdf(file):
#     pages = convert_from_path(file)
#     texto = ''

#     for page in pages:
#         image = preprocess(page)
#         text = pytesseract.image_to_string(image)
#         texto += text + '\n\n'  # Añade espacio entre el texto de diferentes páginas
#             # Identificar si "Creado por rt | Treinta" indica una continuación de la lista de productos
#     # Normalizar el texto unificando los saltos de línea
#     texto_normalizado = re.sub(r'\n+', '\n', texto).strip()
    
#     partes = texto_normalizado.split("Creado por rt | Treinta")
#     texto_con_productos_continuados = ''
#     for parte in partes:
#         texto_con_productos_continuados += parte.strip() + '\n\n'
#     print("Texto con productos continuados: ", texto)
#     # Procesar la sección de productos teniendo en cuenta la posible continuación
#     descripcion_regex = r"Productos\s+(.+?)(?:\s+)?Total:"

#     todas_descripciones = re.findall(descripcion_regex, texto_con_productos_continuados, re.DOTALL)
#     print("Texto de productos: ", todas_descripciones)
#     # print("Texto de productos: ", texto)
#     if todas_descripciones:
#         for descripcion_texto in todas_descripciones:
#             descripcion_texto = descripcion_texto.strip()
#             print("Descripción de productos: ", descripcion_texto)
            
            
#             # Extracción de cantidades
#             cantidad_regex = r"\n(.+?)\s+(\d+)\s+\$(\d+)"
#             cantidades = re.findall(cantidad_regex, descripcion_texto)
#             print("Cantidades:")
#             for cantidad in cantidades:
#                 print('cantidad', cantidad)
#             print("\n---\n")  # Separador para múltiples descripciones
#     else:
#         print("No se encontraron descripciones de productos.")




# codigo para extraer datos de un pdf con precio unitario separado por espacios
# def process_pdf(file):
#     pages = convert_from_path(file)
#     texto = ''
#     for page in pages:
#         # Asumiendo que la función preprocess maneja el preprocesamiento
#         text = pytesseract.image_to_string(page)
#         texto += text + '\n\n'
    
#     # Normalizar el texto unificando los saltos de línea
#     texto_normalizado = re.sub(r'\n+', '\n', texto).strip()
#     print(texto)

#         # Revisar el texto normalizado para depurar
#     descripcion_regex = r"Productos\n(?P<descripcion>.*?)Total:.*?Precio\nunitario\s+\$(?P<precio_unitario>\d+).*?Valor\s+\$(?P<valor_total>\d+)"
#     match = re.search(descripcion_regex, texto_normalizado, re.DOTALL)

#     if match:
#         # Eliminamos espacios adicionales y unimos la descripción en una sola línea
#         descripcion = " ".join(match.group("descripcion").splitlines()).strip()
#         precio_unitario = match.group("precio_unitario").strip()
#         valor_total = match.group("valor_total").strip()
#         print(f"Descripción: {descripcion}, Precio Unitario: ${precio_unitario}, Valor Total: ${valor_total}")
#     else:
#         print("No se encontraron coincidencias con el patrón regex.")


# def process_pdf(file):
#     pages = convert_from_path(file)
#     texto_completo = ''

#     for page in pages:
#         image = preprocess(page)
#         texto_pagina = pytesseract.image_to_string(image)
#         texto_completo += texto_pagina + '\n\n'

#     # Normalización del texto
#     texto_normalizado = re.sub(r'\n+', '\n', texto_completo).strip()

#     # Separación y procesamiento en caso de texto continuado después de "Creado por rt | Treinta"
#     partes = texto_normalizado.split("Creado por rt | Treinta")
#     texto_con_productos_continuados = ''.join([parte.strip() + '\n\n' for parte in partes])

#     # Extracción de descripciones de productos, precio unitario y valor
#     pattern_descripcion = r"\n(.+?)\s+(\d+)\s+\$(\d+)\s+\$(\d+)"
#     productos = re.findall(pattern_descripcion, texto_con_productos_continuados)

#     print("Detalles de Productos:", texto_con_productos_continuados)
#     for producto, cantidad, precio_unitario, valor in productos:
#         print(f"Producto: {producto.strip()}, Cantidad: {cantidad}, Precio Unitario: {precio_unitario}, Valor: {valor}")

#     # Extracción del total
#     pattern_total = r"Total:\s+\$(\d+)"
#     match_total = re.search(pattern_total, texto_con_productos_continuados)
#     if match_total:
#         total = match_total.group(1)
#         print("Total:", total)
#     else:
#         print("No se encontró el total.")