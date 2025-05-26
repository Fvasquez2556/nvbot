import ccxt
import pandas as pd
import time

binance = ccxt.binance()

def obtener_pares_usdt():
    mercados = binance.load_markets()
    pares_usdt = [symbol for symbol in mercados if symbol.endswith("/USDT") and mercados[symbol]['active']]
    return pares_usdt

def obtener_velas(par, timeframe='5m', limite=100):
    try:
        velas = binance.fetch_ohlcv(par, timeframe=timeframe, limit=limite)
        df = pd.DataFrame(velas, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"[{par}] Error al obtener velas: {e}")
        return pd.DataFrame()

def obtener_datos_usdt(timeframe='5m', limite=100, max_pares=10):
    pares = obtener_pares_usdt()
    resultados = {}
    print(f"🔎 Analizando los primeros {max_pares} pares USDT...")
    for par in pares[:max_pares]:  # limitamos para pruebas
        df = obtener_velas(par, timeframe, limite)
        if not df.empty:
            resultados[par] = df
            time.sleep(0.2)  # para evitar rate limit
    return resultados

# Prueba
if __name__ == "__main__":
    datos = obtener_datos_usdt()
    for par, df in datos.items():
        print(f"✅ {par} - Último precio: {df['close'].iloc[-1]}")
