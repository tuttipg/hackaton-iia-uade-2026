# T08 · ¿Este jugador profesional se quema en el split?

> **Hackatón IIA · UADE · 3.4.257.**

**Integrantes:** Camila Roberts · <completar nombre y apellido>
**IA declarada:** ChatGPT
**Pista:** Reglas
**Publicación en LinkedIn:** pendiente

---

## 1. Formulación y PEAS

**La pregunta.** Para cada jugador en un mes, ¿su rendimiento va a caer fuerte el mes siguiente? **SÍ** significa que el sistema detecta riesgo de burnout/agotamiento asociado a una caída fuerte de rendimiento.

| PEAS | Su sistema |
|---|---|
| Medida de rendimiento | Detectar correctamente los casos de riesgo, priorizando no dejar pasar jugadores que realmente caerán de rendimiento. Se reportan exactitud, precisión, sensibilidad y especificidad. |
| Entorno | Un equipo profesional de esports durante un split; cada caso representa a un jugador observado durante un mes. |
| Actuadores | Emitir una alerta SÍ/NO al cuerpo técnico para que evalúe una intervención o descanso. |
| Sensores | Días libres del mes, horas de sueño promedio, partidas oficiales del mes y horas de práctica por día. |

**Objetivo y métrica.** El objetivo real es detectar a tiempo a jugadores con riesgo de una caída fuerte de rendimiento para que el cuerpo técnico pueda intervenir. La métrica no es el objetivo: es una forma de medir qué tan bien se aproxima el sistema a ese objetivo. Como el falso negativo es el error más caro, la **sensibilidad** es especialmente importante, aunque se reportan las cuatro métricas exigidas. Las horas de práctica son una variable de entrada y un proxy de compromiso, no el objetivo a maximizar.

## 2. El sistema

**Cómo decide.** Se usa un sistema de reglas si-entonces. Predice **SÍ** cuando se cumple al menos una de estas reglas:

1. **R1 — carga competitiva alta:** si hay **20 o más partidas oficiales**, entonces SÍ.
2. **R2 — muy pocos días libres + práctica alta:** si hay **2 o menos días libres** y **11 o más horas de práctica por día**, entonces SÍ.
3. Si no se cumple ninguna regla, predice **NO**.

Los umbrales de esta versión se fijaron a partir de los **casos 1–14 de entrenamiento**. R1 separa los dos positivos de entrenamiento con mayor carga competitiva (casos 5 y 6), y R2 separa los otros tres positivos (2, 4 y 11) mediante la combinación de pocos días libres y práctica alta. Los casos 15–20 se usan únicamente para medir.

**Variables que usa y por qué.**
- **Días libres:** representa oportunidad de recuperación.
- **Horas de sueño:** representa recuperación diaria.
- **Partidas oficiales:** aproxima carga competitiva.
- **Horas de práctica:** aproxima carga de entrenamiento/compromiso.

No se utiliza la columna `resultado_real` para decidir un caso nuevo. Tampoco se usa el nombre del conjunto (entrenamiento/prueba) como entrada del sistema.

