import subprocess
import sys
import os

# main.py — Ejercicio 2
#
# 1. Pide al usuario departamento y salario mínimo por teclado.
# 2. Lanza los tres procesos encadenados mediante pipes del SO:
#
#      proceso1 ──pipe──► proceso2 ──pipe──► proceso3
#
# Comunicación elegida: pipes de subprocess (stdout=PIPE, stdin=p.stdout)
# Es el equivalente Python a los PipedReader/PipedWriter de Java:
# conecta los stdout/stdin de los procesos directamente a nivel de SO,
# sin ficheros intermedios ni memoria compartida.
#
# Los tres procesos se lanzan antes de llamar a wait() para evitar
# deadlock: si proceso2 no está leyendo, proceso1 se bloquearía al
# intentar escribir en el pipe lleno.
#
# El Main espera a que los tres terminen (wait) antes de finalizar.


DIRECTORIO = os.path.dirname(os.path.abspath(__file__))
PYTHON     = sys.executable


def ruta(script: str) -> str:
    return os.path.join(DIRECTORIO, script)


def main() -> None:
    departamento   = input("Introduce el departamento: ").strip()
    salario_minimo = input("Introduce el salario mínimo: ").strip()

    # ── Cadena de pipes: P1 → P2 → P3 ───────────────────────────────────────

    # Proceso 1: lee salarios.txt, filtra por departamento → escribe en stdout
    p1 = subprocess.Popen(
        [PYTHON, ruta("proceso1.py"), departamento],
        stdout=subprocess.PIPE
    )

    # Proceso 2: lee de p1.stdout (pipe), filtra por salario → escribe en stdout
    # stdin=p1.stdout conecta directamente el pipe del SO entre p1 y p2
    p2 = subprocess.Popen(
        [PYTHON, ruta("proceso2.py"), salario_minimo],
        stdin=p1.stdout,
        stdout=subprocess.PIPE
    )

    # Una vez que p2 tiene el extremo de lectura del pipe de p1,
    # cerramos p1.stdout en el proceso padre para que p2 reciba EOF
    # cuando p1 termine (sin esto el pipe quedaría abierto en el padre)
    p1.stdout.close()

    # Proceso 3: lee de p2.stdout (pipe), escribe empleados.txt
    p3 = subprocess.Popen(
        [PYTHON, ruta("proceso3.py")],
        stdin=p2.stdout
    )

    # Mismo cierre del extremo del padre para el pipe p2→p3
    p2.stdout.close()

    # ── Esperar a que los tres procesos terminen ─────────────────────────────
    p1.wait()
    p2.wait()
    p3.wait()

    print("Proceso completado. Revisa ejercicio2/empleados.txt")


if __name__ == "__main__":
    main()
