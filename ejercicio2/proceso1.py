import sys
import os

# proceso1.py — Ejercicio 2
#
# Lee salarios.txt y envía a stdout las líneas cuyo departamento coincida
# con el recibido por argumento, SIN el campo departamento.
#
# Parámetro: departamento — único dato variable para filtrar.
# No recibe ruta del fichero porque es fija (salarios.txt en la misma carpeta).
#
# Formato del fichero:  Nombre;Apellido;Salario;Departamento
# Lo que escribe en stdout: Nombre;Apellido;Salario
#
# La comunicación se hace a través de stdout/stdin (pipe del SO),
# que es el mecanismo más natural entre procesos en Python/Unix.
# El Main conecta stdout de P1 con stdin de P2 mediante subprocess.PIPE.


def main() -> None:
    departamento = sys.argv[1]

    directorio   = os.path.dirname(os.path.abspath(__file__))
    ruta_fichero = os.path.join(directorio, "salarios.txt")

    with open(ruta_fichero, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            # Formato: Nombre;Apellido;Salario;Departamento
            partes = linea.split(";")
            if len(partes) < 4:
                continue

            dept = partes[3].strip()

            if dept.lower() == departamento.lower():
                # Enviamos Nombre;Apellido;Salario (sin departamento)
                print(f"{partes[0]};{partes[1]};{partes[2].strip()}")


if __name__ == "__main__":
    main()
