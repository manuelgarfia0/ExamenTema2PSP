import subprocess
import sys
import os

# =============================================================================
# EJERCICIO 2 — Filtro de Salarios
# Comunicación entre procesos mediante pipes del SO (stdout/stdin),
# equivalente a los PipedReader/PipedWriter de Java.
# Cadena: proceso1 ──pipe──► proceso2 ──pipe──► proceso3
# =============================================================================

SCRIPT = os.path.abspath(__file__)
PYTHON = sys.executable


# -----------------------------------------------------------------------------
# PROCESO 1
# Lee salarios.txt y escribe en stdout las líneas del departamento recibido,
# sin el campo departamento.
# Parámetro: departamento — único dato variable para filtrar.
# Formato fichero:  Nombre;Apellido;Salario;Departamento
# Formato stdout:   Nombre;Apellido;Salario
# -----------------------------------------------------------------------------
def proceso1(departamento: str) -> None:
    directorio   = os.path.dirname(SCRIPT)
    ruta_fichero = os.path.join(directorio, "salarios.txt")

    with open(ruta_fichero, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(";")
            if len(partes) < 4:
                continue

            if partes[3].strip().lower() == departamento.lower():
                print(f"{partes[0]};{partes[1]};{partes[2].strip()}")


# -----------------------------------------------------------------------------
# PROCESO 2
# Lee de stdin (pipe de proceso1) y reenvía a stdout las líneas cuyo
# salario sea >= salario_minimo, sin modificarlas.
# Parámetro: salario_minimo — único dato variable para filtrar.
# Formato recibido/enviado: Nombre;Apellido;Salario
# -----------------------------------------------------------------------------
def proceso2(salario_minimo: float) -> None:
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue

        partes = linea.split(";")
        if len(partes) < 3:
            continue

        if float(partes[2].strip()) >= salario_minimo:
            print(linea)


# -----------------------------------------------------------------------------
# PROCESO 3
# Lee de stdin (pipe de proceso2) y escribe empleados.txt.
# Sin parámetros: la ruta de salida es fija y los filtros ya están aplicados.
# Formato recibido: Nombre;Apellido;Salario
# Formato escrito:  Apellido Nombre, Salario
# -----------------------------------------------------------------------------
def proceso3() -> None:
    directorio  = os.path.dirname(SCRIPT)
    ruta_salida = os.path.join(directorio, "empleados.txt")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        for linea in sys.stdin:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(";")
            if len(partes) < 3:
                continue

            nombre   = partes[0].strip()
            apellido = partes[1].strip()
            salario  = float(partes[2].strip())

            f.write(f"{apellido} {nombre}, {salario:.2f}\n")


# -----------------------------------------------------------------------------
# MAIN
# Pide departamento y salario mínimo por teclado.
# Lanza los tres procesos encadenados con pipes y espera a que terminen.
# Se lanzan los tres ANTES de wait() para evitar deadlock: si proceso2
# no está leyendo, proceso1 se bloquearía al llenar el pipe.
# Se cierra p1.stdout y p2.stdout en el padre para que cada proceso
# reciba EOF cuando el anterior termine.
# -----------------------------------------------------------------------------
def main() -> None:
    departamento   = input("Introduce el departamento: ").strip()
    salario_minimo = input("Introduce el salario mínimo: ").strip()

    p1 = subprocess.Popen(
        [PYTHON, SCRIPT, "proceso1", departamento],
        stdout=subprocess.PIPE
    )

    p2 = subprocess.Popen(
        [PYTHON, SCRIPT, "proceso2", salario_minimo],
        stdin=p1.stdout,
        stdout=subprocess.PIPE
    )
    p1.stdout.close()

    p3 = subprocess.Popen(
        [PYTHON, SCRIPT, "proceso3"],
        stdin=p2.stdout
    )
    p2.stdout.close()

    p1.wait()
    p2.wait()
    p3.wait()

    print("Proceso completado. Revisa empleados.txt")


# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA
# Sin argumentos → actúa como main.
# Con argumento "procesoN" → ejecuta ese proceso con los parámetros siguientes.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == "proceso1":
        proceso1(sys.argv[2])
    elif sys.argv[1] == "proceso2":
        proceso2(float(sys.argv[2]))
    elif sys.argv[1] == "proceso3":
        proceso3()
