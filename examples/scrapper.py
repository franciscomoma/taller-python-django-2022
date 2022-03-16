from functools import reduce
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


URL = "https://www.elotrolado.net"

def convertir_noticia(noticia):
    """
    Convierte una noticia de portada de ElOtroLado.net de HTML a diccionario
    """

    # Determina si el artículo está oculto (tiene asignada alguna clase hidden_*)
    oculto = [clase for clase in noticia.attrs["class"] if clase.startswith("hidden")]
    if oculto:
        # Si está oculto, no se devuelve
        return None

    # Si no está oculto, se obtiene la meta información de la noticia
    meta = noticia.find("a", {"class": "meta"}) 
 
    # Devuelve la noticia convertida a diccionario
    return {
        "fecha_publicacion": datetime.strptime(meta.time.attrs["datetime"], "%Y-%m-%dT%H:%M:%S+00:00"),
        "enlace": f"{URL}{meta.attrs['href']}",
        "autor": noticia.find("div", {"class": "author"}).span.text,
        "categoria": noticia.find("a", {"class": "newcat"}).text,
        "titulo": noticia.find("h2").a.attrs["title"],
        "resumen": noticia.find("div", {"class": "body"}).text
    }

def obtener_noticias(pagina_inicial=1, ultima_pagina=None, fecha_desde=None, fecha_hasta=None):
    """
    Obitene una lista de noticias de ElOtroLado.net.
    - pagina_inicial (int): La primera página que se solicitará al servidor
    - ultima_pagina (int): La última página que se solicitará al servidor
    - fecha_desde (datetime): Incluye las noticias desde la fecha dada
    - fecha_hasta (datetime): Incluye las noticias hasta la fecha dada
    """
    noticias_convertidas = []  # La lista donde se añadirán las noticias convertidas

    if not ultima_pagina:
        ultima_pagina = pagina_inicial  # Cuando no se indica la última página, solo se pedirá la página inicial

    if ultima_pagina < pagina_inicial:
        # Cuando la página inicial sea mayor que la última página, se lanza una Excepción
        raise AttributeError("La página inicial no puede ser mayor que la última página")

    fecha_alcanzada = False  # Necesario para no hacer peticiones innecesarias al servidor
    peticiones_hechas = 0  # Un contador de peticiones hechas
    pagina_actual = pagina_inicial  # El número de página actual

    while pagina_actual <= ultima_pagina and not fecha_alcanzada:
        respuesta = requests.get(f"{URL}/?page={pagina_actual}")

        soup = BeautifulSoup(respuesta.text, "html.parser")
        noticias = soup.find_all("div", {"class": "new"})  # Obtiene todas las noticias
        
        for noticia in noticias:
            if noticia_convertida:=convertir_noticia(noticia):  # Asociación de variable dentro del if con operador morsa
                if fecha_desde and noticia_convertida["fecha_publicacion"] < fecha_desde:
                    """
                        Si se indica la fecha desde la que se quieren noticias,
                        no es necesario continuar haciendo peticiones
                    """
                    fecha_alcanzada = True
                    continue

                if fecha_hasta and noticia_convertida["fecha_publicacion"] > fecha_hasta:
                    continue

                noticias_convertidas.append(noticia_convertida)

        peticiones_hechas += 1
        pagina_actual += 1

    return sorted(noticias_convertidas, key=lambda x: x["fecha_publicacion"], reverse=True), peticiones_hechas

if __name__ == '__main__':
    fecha_desde = (datetime.now() - timedelta(days=6))
    fecha_hasta = datetime.now()
    noticias, peticiones_hechas = obtener_noticias(ultima_pagina=10, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta) 

    for noticia in noticias:
        print(f"{noticia['fecha_publicacion']} - {noticia['titulo']} - {noticia['categoria']}")

    print(f"Peticiones hechas: {peticiones_hechas}\nNúmero de noticias: {len(noticias)}")


    def reduce_categorias(x, y):
        resultado = x

        if isinstance(x, tuple):
            # La primera iteracion, x es una tupla
            categoria, noticia = x
            resultado = {categoria: noticia}

        categoria, noticia = y
        resultado[categoria] = [*noticia, *resultado.get(categoria, [])]  # Combina las listas de noticias
    
        return resultado

    resultado = reduce(lambda x, y: {**{x[0]: x[1]}, **{y[0]: y[1] if x[0] != y[0] else [*x[1], *y[1]]}} if isinstance(x, tuple) else {**x, **{y[0]: [*x.get(y[0], []),*y[1]]}}, map(lambda x: (x["categoria"], [x]), noticias))
    #resultado = reduce(reduce_categorias, map(lambda x: (x["categoria"], [x["titulo"]]), noticias))

    logging.info(resultado)