**Cómo se corre en vivo.** Hay dos opciones equivalentes. La más rápida para la mesa es abrir el notebook `T08_colab.ipynb` en Google Colab: [Abrir T08 en Colab](https://colab.research.google.com/github/tuttipg/hackaton-iia-uade-2026/blob/main/T08_colab.ipynb). Ejecuten la primera celda y luego la celda marcada **EJECUTAR ESTA CELDA EN LA MESA**, ingresando los cuatro valores del caso nuevo.\n\nComo alternativa, el archivo `T08_sistema.py` implementa exactamente las mismas reglas y puede ejecutarse de dos formas:

```bash
python T08_sistema.py
```

para ingresar los cuatro valores de forma interactiva, o:

```bash
python T08_sistema.py <dias_libres> <horas_sueno> <partidas_oficiales> <horas_practica>
```

Por ejemplo:

```bash
python T08_sistema.py 4 6.0 9 8
```

devuelve **SÍ**, porque activa R3.

**Dos casos de ejemplo.**

| Caso inventado | Valores | Salida del sistema |
|---|---|---|
| A | 1 día libre, 8 h de sueño, 21 partidas, 6 h de práctica | SÍ — R1 |
| B | 7 días libres, 7,5 h de sueño, 15 partidas, 10 h de práctica | NO — ninguna regla se activa |

## 3. Medición

La lógica de decisión usa únicamente las cuatro variables disponibles en el momento de decidir. Los casos 1–14 se consideran entrenamiento y los 15–20 se usan para medir la prueba.

**Entrenamiento (casos 1–14)**

| | Predice SÍ | Predice NO |
|---|---:|---:|
| **Real SÍ** | VP = 5 | FN = 0 |
| **Real NO** | FP = 0 | VN = 9 |

**Prueba (casos 15–20)**

| | Predice SÍ | Predice NO |
|---|---:|---:|
| **Real SÍ** | VP = 2 | FN = 1 |
| **Real NO** | FP = 1 | VN = 2 |

| Métrica | Entrenamiento | Prueba |
|---|---:|---:|
| Exactitud | 100% | 66,7% |
| Precisión | 100% | 66,7% |
| Sensibilidad | 100% | 66,7% |
| Especificidad | 100% | 66,7% |

**Entrenamiento contra prueba.** El sistema pasa de **100% en entrenamiento a 66,7% en prueba**. Esa caída indica que las reglas ajustadas sobre los casos 1–14 **no generalizan perfectamente** a casos nuevos y es compatible con cierto sobreajuste al conjunto de entrenamiento. Aun así, en prueba supera la línea base trivial del 50%. Por lo tanto, hablamos de **generalización parcial**, no de una solución perfecta. Además, son solo 6 casos sintéticos de prueba, por lo que el resultado no demuestra eficacia sobre jugadores reales.

## 4. El error más caro

El error más caro es el **falso negativo**: predecir NO cuando el jugador realmente iba a sufrir una caída fuerte de rendimiento. Según la ficha, esto implica no detectar el agotamiento, que el jugador rinda mal y que incluso pueda dejar el equipo.

Por ese motivo se prioriza la **sensibilidad** al evaluar el sistema. En la primera versión se había agregado R3 para reducir falsos negativos, pero esa regla se ajustó después de haber observado la prueba y por eso se eliminó: preferimos una medición honesta antes que optimizar retrospectivamente los casos 15–20. Un falso positivo también tiene costo —dar descanso a quien estaba bien y perder ritmo—, pero su consecuencia es menos grave que ignorar un burnout real.

## 5. ¿Comparado contra qué?

**Línea base trivial.** Como en entrenamiento hay 9 casos NO de 14, un sistema que respondiera siempre NO tendría **64,3% de exactitud** en entrenamiento, pero **0% de sensibilidad**: no detectaría ningún caso de riesgo. En prueba hay 3 NO de 6, por lo que la misma línea base tendría **50% de exactitud** y nuevamente **0% de sensibilidad**. Nuestro sistema obtiene **66,7% de exactitud y 66,7% de sensibilidad** en prueba: supera la línea base, aunque todavía deja un falso negativo.

| Checklist (Clase 6) | Respuesta |
|---|---|
| ¿Qué datos? | 20 casos sintéticos de la ficha T08. Casos 1–14 para construir/ajustar y 15–20 para prueba. Variables: días libres, sueño, partidas oficiales y práctica diaria. |
| ¿Qué métrica? | Exactitud, precisión, sensibilidad y especificidad. Se prioriza sensibilidad por el costo del falso negativo. |
| ¿Comparado contra qué? | Contra la línea base trivial de responder siempre NO. |
| ¿Quién lo midió? | El grupo, mediante el script reproducible del repositorio y las etiquetas provistas por la cátedra. El evaluador de la cátedra y la mesa constituyen una validación adicional. |

## 6. Riesgo: el camino completo

**Datos → modelo → decisión → consecuencia.**

Los datos mensuales del jugador entran al sistema de reglas. El modelo produce SÍ o NO. El cuerpo técnico recibe esa alerta y puede decidir intervenir o dar descanso. Un riesgo concreto es que las variables sean proxies incompletos: por ejemplo, muchas horas de práctica no implican por sí mismas burnout. Si el modelo confunde carga con agotamiento puede generar un falso positivo y hacer descansar innecesariamente a un jugador; si omite señales de recuperación insuficiente puede generar el falso negativo más costoso y dejar sin intervención a un jugador que realmente estaba en riesgo.

## 7. Bitácora

### Uso de la IA

| # | Qué le pedimos | Qué aceptamos | Qué rechazamos y por qué |
|---|---|---|---|
| 1 | Revisar las bases, la ficha T08, los datos y la rúbrica. | La estructura exigida del README, la separación entrenamiento/prueba y la necesidad de distinguir objetivo de métrica. | Usar datos externos o cambiar la división 1–14 / 15–20, porque las bases lo prohíben. |
| 2 | Proponer un sistema que pudiera ejecutarse y explicarse en vivo. | Un sistema de reglas simple, trazable y reproducible. | Una solución opaca o innecesariamente compleja, porque dificultaría la defensa y la ejecución en mesa. |
| 3 | Analizar el costo de los errores. | Priorizar sensibilidad porque el falso negativo es el error más caro según la ficha. | Tratar la exactitud como única métrica, porque una línea base trivial podría obtener una exactitud engañosa. |
| 4 | Revisar el sistema frente a la checklist de Clase 6. | Aclarar qué datos, métricas, comparador y evaluador se usan, y advertir que 100% en 6 casos de prueba no prueba generalización real. | Presentar el 100% del benchmark como garantía de funcionamiento universal. |

### Corridas contra el evaluador

| Corrida | Nota | Agujero que encontró | Qué cambiamos |
|---|---:|---|---|
| 1 | 9,5/10 | Faltaba explicar sobreajuste/generalización; además cuestionó R2 como posible proxy y preguntó si los umbrales habían mirado prueba. | Eliminamos R3 porque estaba ajustada después de observar prueba, rehacemos la medición con reglas fijadas desde entrenamiento y explicamos generalización parcial. |


### Aclaraciones posteriores a la corrida 1

**¿R2 predice agotamiento o mide cuánto entrena?** Las horas de práctica no son burnout ni el objetivo. Son solamente un **proxy de carga/compromiso**. R2 no usa práctica sola: exige además **2 o menos días libres**. Aun así, reconocemos que esa relación puede fallar fuera del benchmark; por eso la consecuencia del modelo debe ser una alerta para evaluación del cuerpo técnico, no un diagnóstico automático.

**¿Los umbrales salieron de prueba?** La primera versión incluyó R3 después de observar los casos de prueba, lo que hacía que el 100% de prueba fuera metodológicamente débil. Después de la corrida 1 corregimos esto: eliminamos R3 y dejamos solo reglas justificables con los casos 1–14. La prueba se recalculó sin volver a ajustar las reglas.

**¿Qué hacía el sistema antes de R3?** Sin R3, el caso 20 de prueba queda como falso negativo. R3 lo convertía en verdadero positivo y elevaba artificialmente la prueba de 83,3% a 100% en la versión anterior. Precisamente por eso decidimos eliminarla y reportar el desempeño honesto de la versión final.
