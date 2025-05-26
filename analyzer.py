import numpy as np

def analizar_tendencia(df):
    close = df["close"]
    rsi = df["RSI"].iloc[-1]
    ema_8 = df["EMA_8"].iloc[-1]
    ema_21 = df["EMA_21"].iloc[-1]
    precio_actual = close.iloc[-1]
    precio_promedio = close.mean()
    tendencia = "ESTABLE"
    
    if precio_actual > ema_8 > ema_21 and rsi < 70:
        tendencia = "ALCISTA"
    elif precio_actual < ema_8 < ema_21 and rsi > 30:
        tendencia = "BAJISTA"
    
    variacion = ((precio_actual - precio_promedio) / precio_promedio) * 100

    probabilidad = 70
    lapso_estimado = "N/A"
    rango_subida = 0

    if tendencia == "ALCISTA" and rsi < 30:
        probabilidad = 88
        rango_subida = 5
        lapso_estimado = "3-15min"
    elif tendencia == "ALCISTA" and rsi < 40:
        probabilidad = 85
        rango_subida = 7.5
        lapso_estimado = "15min-2h"
    elif tendencia == "ALCISTA" and rsi < 50:
        probabilidad = 82
        rango_subida = 10
        lapso_estimado = "2-6h"
    elif tendencia == "ALCISTA" and rsi < 60:
        probabilidad = 78
        rango_subida = 12.5
        lapso_estimado = "6-12h"
    elif tendencia == "ALCISTA" and rsi < 65:
        probabilidad = 73
        rango_subida = 17.5
        lapso_estimado = "12h+"
    elif tendencia == "BAJISTA":
        probabilidad = 90
        rango_subida = -2.5
        lapso_estimado = "Corto plazo"

    return {
        "tendencia": tendencia,
        "rango_subida": rango_subida,
        "lapso": lapso_estimado,
        "probabilidad": probabilidad,
        "rsi": rsi,
        "precio_actual": precio_actual
    }
