import sys

# proceso2.py — Ejercicio 2
#
# Lee de stdin (pipe que viene de proceso1) y reenvía a stdout
# solo las líneas cuyo salario sea >= salario_minimo.
#
# Parámetro: salario_minimo — único dato variable para filtrar.
# No necesita departamento ni ruta: proceso1 ya filtró y eliminó esos datos.
#
# Formato recibido por stdin:  Nombre;Apellido;Salario
# Formato enviado a stdout:    Nombre;Apellido;Salario  (sin modificar)
#
# Lee de sys.stdin que el Main habrá conectado al stdout de proceso1.


def main() -> None:
    salario_minimo = float(sys.argv[1])

    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue

        # Salario en el índice 2: Nombre;Apellido;Salario
        partes = linea.split(";")
        if len(partes) < 3:
            continue

        salario = float(partes[2].strip())

        # Solo pasan las líneas que superan o igualan el umbral mínimo
        if salario >= salario_minimo:
            print(linea)  # se reenvía tal cual a stdout


if __name__ == "__main__":
    main()
