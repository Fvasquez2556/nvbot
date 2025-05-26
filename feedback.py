import csv
import os

def cargar_signales_pendientes(path="data/signals.csv"):
    señales = []
    with open(path, mode="r", newline="") as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            if "resultado" not in fila or fila["resultado"] == "":
                señales.append(fila)
    return señales

def guardar_resultados(path, señales, originales):
    fieldnames = list(originales[0].keys())
    if "resultado" not in fieldnames:
        fieldnames.append("resultado")

    with open(path, mode="w", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=fieldnames)
        writer.writeheader()
        for fila in originales:
            writer.writerow(fila)

def main():
    archivo = "data/signals.csv"
    if not os.path.exists(archivo):
        print("⚠️ No se encontró el archivo 'signals.csv'. Ejecuta primero el bot.")
        return

    # Cargar todas las filas
    with open(archivo, mode="r", newline="") as archivo_lectura:
        reader = csv.DictReader(archivo_lectura)
        originales = list(reader)

    pendientes = [fila for fila in originales if "resultado" not in fila or fila["resultado"] == ""]

    if not pendientes:
        print("✅ No hay señales pendientes de evaluación.")
        return

    print(f"🔍 {len(pendientes)} señales pendientes para evaluar:\n")

    for fila in pendientes:
        print(f"[{fila['timestamp']}] {fila['par']} | {fila['tendencia']} | RSI={fila['RSI']} | Prob: {fila['probabilidad']}% | Subida: {fila['rango_subida']}%")

        while True:
            r = input("¿La señal fue acertada? [s]í / [n]o / [x] ignorar: ").strip().lower()
            if r in ["s", "n", "x"]:
                break
            print("❌ Entrada no válida. Intenta de nuevo.")

        for f in originales:
            if f["timestamp"] == fila["timestamp"] and f["par"] == fila["par"]:
                if r == "s":
                    f["resultado"] = "1"
                elif r == "n":
                    f["resultado"] = "0"
                elif r == "x":
                    f["resultado"] = ""

    guardar_resultados("data/signals.csv", pendientes, originales)
    print("\n✅ Feedback guardado con éxito.")

if __name__ == "__main__":
    main()
