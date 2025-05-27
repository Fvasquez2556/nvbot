
import time
import statistics

def calcular_promedios_vh(exchange, symbol, intervals=["30m", "1h", "4h", "6h", "12h", "1d"]):
    promedios = {}
    for interval in intervals:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=100)
            precios = [candle[4] for candle in ohlcv]
            promedio = sum(precios) / len(precios)
            promedios[interval] = promedio
        except Exception as e:
            print(f"Error en {symbol} intervalo {interval}: {e}")
    return promedios

def detectar_rebotes(exchange, symbol):
    señales = []
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
                    "precios": precios,
                    "minimo": minimo,
                    "maximo": maximo
                })
        except Exception:
            continue
    return señales

def evaluar_probabilidad(signal_data):
    precios = signal_data.get("precios", [])
    if not precios or len(precios) < 3:
        return 0.0

    # Detecta consistencia: velas crecientes consecutivas
    crecientes = sum(1 for i in range(1, len(precios)) if precios[i] > precios[i - 1])
    tendencia_fuerte = crecientes >= len(precios) * 0.7

    variacion = signal_data.get("variacion", 0)
    base_score = min(1.0, variacion / 10)  # más variación, más score base

    if tendencia_fuerte:
        return round(min(1.0, base_score + 0.15), 2)
    return round(base_score, 2)

def sugerir_entrada(exchange, symbol, intervalo="1m"):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=intervalo, limit=10)
        cierres = [c[4] for c in ohlcv]
        minimos = [c[3] for c in ohlcv]
        punto_entrada = min(minimos[-3:])  # punto de menor precio reciente

        # verificar impulso
        impulso = cierres[-1] > cierres[-2] > cierres[-3]
        momento = "bueno" if impulso else "débil"

        return {
            "symbol": symbol,
            "entrada_recomendada": round(punto_entrada, 6),
            "momento": momento
        }
    except Exception as e:
        print(f"[Entrada error] {symbol}: {e}")
        return None
