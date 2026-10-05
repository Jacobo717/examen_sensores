# INFORME — MANEJO MASIVO DE DATOS

## 1. Las 5 V aplicadas al proyecto

Las 5 V permiten analizar las características de los datos y las necesidades del sistema de sensores industriales.

| V         | ¿Cómo se relaciona con el proyecto?                                                                    | Ejemplo                                                                                               | ¿Dónde aparece?                                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Volumen   | El sistema almacena una gran cantidad de mediciones de sensores.                                       | El archivo actual contiene 100,000 mediciones. En el futuro se planea trabajar con miles de sensores. | 100,000 registros aparecen en el CSV actual. Miles de sensores corresponden a la ampliación.                                |
| Velocidad | Los sensores generan mediciones continuamente y la frecuencia puede aumentar.                          | Actualmente se registra una medición por minuto y en el futuro se recibiría una medición por segundo. | La medición por minuto corresponde al escenario actual. La medición por segundo es parte de la ampliación.                  |
| Variedad  | El sistema podría trabajar con diferentes tipos de información además de datos numéricos.              | Fotografías de las máquinas y reportes de mantenimiento.                                              | Las fotografías y reportes corresponden a la futura ampliación.                                                             |
| Veracidad | Es importante comprobar que las mediciones sean confiables antes de utilizarlas para tomar decisiones. | Revisar si una lectura de temperatura o vibración es válida o presenta un valor anormal.              | La necesidad de verificar los datos aplica al sistema; el CSV actual contiene las mediciones estructuradas de los sensores. |
| Valor     | El análisis de los datos permite obtener información útil para la supervisión de las máquinas.         | Detectar lecturas superiores a 85 °C para generar una alerta.                                         | Aparece en el análisis actual del CSV.                                                                                      |

---

# 2. Tipos de datos y procesamiento tradicional

## CSV de sensores

El archivo CSV es un dato **estructurado**, porque está organizado mediante filas y columnas con campos definidos.

Las columnas del archivo son:

* `id_registro`
* `fecha_hora`
* `id_sensor`
* `planta`
* `temperatura_c`
* `vibracion_mm_s`

## Mensaje JSON enviado por un sensor

Un mensaje JSON es un dato **semiestructurado**, porque contiene información organizada mediante claves y valores, pero no utiliza una estructura de filas y columnas tan rígida como una tabla.

## Fotografía de una máquina

Una fotografía es un dato **no estructurado**, porque la información principal está contenida en una imagen y no en registros tabulares.

## Texto libre de un reporte de mantenimiento

El texto libre de un reporte de mantenimiento es un dato **no estructurado**, porque no tiene una estructura fija de filas, columnas o campos definidos.

## ¿Por qué 100,000 registros no convierten automáticamente al archivo en Big Data?

Tener 100,000 registros no significa automáticamente que los datos sean Big Data.

Big Data no depende únicamente de la cantidad de registros. También se consideran características como el volumen, la velocidad, la variedad, la veracidad y el valor de los datos.

En este caso, el archivo actual puede ser procesado con herramientas tradicionales en una computadora convencional. Sin embargo, al aumentar la escala podrían aparecer limitaciones de almacenamiento, procesamiento y tiempo de respuesta.

Además, la incorporación de fotografías y reportes de mantenimiento aumentaría la variedad de los datos.

---

# 3. Batch y Streaming

## Procesamiento realizado

El análisis realizado en este proyecto corresponde a **procesamiento Batch**.

Esto se debe a que el programa primero recibe un archivo CSV que ya está almacenado y después procesa sus registros para obtener los resultados.

El proceso es:

```text
Archivo CSV
     ↓
Programa Python
     ↓
Procesamiento de los registros
     ↓
Resultados
     ↓
alertas.csv
```

## Alerta en pocos segundos

Para emitir una alerta pocos segundos después de recibir una lectura mayor que 85 °C utilizaría **Streaming**.

Esto permitiría procesar cada medición conforme llega y generar una respuesta casi inmediata.

```text
Sensor
  ↓
Nueva medición
  ↓
Streaming
  ↓
¿Temperatura > 85 °C?
  ↓
Alerta inmediata
```

## Resumen al terminar el día

Para generar un resumen al terminar el día utilizaría **Batch**.

En este caso no es necesario responder inmediatamente a cada lectura, porque el objetivo es analizar todas las mediciones acumuladas durante el día.

```text
Mediciones del día
       ↓
   Almacenamiento
       ↓
     Batch
       ↓
Resumen diario
```

## Justificación

La elección depende del tiempo en que se necesita obtener el resultado.

Si se necesita una respuesta casi inmediata, conviene Streaming.

Si el resultado puede generarse después de acumular los datos, conviene Batch.

---

# 4. Arquitecturas Lambda y Kappa

## Escenario A

La empresa quiere combinar una ruta que recalcule el historial por lotes con otra que procese rápidamente las mediciones recientes.

Para este escenario utilizaría una **arquitectura Lambda**, porque combina procesamiento Batch y procesamiento rápido de datos recientes.

