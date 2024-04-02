from PIL import Image, ImageEnhance, ImageFilter

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
