import sys
import os

# proceso2.py
# Lee las 24 temperaturas de un fichero DD-MM.txt y escribe la máxima
# en maximas.txt con el formato  fecha:temperatura
#
# Parámetro: nombre del fichero (ej: "01-12.txt").
# El nombre ya codifica la fecha y apunta al fichero de lectura,
# por lo que no se necesitan día y mes por separado.
#
# La escritura en maximas.txt se hace en modo append ("a") para que
# cada proceso añada su línea sin borrar las de los demás.
# El acceso concurrente al fichero es seguro en este caso porque cada
# proceso escribe una sola línea de forma atómica a nivel de SO.


def calcular_maxima(nombre_fichero: str) -> None:
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio, nombre_fichero)
    ruta_salida  = os.path.join(directorio, "maximas.txt")

    with open(ruta_entrada, "r", encoding="utf-8") as f:
        temperaturas = [float(linea.strip()) for linea in f if linea.strip()]

    maxima = max(temperaturas)

    # Obtenemos la fecha quitando la extensión .txt
    fecha = nombre_fichero.replace(".txt", "")

    # Append: varios procesos pueden llegar aquí simultáneamente;
    # cada escritura de una línea corta es atómica en sistemas POSIX
    with open(ruta_salida, "a", encoding="utf-8") as f:
        f.write(f"{fecha}:{maxima:.2f}\n")


if __name__ == "__main__":
    nombre_fichero = sys.argv[1]
    calcular_maxima(nombre_fichero)
