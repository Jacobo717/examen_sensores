import csv

# Ruta del archivo CSV
ruta = "data/sensores_industriales.csv"

# Lista para guardar los registros
registros = []

# Leer el archivo
with open(ruta, "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        fila["temperatura_c"] = float(fila["temperatura_c"])
        fila["vibracion_mm_s"] = float(fila["vibracion_mm_s"])
        registros.append(fila)


# 1. Cantidad de registros
print("===== ANALISIS DE SENSORES INDUSTRIALES =====")
print()
print("Cantidad de registros:", len(registros))


# 2. Cantidad de sensores distintos
sensores = set()

for fila in registros:
    sensores.add(fila["id_sensor"])

print("Cantidad de sensores distintos:", len(sensores))


# 3. Temperatura promedio de cada planta
temperaturas_por_planta = {}

for fila in registros:
    planta = fila["planta"]
    temperatura = fila["temperatura_c"]

    if planta not in temperaturas_por_planta:
        temperaturas_por_planta[planta] = []

    temperaturas_por_planta[planta].append(temperatura)

print()
print("Temperatura promedio por planta:")

promedios = {}

for planta in temperaturas_por_planta:
    temperaturas = temperaturas_por_planta[planta]
    promedio = sum(temperaturas) / len(temperaturas)
    promedios[planta] = promedio

    print(planta, ":", round(promedio, 2), "°C")


# 4. Temperatura máxima, sensor y fecha
temperatura_maxima = max(fila["temperatura_c"] for fila in registros)

print()
print("Temperatura máxima:", temperatura_maxima, "°C")
print("Registros con la temperatura máxima:")

for fila in registros:
    if fila["temperatura_c"] == temperatura_maxima:
        print(
            "Sensor:",
            fila["id_sensor"],
            "| Fecha:",
            fila["fecha_hora"]
        )


# 5. Lecturas con temperatura mayor que 85 °C
alertas = []

for fila in registros:
    if fila["temperatura_c"] > 85:
        alertas.append(fila)

print()
print("Cantidad de alertas de temperatura:", len(alertas))


# 6. Planta con más alertas
alertas_por_planta = {}

for fila in alertas:
    planta = fila["planta"]

    if planta not in alertas_por_planta:
        alertas_por_planta[planta] = 0

    alertas_por_planta[planta] += 1

if len(alertas_por_planta) > 0:
    max_alertas = max(alertas_por_planta.values())

    print()
    print("Planta(s) con más alertas:")

    for planta in alertas_por_planta:
        if alertas_por_planta[planta] == max_alertas:
            print(planta, ":", max_alertas, "alertas")
else:
    print()
    print("No se encontraron alertas.")


# 7. Exportar todas las alertas a resultados/alertas.csv
columnas = [
    "id_registro",
    "fecha_hora",
    "id_sensor",
    "planta",
    "temperatura_c",
    "vibracion_mm_s"
]

ruta_salida = "resultados/alertas.csv"

with open(ruta_salida, "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas)

    escritor.writeheader()
    escritor.writerows(alertas)

print()
print("Archivo de alertas generado en:", ruta_salida)