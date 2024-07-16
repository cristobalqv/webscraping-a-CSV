import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def formatear_precio(precio):
    return precio.replace('$', '').replace('.', '')

def eliminar_palabra(lista):
    nueva_lista = []
    for elemento in lista:
        nuevo_string = re.sub(r'[^\d]', '', elemento)
        nueva_lista.append(nuevo_string.strip())
    return nueva_lista

def exportar_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("data.csv", index=False)

def webscraping():
    diccionario = {'nombre': [],
                'precio': []}

    for i in range(1,4):
        url_base = f'https://www.drogueriascafam.com.co/69-ofertas-destacadas-del-mes?page={i}'

        r = requests.get(url_base)
        soup = BeautifulSoup(r.content, 'html.parser')

        # url contiene diferentes paginas. Queremos iterar en todas ellas, por lo que necesito encontrar un patron para poder iterarlas.
        # este patron se encuentra en las etiquetas 'li', que están dentro de una etiqueta 'ul' con clase 'page-list flex-container'
        ul = soup.find("ul", {"class": "page-list flex-container"}).find_all("li")

        all_products = soup.find_all('article')
        for product in all_products:
            nombre = product.find('div', {'class': 'thumbnail-container relative'}).find('div', {'class': 'product-desc-wrap'}).find('div', {'class': 'product-description relative clearfix'}).find('div', {'class': 'name-product-list'}).find('h3').text.strip()
            precio = formatear_precio(product.find('div', {'class': 'thumbnail-container relative'}).find('div', {'class': 'product-price-and-shipping'}).find('span', {'class': 'price'}).text)
            diccionario['nombre'].append(nombre)
            diccionario['precio'].append(precio)    
        
    nuevo_precio = eliminar_palabra(diccionario['precio'])
    diccionario['precio'] = nuevo_precio
    return diccionario


if __name__ == "__main__":
    data = webscraping()
    exportar_csv(data)



