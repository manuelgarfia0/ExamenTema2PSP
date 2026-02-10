import sys
import os

# proceso3.py — Ejercicio 2
#
# Lee de stdin (pipe que viene de proceso2) y escribe en empleados.txt
# con el formato del enunciado: Apellido Nombre, Salario
#
# No recibe parámetros: la ruta de salida es fija ("empleados.txt")
# y todos los filtros ya los han aplicado los procesos anteriores.
#
# Formato recibido por stdin: Nombre;Apellido;Salario
# Formato escrito en fichero: Apellido Nombre, Salario
# (se invierte el orden de nombre y apellido según el enunciado)


def main() -> None:
    directorio  = os.path.dirname(os.path.abspath(__file__))
    ruta_salida = os.path.join(directorio, "empleados.txt")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        for linea in sys.stdin:
            linea = linea.strip()
            if not linea:
                continue

            # Formato recibido: Nombre;Apellido;Salario
            partes = linea.split(";")
            if len(partes) < 3:
                continue

            nombre   = partes[0].strip()
            apellido = partes[1].strip()
            salario  = float(partes[2].strip())

            # Formato de salida: Apellido Nombre, Salario
            f.write(f"{apellido} {nombre}, {salario:.2f}\n")

    print("proceso3: empleados.txt generado correctamente.")


if __name__ == "__main__":
    main()
