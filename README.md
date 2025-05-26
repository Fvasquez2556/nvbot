# 🧠 NVBot – Crypto Trend Analyzer

**NVBot** es un bot de análisis de criptomonedas que se conecta a la API de Binance para monitorear todos los pares con USDT, calcular tendencias basadas en indicadores técnicos, y emitir señales confiables de alza, baja o estabilización, todo en tiempo real y con alta precisión.

---

## 🚀 Características

- 🔍 Escaneo automatizado de todos los pares USDT disponibles en Binance.
- 📈 Cálculo de precios promedio desde la última corrección.
- 🧠 Análisis de tendencia con señales: subida, bajada, estabilización.
- 🎯 Enfoque en señales con probabilidad de acierto > 85%.
- 📊 Pronta visualización en terminal (modo consola optimizada).
- 🧪 Registro de retroalimentación del usuario para mejora continua (feedback system).
- 🧰 Modularidad: configuración, análisis, indicadores y feedback separados.

---

## 🖥️ Requisitos del sistema

- Python 3.10 o superior
- Conexión a Internet estable
- Cuenta de Binance con API habilitada (para acceso completo)

---

## ⚙️ Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/Fvasquez2556/nvbot.git
cd nvbot

# 2. (Opcional pero recomendado) Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt
```

---

## 🔐 Configuración del archivo `.env`

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente formato:

```dotenv
BINANCE_API_KEY=tu_api_key
BINANCE_SECRET_KEY=tu_secret_key
```

🔒 **¡Nunca compartas este archivo públicamente!** Está en `.gitignore` por seguridad.

---

## ▶️ Ejecución

```bash
python main.py
```

> Esto iniciará el bot en la consola y comenzará el análisis en tiempo real de los pares USDT.

---

## 📁 Estructura del proyecto

```plaintext
nvbot/
│
├── main.py            # Script principal que orquesta todo
├── config.py          # Configuración del entorno (lectura de .env)
├── analyzer.py        # Análisis de precios, señales y lógica principal
├── indicators.py      # Indicadores técnicos (promedios, etc.)
└── feedback.py        # Registro y manejo de la retroalimentación del usuario
```

---

## 🤝 Contribuciones

¿Quieres aportar mejoras? ¡Eres bienvenido!

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b nueva-funcionalidad`)
3. Haz tus cambios y haz commit (`git commit -am 'Agrega nueva función'`)
4. Sube tu rama (`git push origin nueva-funcionalidad`)
5. Crea un Pull Request

---

## 📜 Licencia

Este proyecto está licenciado bajo la **MIT License**. Puedes usarlo, modificarlo y distribuirlo libremente, siempre que se mantenga el aviso de copyright.

---

## 🙌 Créditos

Desarrollado por [@Fvasquez2556](https://github.com/Fvasquez2556) con pasión por la automatización, las criptomonedas y el análisis de datos.
