import math


def resolver_sistema_2x2(a1, b1, c1, a2, b2, c2):
    """Resuelve a1*x + b1*y = c1 y a2*x + b2*y = c2 mediante Regla de Cramer con pasos."""
    det_principal = (a1 * b2) - (b1 * a2)
    pasos = [f"Determinante Principal (Δ) = ({a1} × {b2}) - ({b1} × {a2}) = {det_principal:.4f}"]
    if abs(det_principal) < 1e-9:
        det_dx = (c1 * b2) - (b1 * c2)
        if abs(det_dx) < 1e-9:
            return {"tipo": "infinitas", "mensaje": "Sistema Compatible Indeterminado (Infinitas soluciones)", "pasos": pasos}
        return {"tipo": "incompatible", "mensaje": "Sistema Incompatible (Sin solución)", "pasos": pasos}

    det_x = (c1 * b2) - (b1 * c2)
    det_y = (a1 * c2) - (c1 * a2)
    x = det_x / det_principal
    y = det_y / det_principal

    pasos.extend([
        f"Determinante X (Δx) = ({c1} × {b2}) - ({b1} × {c2}) = {det_x:.4f}",
        f"Determinante Y (Δy) = ({a1} × {c2}) - ({c1} × {a2}) = {det_y:.4f}",
        f"x = Δx / Δ = {x:.4f}",
        f"y = Δy / Δ = {y:.4f}",
    ])
    return {"tipo": "unico", "x": x, "y": y, "det": det_principal, "pasos": pasos}


def analizar_funcion_cuadratica(a, b, c):
    """Calcula vértice, raíces, concavidad y discriminante de f(x) = ax² + bx + c."""
    if abs(a) < 1e-9:
        return {"error": "El coeficiente 'a' no puede ser 0 en una función cuadrática."}

    vx = -b / (2 * a)
    vy = a * (vx ** 2) + (b * vx) + c
    disc = (b ** 2) - (4 * a * c)

    if disc > 0:
        r1 = (-b + math.sqrt(disc)) / (2 * a)
        r2 = (-b - math.sqrt(disc)) / (2 * a)
        raices = sorted([r1, r2])
    elif abs(disc) < 1e-9:
        raices = [round(-b / (2 * a), 6)]
    else:
        raices = []

    return {
        "vertice": (round(vx, 6), round(vy, 6)),
        "tipo_vertice": "Mínimo" if a > 0 else "Máximo",
        "discriminante": disc,
        "raices": raices,
        "corte_y": (0, c),
        "orientacion": "Hacia arriba (Concavidad positiva)" if a > 0 else "Hacia abajo (Concavidad negativa)",
    }


def optimizacion_programacion_lineal_2d(c1, c2, puntos_vertices, tipo="max"):
    """Evalúa la función Z = c1*x + c2*y en los vértices de la región factible."""
    if not puntos_vertices:
        return {"error": "Debe ingresar al menos un punto vértice para optimizar."}

    if tipo not in {"max", "min"}:
        return {"error": "El tipo debe ser 'max' o 'min'."}

    resultados = []
    mejor = None
    mejor_z = float("-inf") if tipo == "max" else float("inf")

    for (x, y) in puntos_vertices:
        z = c1 * x + c2 * y
        resultados.append({"x": x, "y": y, "z": z})
        if (tipo == "max" and z > mejor_z) or (tipo == "min" and z < mejor_z):
            mejor_z = z
            mejor = {"x": x, "y": y, "z": z}

    if mejor is None:
        return {"error": "No se pudo determinar un óptimo para los puntos ingresados."}

    return {"evaluaciones": resultados, "optimo": mejor, "tipo": tipo}
