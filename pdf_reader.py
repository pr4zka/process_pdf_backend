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
