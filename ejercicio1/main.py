import subprocess
import sys
import os

# main.py — Ejercicio 1
#
# Fase 1: lanza 31 subprocesos de proceso1.py en paralelo (uno por cada día
#         de diciembre) y espera a que todos terminen antes de continuar.
#         Se usa subprocess en lugar de multiprocessing porque el enunciado
#         pide procesos independientes, no hilos ni funciones del mismo proceso.
#
# Fase 2: lanza 31 subprocesos de proceso2.py y 31 de proceso3.py también
#         en paralelo. Todos leen ficheros distintos, por lo que no hay
#         conflicto de lectura. La escritura en maximas/minimas.txt se hace
#         en modo append con líneas cortas (atómico en POSIX).
#
# join() equivalente: Popen.wait() — bloquea hasta que el proceso termina.


MES   = 12
NDIAS = 31

DIRECTORIO = os.path.dirname(os.path.abspath(__file__))
PYTHON     = sys.executable  # usa el mismo intérprete que ejecuta este script


def ruta(script: str) -> str:
    return os.path.join(DIRECTORIO, script)


def main() -> None:

    # ── Fase 1: generar ficheros de temperaturas ─────────────────────────────
    procesos_fase1 = []
    for dia in range(1, NDIAS + 1):
        p = subprocess.Popen([PYTHON, ruta("proceso1.py"), str(dia), str(MES)])
        procesos_fase1.append(p)

    # Esperamos a que los 31 ficheros estén escritos antes de lanzar fase 2
    for p in procesos_fase1:
        p.wait()

    print("Fase 1 completada: 31 ficheros de temperaturas generados.")

    # ── Fase 2: calcular máximas y mínimas ───────────────────────────────────
    procesos_fase2 = []
    for dia in range(1, NDIAS + 1):
        nombre_fichero = f"{dia:02d}-{MES:02d}.txt"

        p2 = subprocess.Popen([PYTHON, ruta("proceso2.py"), nombre_fichero])
        p3 = subprocess.Popen([PYTHON, ruta("proceso3.py"), nombre_fichero])

        procesos_fase2.extend([p2, p3])

    for p in procesos_fase2:
        p.wait()

    print("Fase 2 completada: maximas.txt y minimas.txt generados.")


if __name__ == "__main__":
    main()
