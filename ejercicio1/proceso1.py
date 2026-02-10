import random
import sys
import os

# proceso1.py
# Genera 24 temperaturas aleatorias (0.00 - 20.00) para el día recibido
# y las escribe en un fichero con nombre DD-MM.txt.
#
# Parámetros: día y mes — únicos datos variables entre ejecuciones.
# El rango (0-20), la cantidad (24) y el mes son constantes del enunciado.


def generar_temperaturas(dia: int, mes: int) -> None:
    nombre_fichero = f"{dia:02d}-{mes:02d}.txt"
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_fichero)

    with open(ruta, "w", encoding="utf-8") as f:
        for _ in range(24):
            # Temperatura con dos decimales entre 0.00 y 20.00
            temperatura = round(random.uniform(0, 20), 2)
            f.write(f"{temperatura:.2f}\n")


if __name__ == "__main__":
    # Recibe día y mes como argumentos de línea de comandos
    # cuando el Main lo lanza como subproceso
    dia = int(sys.argv[1])
    mes = int(sys.argv[2])
    generar_temperaturas(dia, mes)
