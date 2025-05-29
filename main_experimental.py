
import ccxt
import time
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

                promedios = calcular_promedios_vh(exchange, symbol, intervals=["1d"])
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe="5m", limit=288)
                precios = [candle[4] for candle in ohlcv]
                maximos = [candle[2] for candle in ohlcv]
                minimos = [candle[3] for candle in ohlcv]
                promedio_24h = round(sum(precios) / len(precios), 4)
                precio_actual = precios[-1]

                rebotes_5 = sum(1 for high, low in zip(maximos, minimos)
                                if (high - low) / low >= 0.05)

                drawdown = (entrada["entrada_recomendada"] - min(minimos[-3:])) / entrada["entrada_recomendada"]
                if drawdown > 0.05:
                    continue

                confianza = "ALTA" if probabilidad >= 0.85 else "MODERADA"

                resultados.append([
                    symbol,
                    promedio_24h,
                    round(precio_actual, 4),
                    f"{rebotes_5} velas ≥5%",
                    f"{rebote['variacion']}%",
                    f"{rebote['lapso'] * int(rebote['intervalo'].replace('m', ''))} min",
                    entrada["entrada_recomendada"],
                    confianza
                ])

                registrar_senal_csv(
                    symbol,
                    precio_actual,
                    entrada["entrada_recomendada"],
                    rebote["variacion"],
                    rebote["lapso"] * int(rebote["intervalo"].replace("m", "")),
                    probabilidad
                )
        except Exception as e:
            print(f"[Error] {symbol}: {e}")

    if resultados:
        headers = [
            "Par", "Prom. 24h", "Actual",
            "# Rebotes ≥5%", "Rebote", "En", "Entrada", "Confianza"
        ]
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
    else:
        print("⚠️ No se encontraron señales en modo experimental.")

if __name__ == "__main__":
    while True:
        print("🔄 MODO EXPERIMENTAL: analizando señales con condiciones flexibles...\n")
        analizar_rebotes_experimental()
