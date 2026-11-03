# T08 · ¿Este jugador profesional se quema en el split?

> **Hackatón IIA · UADE · 3.4.257.**

**Integrantes:** Camila Roberts · Tomas Perez Genestouse
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

1. **R1 — carga competitiva alta + recuperación limitada:** si hay **20 o más partidas oficiales** y además hay **5 o menos días libres** o **6 horas o menos de sueño**, entonces SÍ.
2. **R2 — muy pocos días libres + práctica alta:** si hay **2 o menos días libres** y **11 o más horas de práctica por día**, entonces SÍ.
3. Si no se cumple ninguna regla, predice **NO**.

**De dónde salen las reglas.** Se fijan con los casos **1–14 de entrenamiento**. Una primera versión con solo R1 detectaba los positivos 5 y 6, pero dejaba como falsos negativos los casos 2, 4 y 11. Como el falso negativo es el error más caro, agregamos R2: con eso los FN de entrenamiento bajan de **3 a 0** sin generar falsos positivos en entrenamiento. No agregamos nuevas reglas para corregir errores observados en los casos 15–20.

**Variables que usa y por qué.**
- **Días libres:** representa oportunidad de recuperación.
- **Horas de sueño:** representa recuperación diaria.
- **Partidas oficiales:** aproxima carga competitiva.
- **Horas de práctica:** aproxima carga de entrenamiento/compromiso.

No se utiliza la columna `resultado_real` para decidir un caso nuevo. Tampoco se usa el nombre del conjunto (entrenamiento/prueba) como entrada del sistema.

**Cómo se corre en vivo.** Hay dos opciones equivalentes. La más rápida para la mesa es abrir el notebook `T08_colab.ipynb` en Google Colab: [Abrir T08 en Colab](https://colab.research.google.com/github/tuttipg/hackaton-iia-uade-2026/blob/main/T08_colab.ipynb). Ejecuten la primera celda y luego la celda marcada **EJECUTAR ESTA CELDA EN LA MESA**, ingresando los cuatro valores del caso nuevo.

Como alternativa, el archivo `T08_sistema.py` implementa exactamente las mismas reglas y puede ejecutarse de dos formas:

```bash
python T08_sistema.py
```

para ingresar los cuatro valores de forma interactiva, o:

```bash
python T08_sistema.py <dias_libres> <horas_sueno> <partidas_oficiales> <horas_practica>
```

Por ejemplo:

```bash
python T08_sistema.py 1 8.0 21 6
```

devuelve **SÍ**, porque activa **R1: carga competitiva alta + recuperación limitada**.

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
| **Real NO** | FP = 0 | VN = 3 |

| Métrica | Entrenamiento | Prueba |
|---|---:|---:|
| Exactitud | 100% | 83,3% |
| Precisión | 100% | 100% |
| Sensibilidad | 100% | 66,7% |
| Especificidad | 100% | 100% |

**Entrenamiento contra prueba.** El sistema pasa de **100% en entrenamiento a 83,3% en prueba**. En prueba mantiene precisión y especificidad de 100%, pero la sensibilidad baja a **66,7%** porque el caso 20 queda como falso negativo. Esto muestra **generalización parcial** y un límite real del sistema: las reglas aprendidas de entrenamiento no cubren todos los patrones positivos nuevos. No retocamos las reglas para corregir ese caso, porque hacerlo después de observar prueba contaminaría la evaluación.

## 4. El error más caro

El error más caro es el **falso negativo**: predecir NO cuando el jugador realmente iba a sufrir una caída fuerte de rendimiento. Según la ficha, esto implica no detectar el agotamiento, que el jugador rinda mal y que incluso pueda dejar el equipo.

**Qué cambiamos por ese error.** La primera versión tenía solo R1. Esa versión detectaba los positivos 5 y 6, pero dejaba **3 falsos negativos de entrenamiento**: 2, 4 y 11. Por el mayor costo del falso negativo agregamos **R2**, que combina muy pocos días libres con práctica alta. Con R1 + R2, los falsos negativos de entrenamiento bajan de **3 a 0**.

En prueba aparece un nuevo patrón: el **caso 20** queda como falso negativo. Decidimos **no agregar una regla después de verlo**, porque eso sería ajustar el sistema sobre prueba. Lo reportamos como límite de generalización. Así priorizamos sensibilidad durante el diseño sin convertir la prueba en entrenamiento.

## 5. ¿Comparado contra qué?

**Línea base trivial.** Como en entrenamiento hay 9 casos NO de 14, un sistema que respondiera siempre NO tendría **64,3% de exactitud** en entrenamiento, pero **0% de sensibilidad**: no detectaría ningún caso de riesgo. En prueba hay 3 NO de 6, por lo que la misma línea base tendría **50% de exactitud** y **0% de sensibilidad**. Nuestro sistema obtiene **83,3% de exactitud y 66,7% de sensibilidad** en prueba: supera claramente la línea base, aunque todavía deja un falso negativo.



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
| 4 | Revisar el sistema frente a la checklist de Clase 6. | Aclarar qué datos, métricas, comparador y evaluador se usan, y explicar la diferencia entre entrenamiento y prueba. | Presentar el benchmark como garantía de funcionamiento universal o retocar reglas para corregir errores ya vistos en prueba. |

### Aclaraciones posteriores a las corridas del evaluador

**¿R2 predice agotamiento o mide cuánto entrena?** Las horas de práctica no son burnout. Son un **proxy de carga/compromiso** y R2 no las usa solas: exige además **2 o menos días libres**. La salida es una alerta para evaluación del cuerpo técnico, no un diagnóstico automático.

**¿Qué cambiamos para cometer menos falsos negativos?** Agregamos R2 a una versión inicial que tenía solo R1. Eso redujo los FN de entrenamiento de **3 a 0**.

**¿Qué pasa con el caso 20?** Queda como falso negativo en prueba. No lo corregimos agregando una regla nueva después de verlo porque eso sería ajustar sobre prueba y debilitaría la validez del benchmark.

**¿Qué pasó con R3?** Se probó en una iteración intermedia, pero se rechazó para la versión final porque mejoraba específicamente un error ya observado en prueba y era redundante para la matriz de entrenamiento. Quedó registrado como una decisión rechazada en la bitácora.

### Corridas contra el evaluador

| Corrida | Nota | Agujero que encontró | Qué cambiamos |
|---|---:|---|---|
| 1 | 9,5/10 | Faltaba explicar generalización y preguntó por posible ajuste a prueba. | Se explicitó la diferencia entre entrenamiento y prueba y se revisó el riesgo de leakage. |
| 2 | 9/10 | README y código desincronizados; no quedaba claro qué cambio reducía falsos negativos. | Se sincronizó todo y se justificó R2 como cambio que baja FN de entrenamiento de 3 a 0; el caso 20 queda como límite de generalización. |
