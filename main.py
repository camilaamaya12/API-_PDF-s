import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time
from datetime import date
import os
from io import BytesIO

def slugify(url):
    """Extrae el slug de una URL y lo convierte en un nombre de archivo válido."""
    slug = re.sub(r'^https?://', '', url)  # Elimina el prefijo http:// o https://
    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', slug)  # Reemplaza caracteres no válidos por _
    return slug

# Función para crear una carpeta si no existe
def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Función para capturar y guardar las imágenes de las páginas web
def capture_and_save_screenshots(urls, resolutions, capture_folder):
    # Ruta del ChromeDriver
    chromedriver_path = 'chromedriver-win64\chromedriver.exe'  # Actualiza esta ruta a donde está tu ChromeDriver

    # Configurar opciones de Chrome para el modo headless y el tamaño de la ventana
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--hide-scrollbars")
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Ruta de Chrome

    # Crear servicio de ChromeDriver
    service = Service(executable_path=chromedriver_path)

    # Inicializar el navegador
    driver = webdriver.Chrome(service=service, options=options)

    # Lista para almacenar las rutas de las imágenes capturadas
    screenshot_paths = []

    for url in urls:
        for resolution in resolutions:
            width, height = resolution
            driver.set_window_size(width, height)
            driver.get(url)
            # Incrementar el tiempo de espera para asegurarse de que todo el contenido y los scripts se carguen
            time.sleep(10)

            # Hacer scroll hasta el final de la página
            scroll_pause_time = 3
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Hacer scroll hacia abajo
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Esperar a que la página cargue
                time.sleep(scroll_pause_time)

                # Calcular la nueva altura de la página y comparar con la última altura
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Tomar una captura de pantalla completa de la página
            total_height = driver.execute_script("return document.body.scrollHeight")
            total_width = driver.execute_script("return document.body.scrollWidth")

            driver.set_window_size(total_width, total_height)
            time.sleep(5)  # Esperar a que el tamaño de la ventana se ajuste

            screenshot = driver.get_screenshot_as_png()
            screenshot_image = Image.open(BytesIO(screenshot))

            # Manipular la URL y la fecha para dar nombre a la imagen
            x = url.split("/")
            x2 = x[-1]
            
            today = date.today().isoformat()
            screenshot_path = os.path.join(capture_folder, f'{x2}-{today}-{width}x{height}.pdf')

            # Guardar la imagen
            screenshot_image.save(screenshot_path)
            screenshot_paths.append(screenshot_path)

    driver.quit()

    return screenshot_paths

# Lista de URLs a capturar
urls = [

"https://youtube.com",








]


   
    
   


# Resoluciones para las capturas de pantalla [(ancho, alto)]
resolutions = [(1920, 1080)]

# Carpeta para almacenar las capturas
capture_folder = 'captures'
create_folder_if_not_exists(capture_folder)

# Capturar y guardar las imágenes
screenshot_paths = capture_and_save_screenshots(urls, resolutions, capture_folder)
print("Capturas guardadas en la carpeta 'captures':")
for path in screenshot_paths:
    print(path)
