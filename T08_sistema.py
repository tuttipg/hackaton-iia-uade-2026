"""
T08 · ¿Este jugador profesional se quema en el split?

Versión final: reglas fijadas con los casos 1–14 de entrenamiento.
Los casos 15–20 se usan para medir y NO se usan para retocar el sistema.
"""

import sys


def predecir_burnout(dias_libres, horas_sueno, partidas_oficiales, horas_practica):
    """
    Devuelve (prediccion, motivo), donde 1 = SÍ y 0 = NO.
    """

    # R1: carga competitiva alta + recuperación limitada.
    if partidas_oficiales >= 20 and (dias_libres <= 5 or horas_sueno <= 6.0):
        return 1, "R1: carga competitiva alta + recuperación limitada"

    # R2: muy pocos días libres + práctica alta.
    # Se agregó para reducir falsos negativos respecto de una versión inicial con solo R1.
    if dias_libres <= 2 and horas_practica >= 11:
        return 1, "R2: muy pocos días libres + práctica alta"

    return 0, "Ninguna regla de riesgo se activó"


CASOS = [
    (1, "entrenamiento", 3, 6.8, 5, 12, 0),
    (2, "entrenamiento", 2, 8.1, 17, 13, 1),
    (3, "entrenamiento", 5, 8.3, 5, 13, 0),
    (4, "entrenamiento", 0, 5.7, 14, 11, 1),
    (5, "entrenamiento", 1, 8.1, 21, 8, 1),
    (6, "entrenamiento", 6, 5.4, 29, 8, 1),
    (7, "entrenamiento", 6, 7.7, 18, 13, 0),
    (8, "entrenamiento", 8, 6.3, 5, 8, 0),
    (9, "entrenamiento", 2, 7.7, 16, 8, 0),
    (10, "entrenamiento", 6, 5.3, 15, 11, 0),
    (11, "entrenamiento", 2, 5.6, 14, 12, 1),
    (12, "entrenamiento", 7, 5.9, 17, 13, 0),
    (13, "entrenamiento", 6, 8.0, 9, 9, 0),
    (14, "entrenamiento", 7, 7.2, 15, 11, 0),
    (15, "prueba", 7, 5.8, 16, 12, 0),
    (16, "prueba", 5, 5.2, 23, 6, 1),
    (17, "prueba", 6, 7.1, 25, 14, 0),
    (18, "prueba", 1, 8.0, 21, 6, 1),
    (19, "prueba", 8, 6.9, 18, 11, 0),
    (20, "prueba", 4, 6.0, 9, 8, 1),
]


def medir(conjunto):
    filas = [c for c in CASOS if c[1] == conjunto]
    vp = vn = fp = fn = 0
    for _, _, dias, sueno, partidas, practica, real in filas:
        pred, _ = predecir_burnout(dias, sueno, partidas, practica)
        if real == 1 and pred == 1:
            vp += 1
        elif real == 0 and pred == 0:
            vn += 1
        elif real == 0 and pred == 1:
            fp += 1
        else:
            fn += 1

    n = len(filas)
    return {
        "VP": vp, "FN": fn, "FP": fp, "VN": vn,
        "exactitud": (vp + vn) / n if n else 0,
        "precision": vp / (vp + fp) if (vp + fp) else 0,
        "sensibilidad": vp / (vp + fn) if (vp + fn) else 0,
        "especificidad": vn / (vn + fp) if (vn + fp) else 0,
    }


def imprimir_medicion():
    for conjunto in ("entrenamiento", "prueba"):
        m = medir(conjunto)
        print(f"\n{conjunto.upper()}")
        print(f"VP={m['VP']}  FN={m['FN']}  FP={m['FP']}  VN={m['VN']}")
        print(
            "Exactitud={:.1%} | Precisión={:.1%} | "
            "Sensibilidad={:.1%} | Especificidad={:.1%}".format(
                m["exactitud"], m["precision"], m["sensibilidad"], m["especificidad"]
            )
        )


def modo_live(args):
    if len(args) == 4:
        dias = float(args[0])
        sueno = float(args[1])
        partidas = float(args[2])
        practica = float(args[3])
    else:
        print("\nMODO EN VIVO · Ingresá el caso nuevo")
        dias = float(input("Días libres en el mes: "))
        sueno = float(input("Horas de sueño promedio: "))
        partidas = float(input("Partidas oficiales en el mes: "))
        practica = float(input("Horas de práctica por día: "))

    pred, motivo = predecir_burnout(dias, sueno, partidas, practica)
    print("\nSALIDA:", "SÍ" if pred == 1 else "NO")
    print("Motivo:", motivo)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        modo_live(sys.argv[1:])
    else:
        imprimir_medicion()
        modo_live([])
