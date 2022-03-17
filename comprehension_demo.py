from scrapper import obtener_noticias

noticias, otra_cosa = obtener_noticias()

categorias = {noticia.get('categoria') for noticia in noticias}


def noticias_por_autor(autor):
    return [noticia.get('titulo') for noticia in noticias if noticia.get('autor') == autor]

autores_y_noticias = {noticia.get('autor'): noticias_por_autor(noticia.get('autor')) for noticia in noticias}

autores_y_noticias.get("Benzo")