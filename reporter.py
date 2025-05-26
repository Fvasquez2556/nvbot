import pandas as pd
from tabulate import tabulate
from analyzer import analizar_tendencia

def mostrar_resultados(df):
    print(df[['close', 'RSI', 'EMA_8', 'EMA_21']].tail())

def mostrar_analisis_individual(df, par="(desconocido)"):
    analisis = analizar_tendencia(df)
    tabla = [[
        par,
        analisis['tendencia'],
        f"{analisis['rango_subida']}%",
        analisis['lapso'],
        f"{analisis['probabilidad']}%",
        f"{analisis['rsi']:.2f}",
        f"{analisis['precio_actual']:.4f}"
    ]]
    headers = ["Par", "Tendencia", "Subida Estimada", "Lapso", "Probabilidad", "RSI", "Precio Actual"]
    print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
