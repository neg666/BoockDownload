import subprocess
import sys

def instalar_dependencias():
    print("Instalando dependencias necesarias...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', 'beautifulsoup4'])
    print("Dependencias instaladas correctamente.")

def importar_dependencias():
    global requests, BeautifulSoup, re, os
    import requests
    from bs4 import BeautifulSoup
    import re
    import os

def crear_carpeta(nombre):
    if not os.path.exists(nombre):
        os.makedirs(nombre)

def buscar_y_descargar_libros(palabras_clave, carpeta):
    url_base = 'https://www.google.com/search?q=filetype:pdf+'
    query = '+'.join(palabras_clave)
    urls = [f"{url_base}{query}&start={i*10}" for i in range(4)]  # Modificar el rango según la cantidad de resultados que desees buscar

    for d in urls:
        response = requests.get(d)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=re.compile('.*\.pdf'))
        for link in links:
            try:
                descargar = link.get('href').split('&sa=')[0].split('?q=')[1].split('.pdf')[0] + '.pdf'
                nombre = os.path.basename(descargar).replace('%25', '_')
                print('Se descargará: ' + nombre)
                response = requests.get(descargar, stream=True)
                ruta = os.path.join(carpeta, nombre)
                with open(ruta, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print('Libro: ' + nombre + ' [Descargado]')
            except Exception as e:
                print(f"Error al descargar {link.get('href')}: {e}")

def mostrar_menu():
    print("Bienvenido al descargador de libros PDF")
    palabras_clave = input("Ingrese las palabras clave para buscar libros (separadas por espacios): ").split()
    carpeta = 'libros_descargados'
    crear_carpeta(carpeta)
    buscar_y_descargar_libros(palabras_clave, carpeta)

if __name__ == "__main__":
    try:
        importar_dependencias()
    except ImportError:
        instalar_dependencias()
        importar_dependencias()
    mostrar_menu()
