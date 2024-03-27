import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import re
import numpy as np

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


def validate_line_format(line):

    fields = line.split(',') 
    
    # Validar número de campos
    if len(fields) != 4:
        return False

    # Validar tipos de datos
    if not fields[0].isnumeric() or not fields[1].isalpha():
        return False

    # Validar campos vacíos
    if fields[0] == '' or fields[3] == '':  
        return False

    # Otras validaciones
    ...

    return True



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
#         print("No se encontraron descripciones de productos."





def process_pdf(file):
    pages = convert_from_path(file)
    texto = ''

    for page in pages:
        # Asumiendo que la función preprocess maneja el preprocesamiento
        text = pytesseract.image_to_string(page)
        texto += text + '\n\n'
    
    # Normalizar el texto unificando los saltos de línea
    texto_normalizado = re.sub(r'\n+', '\n', texto).strip()
    
    # Revisar el texto normalizado para depurar
    print("Texto normalizado: ", texto_normalizado)  # Imprime una parte para depuración
    
    # Ajuste en el regex para mejorar la coincidencia
    # Este regex intenta capturar cualquier texto antes de la cantidad y el precio unitario,
    # asumiendo que el precio unitario sigue inmediatamente después de la cantidad y ambos están en la misma línea
    descripcion_regex = r"(.+?)\n(\d+)\s+\$\s*(\d+)\n"
    
    productos = re.finditer(descripcion_regex, texto_normalizado, re.DOTALL)
    for producto in productos:
        print(producto)  # Debugging para ver si hay coincidencias
        descripcion = producto.group(1).strip().replace('\n', ' ')
        cantidad = producto.group(2).strip()
        precio_unitario = producto.group(3).strip()
        # print(f"Descripción: {descripcion}, Cantidad: {cantidad}, Precio Unitario: ${precio_unitario}")


process_pdf('factura3.pdf')
