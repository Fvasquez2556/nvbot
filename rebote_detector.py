
import time
import datetime
import statistics

# Este archivo asume que ya tienes un cliente de Binance configurado como `exchange`
# y que estás usando ccxt para obtener datos de mercado

def calcular_promedios_vh(exchange, symbol, intervals=["30m", "1h", "4h", "6h", "12h", "1d"]):
    promedios = {}
    for interval in intervals:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=100)
            precios = [candle[4] for candle in ohlcv]  # precios de cierre
            promedio = sum(precios) / len(precios)
            promedios[interval] = promedio
        except Exception as e:
            print(f"Error en {symbol} intervalo {interval}: {e}")
    return promedios


def detectar_rebotes(exchange, symbol):
    señales = []
    ahora = int(time.time() * 1000)

    # Detectar rebotes en 5-30min (para rebotes 5%–10%)
    for intervalo, lapso in [("1m", 30), ("3m", 15), ("5m", 6)]:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=intervalo, limit=lapso)
            precios = [c[4] for c in ohlcv]
            maximo = max(precios)
            minimo = min(precios)
            variacion = ((maximo - minimo) / minimo) * 100

            if 5 <= variacion <= 10:
                señales.append({
                    "symbol": symbol,
                    "intervalo": intervalo,
                    "lapso": lapso,
                    "variacion": round(variacion, 2),
                    "tipo": "rebote 5-10%",
                })
        except:
            continue

    # Detectar rebotes en 2–5min (para rebotes del 2.5%)
    for intervalo, lapso in [("1m", 5), ("1m", 3)]:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=intervalo, limit=lapso)
            precios = [c[4] for c in ohlcv]
            maximo = max(precios)
            minimo = min(precios)
            variacion = ((maximo - minimo) / minimo) * 100

            if 2.3 <= variacion <= 2.7:  # tolerancia de ±0.2%
                señales.append({
                    "symbol": symbol,
                    "intervalo": intervalo,
                    "lapso": lapso,
                    "variacion": round(variacion, 2),
                    "tipo": "rebote 2.5%",
                })
        except:
            continue

    return señales


def evaluar_probabilidad(signal_data):
    # Esto es un prototipo: puedes expandirlo con análisis real
    # Por ahora: si el rebote es consistente y reciente, asumimos probabilidad alta
    # Podrías usar modelos estadísticos, RSI, volumen, etc.
    return 0.87  # Simulado como > 85%


def sugerir_entrada(exchange, symbol, intervalo="1m"):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=intervalo, limit=10)
        precios = [c[4] for c in ohlcv]
        tendencia = precios[-1] > precios[-2] > precios[-3]
        punto = precios[-1]
        return {
            "symbol": symbol,
            "entrada_recomendada": punto,
            "momento": "bueno" if tendencia else "neutral"
        }
    except:
        return None
