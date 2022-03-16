import os
import re
import tracemalloc


if __name__ == "__main__":

    tracemalloc.start()

    def iter_quijote():
        letra_regex = re.compile("[a-záéíóúüñçA-ZÁÉÍÓÚÜÑÇ]")

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "quijote.txt"), "r", encoding="utf8") as f:

            palabra = ""
            while True:
                letra = f.read(1)

                if not letra:
                    break
                elif letra_regex.match(letra):
                    palabra += letra
                elif palabra:
                    yield palabra
                    palabra = ""

    palabras = iter_quijote()

    for palabra in palabras:
        print(palabra)

    current, peak = tracemalloc.get_traced_memory()
    print(f"La memoria usada actualmente es {current / 10**6}MB; El pico fué de {peak / 10**6}MB")
    tracemalloc.stop()
