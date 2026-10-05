# Análisis de Sensores Industriales

## Objetivo

El objetivo de este proyecto es analizar un conjunto de mediciones simuladas obtenidas de sensores industriales instalados en cuatro plantas. El programa procesa las mediciones de temperatura y vibración y genera información útil sobre los sensores y las alertas de temperatura.

## Descripción de los datos

El archivo utilizado es:

`data/sensores_industriales.csv`

El archivo contiene 100,000 mediciones simuladas.

Las columnas son:

* `id_registro`: identificador de la medición.
* `fecha_hora`: fecha y hora de la lectura.
* `id_sensor`: identificador del sensor.
* `planta`: planta donde está instalado el sensor.
* `temperatura_c`: temperatura registrada en grados Celsius.
* `vibracion_mm_s`: vibración registrada en milímetros por segundo.

Los datos utilizados en este proyecto son simulados y se proporcionan únicamente con fines académicos.

## Requisitos

Se necesita:

* Python 3.
* Git.

El programa utiliza únicamente la biblioteca estándar de Python, por lo que no se requieren dependencias externas.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Jacobo717/examen_sensores.git
```

Entrar al proyecto:

```bash
cd examen_sensores
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows:

```powershell
.venv\Scripts\activate
```

## Ejecución

Ejecutar el programa con:

```powershell
python analisis.py
```

El programa muestra:

* Cantidad total de registros.
* Cantidad de sensores distintos.
* Temperatura promedio por planta.
* Temperatura máxima y los datos relacionados.
* Cantidad de alertas de temperatura.
* Planta o plantas con mayor cantidad de alertas.

También genera automáticamente:

```text
resultados/alertas.csv
```

Este archivo contiene las lecturas cuya temperatura es mayor que 85 °C y conserva las columnas originales.

## Umbral de alerta

Para este ejercicio se considera una alerta cuando:

```text
temperatura > 85 °C
```

Una temperatura de exactamente 85 °C no se considera alerta.

## Reproducibilidad

El proyecto utiliza rutas relativas y puede ser ejecutado desde una segunda copia del repositorio siguiendo únicamente las instrucciones de este README.

## Estructura del proyecto

```text
examen_sensores/
├── data/
│   └── sensores_industriales.csv
├── resultados/
│   └── alertas.csv
├── evidencias/
├── analisis.py
├── informe.md
├── README.md
├── requirements.txt
└── .gitignore
```
