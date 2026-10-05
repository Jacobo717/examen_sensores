import csv

ruta = "data/sensores_industriales.csv"

with open(ruta, "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    print("Columnas:")
    print(lector.fieldnames)

    contador = 0

    for fila in lector:
        contador += 1

print("Cantidad de registros:", contador)