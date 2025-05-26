# Funciones de indicadores técnicos (RSI, EMA, etc.)
import pandas as pd

def calcular_rsi(data, period=14):
    delta = data['close'].diff()
    ganancia = delta.where(delta > 0, 0.0)
    perdida = -delta.where(delta < 0, 0.0)

    media_ganancia = ganancia.rolling(window=period).mean()
    media_perdida = perdida.rolling(window=period).mean()

    rs = media_ganancia / media_perdida
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

def calcular_ema(data, period=14, column='close', nombre_columna=None):
    if nombre_columna is None:
        nombre_columna = f'EMA_{period}'
    data[nombre_columna] = data[column].ewm(span=period, adjust=False).mean()
    return data
