import sys
import os

# proceso3.py
# Lee las 24 temperaturas de un fichero DD-MM.txt y escribe la mínima
# en minimas.txt con el formato  fecha:temperatura
#
# Parámetro: nombre del fichero. Mismo criterio que proceso2:
# el nombre lo identifica todo y no se necesitan parámetros extra.
#
# Misma estrategia de append que proceso2 para minimas.txt.


def calcular_minima(nombre_fichero: str) -> None:
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio, nombre_fichero)
    ruta_salida  = os.path.join(directorio, "minimas.txt")

    with open(ruta_entrada, "r", encoding="utf-8") as f:
        temperaturas = [float(linea.strip()) for linea in f if linea.strip()]

    minima = min(temperaturas)

    fecha = nombre_fichero.replace(".txt", "")

    with open(ruta_salida, "a", encoding="utf-8") as f:
        f.write(f"{fecha}:{minima:.2f}\n")


if __name__ == "__main__":
    nombre_fichero = sys.argv[1]
    calcular_minima(nombre_fichero)
