
import time
import os
import csv
from datetime import datetime
from tabulate import tabulate
import ccxt

from scanner import obtener_datos_usdt
from indicators import calcular_rsi, calcular_ema
from analyzer import analizar_tendencia
from rebote_detector import (
    calcular_promedios_vh,
    detectar_rebotes,
    evaluar_probabilidad,
    sugerir_entrada
)

exchange = ccxt.binance({
    "enableRateLimit": True,
})

# Crea carpeta y archivo CSV si no existen
os.makedirs("data", exist_ok=True)
archivo_csv = "data/signals.csv"
if not os.path.exists(archivo_csv):
    with open(archivo_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp", "par", "precio_actual", "tendencia",
            "RSI", "probabilidad", "rango_subida", "lapso"
        ])

def analizar_rebotes_rapidos():
    print("🔎 Ejecutando análisis de rebotes rápidos...\n")
    mercados = exchange.load_markets()
    pares_spot_activos = [
        symbol for symbol, data in mercados.items()
        if data.get("spot", False)
        and data.get("active", True)
        and symbol.endswith("/USDT")
    ]

    for symbol in pares_spot_activos:
        try:
            rebotes = detectar_rebotes(exchange, symbol)
            for rebote in rebotes:
                probabilidad = evaluar_probabilidad(rebote)
                if probabilidad >= 0.85:
                    entrada = sugerir_entrada(exchange, symbol)
                    print(f"📈 Señal detectada en {symbol}")
                    print(f" - Tipo: {rebote['tipo']}")
                    print(f" - Variación: {rebote['variacion']}% en {rebote['lapso']} velas de {rebote['intervalo']}")
                    print(f" - Probabilidad estimada: {round(probabilidad*100, 2)}%")
                    if entrada:
                        print(f" - Entrada sugerida: {entrada['entrada_recomendada']} ({entrada['momento']})")
                    print("-" * 50)
        except Exception as e:
            print(f"[Error] {symbol}: {e}")

def analizar_tendencias_lentas():
    print("📊 Ejecutando análisis de tendencias (RSI/EMA)...")
    datos = obtener_datos_usdt(timeframe="5m", limite=144, max_pares=75)
    resultados_filtrados = []

    for par, df in datos.items():
        if df.empty:
            continue

        df = calcular_rsi(df)
        df = calcular_ema(df, period=8)
        df = calcular_ema(df, period=21)

        analisis = analizar_tendencia(df)

        if (analisis["tendencia"] == "ALCISTA" and 
            analisis["probabilidad"] >= 85 and 
            analisis["rango_subida"] >= 5):

            resultados_filtrados.append([
                par,
                analisis["tendencia"],
                f"{analisis['rango_subida']}%",
                analisis["lapso"],
                f"{analisis['probabilidad']}%",
                f"{analisis['rsi']:.2f}",
                f"{analisis['precio_actual']:.4f}"
            ])

            with open(archivo_csv, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.utcnow().isoformat(),
                    par,
                    analisis["precio_actual"],
                    analisis["tendencia"],
                    round(analisis["rsi"], 2),
                    analisis["probabilidad"],
                    analisis["rango_subida"],
                    analisis["lapso"]
                ])

    if resultados_filtrados:
        headers = ["Par", "Tendencia", "Subida Estimada", "Lapso", "Probabilidad", "RSI", "Precio Actual"]
        print("📈 Señales detectadas:")
        print(tabulate(resultados_filtrados, headers=headers, tablefmt="fancy_grid"))
    else:
        print("⚠️ No se detectaron señales con condiciones de rebote ≥ 85%.")

if __name__ == "__main__":
    print("🔄 Iniciando NVBot con pares activos del mercado Spot...\n")
    while True:
        analizar_rebotes_rapidos()
        analizar_tendencias_lentas()
        print("⏳ Esperando 60 segundos antes del próximo análisis...\n")
        time.sleep(60)
        print("🔄 Reanudando análisis...\n")