### Diagrama

```text
                    DATOS DE SENSORES
                           |
                           v
                 +---------------------+
                 |    Datos almacenados|
                 +---------------------+
                    /               \
                   /                 \
                  v                   v
        +----------------+   +----------------+
        |  Capa Batch    |   | Capa Streaming |
        |  Históricos    |   | Datos recientes|
        +----------------+   +----------------+
                  \                   /
                   \                 /
                    v               v
                 +---------------------+
                 |      RESULTADOS     |
                 +---------------------+
```

La capa Batch permite recalcular información histórica, mientras que la capa Streaming permite obtener resultados de las mediciones recientes con menor tiempo de espera.

---

## Escenario B

La empresa quiere utilizar una sola lógica de procesamiento de eventos y conservar las mediciones para volver a procesarlas cuando sea necesario.

Para este escenario utilizaría una **arquitectura Kappa**, porque se basa en una sola ruta de procesamiento de eventos.

### Diagrama

```text
             SENSORES
                |
                v
      +-------------------+
      | Eventos / Stream  |
      +-------------------+
                |
                v
      +-------------------+
      | Procesamiento     |
      | de eventos        |
      +-------------------+
                |
                v
         +-------------+
         | Resultados  |
         +-------------+
                |
                v
       +----------------+
       | Almacenamiento |
       | de eventos     |
       +----------------+
                |
                +-------> Reprocesamiento
```

La conservación de los eventos permite volver a procesar los datos cuando sea necesario sin depender de una segunda lógica de procesamiento.

---

# 5. Analítica descriptiva, predictiva y prescriptiva

## 5.1 Analítica descriptiva

La analítica descriptiva permite conocer qué ocurrió en los datos.

A partir de la ejecución de `analisis.py` se obtuvieron los siguientes resultados:

### Cantidad de registros

El archivo contiene:

**100,000 registros.**

### Sensores distintos

Se identificaron:

**40 sensores distintos.**

### Temperatura promedio por planta

Los promedios obtenidos fueron:

```text
Planta_1 : 66.62 °C
Planta_2 : 66.53 °C
Planta_3 : 66.77 °C
Planta_4 : 66.67 °C
```

### Temperatura máxima

La temperatura máxima registrada fue:

**104.99 °C**

Los registros con esta temperatura máxima fueron:

```text
Sensor: S023 | Fecha: 01/09/26 22:23
Sensor: S019 | Fecha: 02/09/26 13:11
Sensor: S014 | Fecha: 02/09/26 15:23
Sensor: S030 | Fecha: 02/09/26 16:02
```

### Cantidad de alertas

Considerando como alerta una temperatura mayor que 85 °C:

**6,954 lecturas fueron identificadas como alerta.**

### Planta con más alertas

La planta con mayor cantidad de alertas fue:

**Planta_3, con 1,777 alertas.**

Estos resultados describen lo que ocurrió en el conjunto de datos analizado.

---

## 5.2 Analítica predictiva

Una pregunta predictiva que podría estudiarse es:

**¿Es posible predecir si una máquina podría presentar un problema de funcionamiento utilizando la evolución de su temperatura y vibración?**

Para investigar esta pregunta sería necesario contar con información adicional, por ejemplo:

* Historial de fallas de las máquinas.
* Historial de mantenimiento.
* Identificación de cada máquina.
* Mediciones históricas de temperatura.
* Mediciones históricas de vibración.
* Condiciones de operación de las máquinas.

Con estos datos sería posible buscar patrones relacionados con posibles fallas futuras.

---

## 5.3 Analítica prescriptiva

Ante un riesgo previsto, una posible acción sería:

**Programar una inspección o mantenimiento preventivo de la máquina.**

Antes de tomar esta decisión sería necesario revisar:

* Temperatura reciente.
* Evolución de la vibración.
* Historial de mantenimiento.
* Alertas anteriores.
* Condiciones de operación.
* Historial de fallas.

La decisión no debe basarse únicamente en una lectura superior a 85 °C, porque una alerta del ejercicio no demuestra por sí sola que una máquina vaya a fallar.

---

# Conclusión

El análisis realizado sobre las 100,000 mediciones permitió identificar 40 sensores distintos, calcular las temperaturas promedio de las cuatro plantas y detectar 6,954 lecturas que superaron el umbral de 85 °C.

La temperatura máxima registrada fue de 104.99 °C y se presentó en cuatro registros. La Planta_3 fue la que presentó la mayor cantidad de alertas, con 1,777.

Actualmente, el archivo puede procesarse mediante herramientas tradicionales como Python. Sin embargo, la futura incorporación de miles de sensores, mediciones por segundo, fotografías y reportes de mantenimiento aumentaría considerablemente el volumen, la velocidad y la variedad de los datos.

Por esta razón, conceptos de Big Data como Batch, Streaming, Lambda, Kappa y los diferentes tipos de analítica son importantes para diseñar una solución que pueda crecer con las necesidades de la empresa.
