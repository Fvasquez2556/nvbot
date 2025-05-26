from scanner import obtener_datos_usdt
from indicators import calcular_rsi, calcular_ema
from analyzer import analizar_tendencia
from tabulate import tabulate
import csv
import os
from datetime import datetime
import time

if __name__ == '__main__':
    print("🔄 Iniciando NVBot...")

    # Crear carpeta data si no existe
    os.makedirs("data", exist_ok=True)
    archivo_csv = "data/signals.csv"

    # Crear archivo y encabezado si no existe
    if not os.path.exists(archivo_csv):
        with open(archivo_csv, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp", "par", "precio_actual", "tendencia",
                "RSI", "probabilidad", "rango_subida", "lapso"
            ])

    # Obtener datos de múltiples pares
    datos = obtener_datos_usdt(timeframe="5m", limite=144, max_pares=75)

    resultados_filtrados = []

    for par, df in datos.items():
        if df.empty:
            continue

        # Calcular indicadores
        df = calcular_rsi(df)
        df = calcular_ema(df, period=8)
        df = calcular_ema(df, period=21)

        # Analizar
        analisis = analizar_tendencia(df)

        # Filtrar señales de subida con probabilidad >= 85%
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

            # Guardar en CSV
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

    # Mostrar resultados finales
    if resultados_filtrados:
        headers = ["Par", "Tendencia", "Subida Estimada", "Lapso", "Probabilidad", "RSI", "Precio Actual"]
        print("\n📈 Señales de posible rebote detectadas:")
        print(tabulate(resultados_filtrados, headers=headers, tablefmt="fancy_grid"))
    else:
        print("\n⚠️ No se detectaron señales con condiciones de rebote ≥ 85%.")
    print("✅ NVBot finalizado.")
    print("🔄 Revisa el archivo data/signals.csv para más detalles.")
    print("🔄 Ejecuta feedback.py para evaluar las señales generadas."
          " ¡Gracias por usar NVBot!")

    # Definir la función para ejecutar un ciclo de escaneo
    def ejecutar_ciclo():
        # Obtener datos de múltiples pares
        datos = obtener_datos_usdt(timeframe="5m", limite=144, max_pares=75)

        resultados_filtrados = []

        for par, df in datos.items():
            if df.empty:
                continue

            # Calcular indicadores
            df = calcular_rsi(df)
            df = calcular_ema(df, period=8)
            df = calcular_ema(df, period=21)

            # Analizar
            analisis = analizar_tendencia(df)

            # Filtrar señales de subida con probabilidad >= 85%
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

                # Guardar en CSV
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

        # Mostrar resultados finales
        if resultados_filtrados:
            headers = ["Par", "Tendencia", "Subida Estimada", "Lapso", "Probabilidad", "RSI", "Precio Actual"]
            print("\n📈 Señales de posible rebote detectadas:")
            print(tabulate(resultados_filtrados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("\n⚠️ No se detectaron señales con condiciones de rebote ≥ 85%.")
        print("✅ NVBot finalizado.")
        print("🔄 Revisa el archivo data/signals.csv para más detalles.")

    # Bucle infinito para escaneo periódico
    while True:
        print("🔄 Iniciando nuevo ciclo de escaneo...\n")
        ejecutar_ciclo()
        print("\n⏳ Esperando 1 minuto antes del próximo ciclo...\n")
        time.sleep(60)  # Espera de 1 minuto (60 segundos)
    
    