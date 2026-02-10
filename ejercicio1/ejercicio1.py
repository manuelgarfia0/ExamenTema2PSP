import random
import subprocess
import sys
import os

# =============================================================================
# EJERCICIO 1 — Temperaturas de Diciembre
# =============================================================================

MES    = 12
NDIAS  = 31
SCRIPT = os.path.abspath(__file__)
PYTHON = sys.executable


# -----------------------------------------------------------------------------
# PROCESO 1
# Genera 24 temperaturas aleatorias (0.00–20.00) para el día recibido
# y las escribe en DD-MM.txt.
# Parámetros: día y mes — únicos datos variables entre ejecuciones.
# -----------------------------------------------------------------------------
def proceso1(dia: int, mes: int) -> None:
    directorio     = os.path.dirname(SCRIPT)
    nombre_fichero = f"{dia:02d}-{mes:02d}.txt"
    ruta           = os.path.join(directorio, nombre_fichero)

    with open(ruta, "w", encoding="utf-8") as f:
        for _ in range(24):
            temperatura = round(random.uniform(0, 20), 2)
            f.write(f"{temperatura:.2f}\n")


# -----------------------------------------------------------------------------
# PROCESO 2
# Lee las temperaturas de DD-MM.txt y añade la máxima a maximas.txt.
# Parámetro: nombre del fichero — ya identifica el día y apunta a la lectura.
# Append atómico en POSIX: seguro con múltiples procesos simultáneos.
# -----------------------------------------------------------------------------
def proceso2(nombre_fichero: str) -> None:
    directorio   = os.path.dirname(SCRIPT)
    ruta_entrada = os.path.join(directorio, nombre_fichero)
    ruta_salida  = os.path.join(directorio, "maximas.txt")

    with open(ruta_entrada, "r", encoding="utf-8") as f:
        temperaturas = [float(l.strip()) for l in f if l.strip()]

    fecha = nombre_fichero.replace(".txt", "")

    with open(ruta_salida, "a", encoding="utf-8") as f:
        f.write(f"{fecha}:{max(temperaturas):.2f}\n")


# -----------------------------------------------------------------------------
# PROCESO 3
# Lee las temperaturas de DD-MM.txt y añade la mínima a minimas.txt.
# Mismo criterio de parámetros y escritura que proceso2.
# -----------------------------------------------------------------------------
def proceso3(nombre_fichero: str) -> None:
    directorio   = os.path.dirname(SCRIPT)
    ruta_entrada = os.path.join(directorio, nombre_fichero)
    ruta_salida  = os.path.join(directorio, "minimas.txt")

    with open(ruta_entrada, "r", encoding="utf-8") as f:
        temperaturas = [float(l.strip()) for l in f if l.strip()]

    fecha = nombre_fichero.replace(".txt", "")

    with open(ruta_salida, "a", encoding="utf-8") as f:
        f.write(f"{fecha}:{min(temperaturas):.2f}\n")


# -----------------------------------------------------------------------------
# MAIN
# Fase 1: 31 subprocesos de proceso1 en paralelo. Se espera a que todos
#         terminen (wait) antes de la fase 2: P2 y P3 necesitan los ficheros.
# Fase 2: 31 subprocesos de proceso2 y 31 de proceso3 en paralelo.
# Cada subproceso relanza este mismo fichero con el nombre del proceso
# como primer argumento, evitando ficheros separados.
# -----------------------------------------------------------------------------
def main() -> None:

    # ── Fase 1: generar ficheros de temperaturas ──────────────────────────────
    procesos_fase1 = []
    for dia in range(1, NDIAS + 1):
        p = subprocess.Popen([PYTHON, SCRIPT, "proceso1", str(dia), str(MES)])
        procesos_fase1.append(p)

    for p in procesos_fase1:
        p.wait()

    print("Fase 1 completada: 31 ficheros de temperaturas generados.")

    # ── Fase 2: calcular máximas y mínimas ────────────────────────────────────
    procesos_fase2 = []
    for dia in range(1, NDIAS + 1):
        nombre_fichero = f"{dia:02d}-{MES:02d}.txt"
        p2 = subprocess.Popen([PYTHON, SCRIPT, "proceso2", nombre_fichero])
        p3 = subprocess.Popen([PYTHON, SCRIPT, "proceso3", nombre_fichero])
        procesos_fase2.extend([p2, p3])

    for p in procesos_fase2:
        p.wait()

    print("Fase 2 completada: maximas.txt y minimas.txt generados.")


# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA
# Sin argumentos → actúa como main.
# Con argumento "procesoN" → ejecuta ese proceso con los parámetros siguientes.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == "proceso1":
        proceso1(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == "proceso2":
        proceso2(sys.argv[2])
    elif sys.argv[1] == "proceso3":
        proceso3(sys.argv[2])
