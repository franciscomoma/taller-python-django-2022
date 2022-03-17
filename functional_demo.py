from scrapper import obtener_noticias

noticias, otra_cosa = obtener_noticias()

categorias = set(map(lambda noticia: noticia.get('categoria'), noticias))
