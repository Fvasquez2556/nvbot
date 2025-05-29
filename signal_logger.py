import csv
from datetime import datetime

def registrar_senal_csv(
    symbol,
    precio_actual,
    precio_entrada,
    rango_subida_estimado,
    lapso_estimado,
    rebotes_previos,
    variaciones_previas,
    drawdown,
    rsi,
    ema8,
    ema21,
    volumen,
    resultado_real="",
    archivo="signals_log.csv"
):
    try:
        with open(archivo, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                symbol,
                precio_actual,
                precio_entrada,
                rango_subida_estimado,
                lapso_estimado,
                rebotes_previos,
                variaciones_previas,
                drawdown,
                rsi,
                ema8,
                ema21,
                volumen,
                resultado_real
            ])
    except Exception as e:
        print(f"[Logger error] No se pudo registrar señal para {symbol}: {e}")
