import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import re
import numpy as np

# def preprocess(image):
#     # Convertir a escala de grises
#     img = image.convert('L')  

#     # Aumentar contraste
#     enhancer = ImageEnhance.Contrast(img)
#     img = enhancer.enhance(2)

#     # Reducir ruido 
#     img = img.filter(ImageFilter.MedianFilter())
#     # Mejora del contraste
#     img = np.array(img)
#     img = cv2.equalizeHist(img)

#     # Eliminación de artefactos y manchas
#     edges = cv2.Canny(img, 30, 150)
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if area < 100:
#             cv2.drawContours(img, [contour], -1, (0, 0, 0), -1)

#     # Umbralizar
#     thresh = 200
#     img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

#     return img


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
#                     "Precio Unitario": match.group(3).replace(",", ""),
#                     "Valor": match.group(4).replace(",", "")
#                 })

#         # Imprimir detalles de productos
#         for producto in productos:
#             print(f"Producto: {producto['Producto']}, Cantidad: {producto['Cantidad']}, Precio Unitario: ${producto['Precio Unitario']}, Valor: ${producto['Valor']}")
#     else:
#         print("Información de productos no encontrada.")

#     # Extraer el total de manera más flexible
#     total_match = re.search(r"Total:\s+\$([\d,]+)", texto_completo)
#     if total_match:
#         print(f"Total: ${total_match.group(1).replace(',', '')}")
#     else:
#         print("Total no encontrado.")


def convert_to_grayscale(image):
    return image.convert('L')

def enhance_contrast(image, factor=2.0):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def reduce_noise(image):
    return image.filter(ImageFilter.MedianFilter())

def equalize_histogram(image):
    img_array = np.array(image)
    return cv2.equalizeHist(img_array)

def remove_artifacts_and_stains(image):
    edges = cv2.Canny(image, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100:
            cv2.drawContours(image, [contour], -1, (0, 0, 0), -1)
    return image

def threshold_image(image, thresh=200):
    _, thresh_img = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    return thresh_img

def preprocess(image):
    # Convertir a escala de grises
    img_gray = convert_to_grayscale(image)

    # Aumentar contraste
    img_enhanced = enhance_contrast(img_gray)

    # Reducir ruido 
    img_noise_reduced = reduce_noise(img_enhanced)

    # Mejora del contraste
    img_equalized = equalize_histogram(img_noise_reduced)

    # Eliminación de artefactos y manchas
    img_artifacts_removed = remove_artifacts_and_stains(img_equalized)

    # Umbralizar
    img_thresholded = threshold_image(img_artifacts_removed)

    return img_thresholded



def process_pdf(file):
    pages = convert_from_path(file)
    texto_completo = ''

    for page in pages:
        image = preprocess(page)
        texto_pagina = pytesseract.image_to_string(image)
        texto_completo += texto_pagina + '\n\n'
    # print('texto_completo', texto_completo)

    # Eliminar el texto a ignorar del texto completo
    texto_limpio = re.sub(r'\d+-\d+ © .*\n', '', texto_completo, flags=re.MULTILINE)
    print('texto_limpio', texto_limpio)
    # Continuar con la extracción del bloque de productos
    bloque_productos = re.search(r"Productos\n(.*?)(?:\nTotal:|$)", texto_limpio, re.DOTALL)

    if bloque_productos:
        productos_texto = bloque_productos.group(1).strip()
        productos_limpio = "\n".join([linea.strip() for linea in productos_texto.split("\n") if linea.strip()])
        detalles_productos = re.findall(r"(.*?)\n(\d+)\s+\$(\d+)\s+\$(\d+)", productos_limpio, re.DOTALL)

        for producto, cantidad, precio_unitario, valor in detalles_productos:
            print(f"Producto: {producto}, Cantidad: {cantidad}, Precio Unitario: ${precio_unitario}, Valor: ${valor}")
        
        # Intentar extraer el total si está presente
        total_match = re.search(r"Total:\s+\$(\d+)", texto_limpio)
        if total_match:
            print(f"Total: ${total_match.group(1)}")
        else:
            print("Total no encontrado.")
    else:
        print("Bloque de productos no encontrado.")

process_pdf('test3.pdf')
