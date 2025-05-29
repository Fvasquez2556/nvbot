
import csv
from datetime import datetime

def registrar_senal_csv(symbol, precio_actual, entrada_recomendada, variacion, lapso, probabilidad, archivo="signals_log.csv"):
    try:
        with open(archivo, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.utcnow().isoformat(),
                symbol,
                precio_actual,
                entrada_recomendada,
                f"{variacion}%",
                f"{lapso} min",
                f"{round(probabilidad * 100, 2)}%"
            ])
    except Exception as e:
        print(f"[Logger error] No se pudo registrar señal para {symbol}: {e}")
