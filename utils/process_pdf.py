import pytesseract
from pdf2image import convert_from_path
import cv2

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
    descripcion_regex = r"Productos\n(?P<descripcion>.*?)Total:.*?Precio\nunitario\s+\$(?P<precio_unitario>\d+).*?Valor\s+\$(?P<valor_total>\d+)"
    match = re.search(descripcion_regex, texto_normalizado, re.DOTALL)

    if match:
        # Eliminamos espacios adicionales y unimos la descripción en una sola línea
        descripcion = " ".join(match.group("descripcion").splitlines()).strip()
        precio_unitario = match.group("precio_unitario").strip()
        valor_total = match.group("valor_total").strip()
        print(f"Descripción: {descripcion}, Precio Unitario: ${precio_unitario}, Valor Total: ${valor_total}")
    else:
        print("No se encontraron coincidencias con el patrón regex.")
