
import ccxt
import time
from tabulate import tabulate
from rebote_detector import (
    calcular_promedios_vh,
    detectar_rebotes,
    evaluar_probabilidad,
    sugerir_entrada
)

# Inicializar exchange
exchange = ccxt.binance({ "enableRateLimit": True })

def filtrar_pares_usdt_activos(exchange):
    mercados = exchange.load_markets()
    pares = []
    for symbol, info in mercados.items():
        if symbol.endswith("/USDT") and info.get("active") and info.get("spot"):
            pares.append(symbol)
    return pares

def analizar_rebotes_y_mostrar():
    pares_usdt = filtrar_pares_usdt_activos(exchange)
    resultados = []

    for symbol in pares_usdt:
        try:
            rebotes = detectar_rebotes(exchange, symbol)
            for rebote in rebotes:
                probabilidad = evaluar_probabilidad(rebote)
                if probabilidad < 0.85:
                    continue

                entrada = sugerir_entrada(exchange, symbol)
                promedios = calcular_promedios_vh(exchange, symbol, intervals=["1d"])
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe="5m", limit=288)
                precios = [candle[4] for candle in ohlcv]
                maximos = [candle[2] for candle in ohlcv]
                minimos = [candle[3] for candle in ohlcv]
                promedio_24h = round(sum(precios) / len(precios), 4)
                precio_actual = precios[-1]

                # Calcular cuántas veces hubo una subida >=5% en una vela
                rebotes_5 = sum(1 for high, low in zip(maximos, minimos)
                                if (high - low) / low >= 0.05)

                # Verificar drawdown antes de subida (simplificado)
                drawdown = (entrada["entrada_recomendada"] - minimos[-1]) / entrada["entrada_recomendada"]
                if drawdown > 0.02:
                    continue  # se descarta si la caída antes de subir es >2%

                resultados.append([
                    symbol,
                    promedio_24h,
                    round(precio_actual, 4),
                    f"{rebotes_5} velas ≥5%",
                    f"{rebote['variacion']}%",
                    f"{rebote['lapso'] * int(rebote['intervalo'].replace('m', ''))} min",
                    entrada["entrada_recomendada"]
                ])
        except Exception as e:
            print(f"[Error] {symbol}: {e}")

    # Mostrar tabla
    if resultados:
        headers = [
            "Par", "Precio Prom. 24h", "Precio Actual",
            "# Rebotes ≥5%", "Rebote Actual", "En", "Entrada Recomendada"
        ]
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
    else:
        print("⚠️ No se encontraron señales con probabilidad ≥ 85% y drawdown ≤ 2%.")

if __name__ == "__main__":
    while True:
        print("🔄 Analizando pares USDT activos en Binance...\n")
        analizar_rebotes_y_mostrar()
        print("⏳ Esperando 60 segundos antes del siguiente ciclo...\n")
        time.sleep(60)
# This code is a complete script that integrates the rebote detection functionality with Binance's API.
# It fetches active USDT pairs, detects rebounds, evaluates probabilities, suggests entry points,