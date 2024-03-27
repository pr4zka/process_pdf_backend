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

    # Umbralizar
    img = np.array(img) 
    thresh = 200
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    # Opcional: corregir perspectiva 
    # img = correct_perspective(img)

    # Opcional: ajustar brillo/contraste
    # img = adjust_brightness_contrast(img)  

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

# def special_handling(line):
#     # Lógica para saltos de línea
def process_pdf(file):
    # Convertir PDF a imágenes
    pages = convert_from_path(file)
    texto = ''
    for page in pages:
        # Preprocesar imagen
        image = preprocess(page)  
        # Aplicar OCR
        text = pytesseract.image_to_string(image, lang='eng')
        texto += text
    
    # Procesar la cabecera
    # Procesar la cabecera
    cabecera = re.search(r"([^\n]+)\n\n([^\n]+)", texto)
    titulo = cabecera.group(1).strip()
    subtitulo = cabecera.group(2).strip()

    print("Título:", titulo)
    print("Subtítulo:", subtitulo)

    # Procesar la tabla
    tabla = re.search(r"Cantidad\s+Precio\s+Valor\n(.+?)\n\n", texto, re.DOTALL)
    descripcion = re.search(r"Productos\n\n(.+?)(?=\n\n[A-Z]+|$)", texto, re.DOTALL)
    tabla_texto = tabla.group(1)
    filas = re.findall(r"(.+?)\s+(\d+)\s+\$([\d\n]+)\s+\$(\d+)", tabla_texto,re.DOTALL)

    print("Tabla:")
    for fila in filas:
        producto = fila[0]
        cantidad = int(fila[1])
        precio_unitario = int("".join(fila[2].split("\n")).replace("§", ""))
        valor = int(fila[3])

        print("Producto:", producto.strip())
        print("Cantidad:", cantidad)
        print("Precio unitario:", precio_unitario)
        print("Valor:", valor)
        print()

    # Procesar el total
    total = re.search(r"Total:\s+\$(\d+)", texto)
    total_valor = int(total.group(1))

    print("Total:", total_valor)




    # Extracción de la información usando expresiones regulares
    # patron_productos = r"(.+?)\s+(\d+)\s+\$(\d+)\s+\$(\d+)"
    # productos = re.findall(patron_productos, newText)
    # print(productos)
    # patron_total = r"Total:\s+\$(\d+)"
    # total = re.search(patron_total, newText)

    # # Imprimir la información extraída
    
    # for producto in productos:
    #     nombre_producto, cantidad, precio_unitario, valor = producto
    #     print("Producto:", nombre_producto)
    #     print("Cantidad:", cantidad)
    #     print("Precio unitario:", precio_unitario)
    #     print("Valor:", valor)

process_pdf('test4.pdf')


