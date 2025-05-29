
import ccxt
import time
from datetime import datetime
from tabulate import tabulate
from rebote_detector import (
    calcular_promedios_vh,
    detectar_rebotes,
    evaluar_probabilidad,
    sugerir_entrada
)
from signal_logger import registrar_senal_csv

exchange = ccxt.binance({ "enableRateLimit": True })

def filtrar_pares_usdt_activos(exchange):
    mercados = exchange.load_markets()
    pares = []
    for symbol, info in mercados.items():
        if symbol.endswith("/USDT") and info.get("active") and info.get("spot"):
            pares.append(symbol)
    return pares

def analizar_rebotes_experimental():
    pares_usdt = filtrar_pares_usdt_activos(exchange)
    resultados = []

    for symbol in pares_usdt:
        try:
            rebotes = detectar_rebotes(exchange, symbol)
            for rebote in rebotes:
                if rebote["variacion"] < 3.5:
                    continue

                probabilidad = evaluar_probabilidad(rebote)
                if probabilidad < 0.75:
                    continue

                entrada = sugerir_entrada(exchange, symbol)
                if not entrada:
                    continue

                ohlcv = exchange.fetch_ohlcv(symbol, timeframe="5m", limit=288)
                precios = [candle[4] for candle in ohlcv]
                maximos = [candle[2] for candle in ohlcv]
                minimos = [candle[3] for candle in ohlcv]
                volumenes = [candle[5] for candle in ohlcv]

                promedio_24h = round(sum(precios) / len(precios), 4)
                precio_actual = precios[-1]
                rebotes_5 = sum(1 for high, low in zip(maximos, minimos) if (high - low) / low >= 0.05)
                variaciones_previas = [round((high - low) / low * 100, 2) for high, low in zip(maximos, minimos)]
                drawdown = round((entrada["entrada_recomendada"] - min(minimos[-3:])) / entrada["entrada_recomendada"], 4)
                rsi = 50  # Simulado
                ema8 = sum(precios[-8:]) / 8
                ema21 = sum(precios[-21:]) / 21
                volumen = sum(volumenes[-12:]) / 12

                confianza = "ALTA" if probabilidad >= 0.85 else "MODERADA"

                # Mostrar salida para el usuario (consola)
                hora_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                resultados.append([
                    hora_local,
                    symbol,
                    promedio_24h,
                    round(precio_actual, 4),
                    rebotes_5,
                    f"{rebote['variacion']}%",
                    f"{rebote['lapso'] * int(rebote['intervalo'].replace('m', ''))} min",
                    entrada["entrada_recomendada"]
                ])

                # Guardar en CSV completo
                registrar_senal_csv(
                    symbol,
                    precio_actual,
                    entrada["entrada_recomendada"],
                    rebote["variacion"],
                    rebote["lapso"] * int(rebote["intervalo"].replace("m", "")),
                    rebotes_5,
                    variaciones_previas,
                    drawdown,
                    round(rsi, 2),
                    round(ema8, 6),
                    round(ema21, 6),
                    round(volumen, 2),
                    resultado_real=""
                )

        except Exception as e:
            print(f"[Error] {symbol}: {e}")

    if resultados:
        headers = [
            "Hora", "Par", "Prom. 24h", "Actual",
            "# Rebotes ≥5%", "Rebote", "En", "Entrada Recomendada"
        ]
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
    else:
        print("⚠️ No se encontraron señales en modo experimental.")

if __name__ == "__main__":
    while True:
        print("🔄 MODO EXPERIMENTAL COMPLETO: analizando señales...\n")
        analizar_rebotes_experimental()

