import math

# =========================================================================
# 1. CINEMÁTICA Y MOVIMIENTO (MRU / MRUA / ROBÓTICA)
# =========================================================================
def calcular_mru(velocidad=None, distancia=None, tiempo=None):
    """Calcula la variable faltante en un Movimiento Rectilíneo Uniforme (d = v * t)."""

    if sum(v is not None for v in [velocidad, distancia, tiempo]) != 2:
        return {"error": "Debes ingresar exactamente dos de las tres variables (velocidad, distancia, tiempo)."}

    if velocidad is None:
        if distancia is None or tiempo is None or tiempo <= 0:
            return {"error": "La distancia y el tiempo deben ser válidos para calcular la velocidad."}

        v = distancia / tiempo
        return {"variable_calculada": "Velocidad (v)", "resultado": round(v, 4), "unidad": "m/s", "formula": "v = d / t"}

    if distancia is None:
        if velocidad is None or tiempo is None or tiempo <= 0:
            return {"error": "La velocidad y el tiempo deben ser válidos para calcular la distancia."}

        d = velocidad * tiempo
        return {"variable_calculada": "Distancia (d)", "resultado": round(d, 4), "unidad": "m", "formula": "d = v * t"}

    if tiempo is None:
        if velocidad == 0:
            return {"error": "La velocidad no puede ser cero para calcular tiempo."}

        t = distancia / velocidad
        return {"variable_calculada": "Tiempo (t)", "resultado": round(t, 4), "unidad": "s", "formula": "t = d / v"}

    return {"error": "La combinación de variables ingresada no es válida."}


def calcular_mrua(v_inicial, v_final=None, aceleracion=None, tiempo=None, distancia=None):
    """Resuelve ecuaciones de Movimiento Rectilíneo Uniformemente Acelerado."""
    if aceleracion is not None and tiempo is not None:
        if tiempo <= 0:
            return {"error": "El tiempo debe ser mayor a cero."}

        vf = v_inicial + (aceleracion * tiempo)
        d = (v_inicial * tiempo) + (0.5 * aceleracion * (tiempo ** 2))
        return {
            "velocidad_final": round(vf, 4),
            "distancia_recorrida": round(d, 4),
            "aceleracion": aceleracion,
            "tiempo": tiempo,
            "pasos": [
                f"v_f = {v_inicial} + ({aceleracion} × {tiempo}) = {round(vf, 4)} m/s",
                f"d = ({v_inicial} × {tiempo}) + 0.5 × {aceleracion} × ({tiempo}²) = {round(d, 4)} m",
            ],
        }

    if v_final is not None and tiempo is not None:
        if tiempo <= 0:
            return {"error": "El tiempo debe ser mayor a cero."}

        a = (v_final - v_inicial) / tiempo
        d = (v_inicial * tiempo) + (0.5 * a * (tiempo ** 2))
        return {
            "aceleracion": round(a, 4),
            "distancia_recorrida": round(d, 4),
            "velocidad_final": v_final,
            "tiempo": tiempo,
            "pasos": [
                f"a = ({v_final} - {v_inicial}) / {tiempo} = {round(a, 4)} m/s²",
                f"d = ({v_inicial} × {tiempo}) + 0.5 × {round(a, 4)} × ({tiempo}²) = {round(d, 4)} m",
            ],
        }

    return {"error": "Ingresa al menos la velocidad inicial y combinación de (aceleración + tiempo) o (velocidad final + tiempo)."}


# =========================================================================
# 2. DINÁMICA, LEYES DE NEWTON Y FRICCIÓN
# =========================================================================
def calcular_fuerza_newton(masa, aceleracion=None, fuerza=None):
    """Calcula la Segunda Ley de Newton: F = m * a."""
    if masa <= 0:
        return {"error": "La masa debe ser mayor a cero."}

    g = 9.81
    peso = masa * g

    if fuerza is None and aceleracion is not None:
        f = masa * aceleracion
        return {"fuerza_net_N": round(f, 4), "masa_kg": masa, "aceleracion_m_s2": aceleracion, "peso_N": round(peso, 2), "formula": "F = m * a"}

    if aceleracion is None and fuerza is not None:
        a = fuerza / masa
        return {"aceleracion_m_s2": round(a, 4), "fuerza_net_N": fuerza, "masa_kg": masa, "peso_N": round(peso, 2), "formula": "a = F / m"}

    return {"error": "Proporciona la masa y la aceleración o la fuerza aplicada."}


def calcular_fuerza_friccion(masa, coeficiente_friccion, en_plano_inclinado_grados=0):
    """Calcula la Fuerza Normal y la Fuerza de Fricción (f_k = mu * Normal)."""
    g = 9.81
    rad = math.radians(en_plano_inclinado_grados)
    peso = masa * g
    normal = peso * math.cos(rad)
    f_friccion = coeficiente_friccion * normal
    f_paralela_gravedad = peso * math.sin(rad)
    return {"peso_N": round(peso, 2), "fuerza_normal_N": round(normal, 2), "fuerza_friccion_N": round(f_friccion, 2), "fuerza_gravedad_paralela_N": round(f_paralela_gravedad, 2), "coeficiente_mu": coeficiente_friccion, "angulo_grados": en_plano_inclinado_grados}


# =========================================================================
# 3. ELECTRICIDAD, LEY DE OHM Y CIRCUITOS EN HARDWARE
# =========================================================================
def resolver_ley_ohm(voltaje=None, corriente=None, resistencia=None):
    """Calcula V = I * R, Potencia P = V * I."""
    if sum(v is not None for v in [voltaje, corriente, resistencia]) != 2:
        return {"error": "Debes ingresar exactamente dos de los tres parámetros (V, I, R)."}

    if voltaje is None:
        if corriente is None or resistencia is None:
            return {"error": "Faltan datos para calcular el voltaje."}
        v = corriente * resistencia
        i = corriente
        r = resistencia
        p = v * i
        return {"voltaje_V": round(v, 4), "corriente_A": round(i, 4), "corriente_mA": round(i * 1000, 2), "resistencia_Ohm": round(r, 4), "potencia_W": round(p, 4)}

    if corriente is None:
        if voltaje is None or resistencia is None:
            return {"error": "Faltan datos para calcular la corriente."}
        if resistencia == 0:
            return {"error": "La resistencia no puede ser 0 ohmios."}

        i = voltaje / resistencia
        v = voltaje
        r = resistencia
        p = v * i
        return {"voltaje_V": round(v, 4), "corriente_A": round(i, 4), "corriente_mA": round(i * 1000, 2), "resistencia_Ohm": round(r, 4), "potencia_W": round(p, 4)}

    if voltaje is None or corriente is None:
        return {"error": "Faltan variables para completar el cálculo."}

    if corriente == 0:
        return {"error": "La corriente no puede ser 0 amperios."}

    r = voltaje / corriente
    v = voltaje
    i = corriente
    p = v * i
    return {"voltaje_V": round(v, 4), "corriente_A": round(i, 4), "corriente_mA": round(i * 1000, 2), "resistencia_Ohm": round(r, 4), "potencia_W": round(p, 4)}


def analizar_circuito_resistencias(voltaje_fuente, resistencias_lista, tipo_circuito="serie"):
    """Analiza circuitos en Serie o Paralelo con N resistencias."""
    if not resistencias_lista or any(r <= 0 for r in resistencias_lista):
        return {"error": "Ingresa una lista de resistencias válidas con valores mayores a cero."}

    if voltaje_fuente <= 0:
        return {"error": "El voltaje de la fuente debe ser mayor a cero."}

    tipo = tipo_circuito.lower()
    if tipo not in {"serie", "paralelo"}:
        return {"error": "El tipo de circuito debe ser 'serie' o 'paralelo'."}

    if tipo == "serie":
        r_eq = sum(resistencias_lista)
        i_total = voltaje_fuente / r_eq
        p_total = voltaje_fuente * i_total
        caidas = []
        for idx, r in enumerate(resistencias_lista, start=1):
            v_i = i_total * r
            p_i = v_i * i_total
            caidas.append({"resistencia": f"R{idx} ({r} Ω)", "voltaje_V": round(v_i, 3), "corriente_A": round(i_total, 4), "potencia_W": round(p_i, 3)})
        return {"tipo": "Serie", "resistencia_equivalente_Ohm": round(r_eq, 4), "corriente_total_A": round(i_total, 4), "potencia_total_W": round(p_total, 4), "detalles_componentes": caidas}

    inv_r = sum(1.0 / r for r in resistencias_lista)
    r_eq = 1.0 / inv_r
    i_total = voltaje_fuente / r_eq
    p_total = voltaje_fuente * i_total
    caidas = []
    for idx, r in enumerate(resistencias_lista, start=1):
        i_i = voltaje_fuente / r
        p_i = voltaje_fuente * i_i
        caidas.append({"resistencia": f"R{idx} ({r} Ω)", "voltaje_V": round(voltaje_fuente, 3), "corriente_A": round(i_i, 4), "potencia_W": round(p_i, 3)})

    return {"tipo": "Paralelo", "resistencia_equivalente_Ohm": round(r_eq, 4), "corriente_total_A": round(i_total, 4), "potencia_total_W": round(p_total, 4), "detalles_componentes": caidas}


# =========================================================================
# 4. TRABAJO, ENERGÍA Y CONSUMO EN EQUIPOS INFORMÁTICOS
# =========================================================================
def calcular_consumo_energia_equipos(potencia_watts, horas_diarias, dias_mes=30, precio_kwh=50.0):
    """Calcula el consumo eléctrico de servidores/PCs en kWh y costo mensual."""
    kw = potencia_watts / 1000.0
    kwh_dia = kw * horas_diarias
    kwh_mes = kwh_dia * dias_mes
    costo_mes = kwh_mes * precio_kwh
    return {"potencia_watts": potencia_watts, "potencia_kw": round(kw, 3), "kwh_diarios": round(kwh_dia, 3), "kwh_mensuales": round(kwh_mes, 2), "costo_estimado_mensual": round(costo_mes, 2), "precio_kwh_utilizado": precio_kwh}


def calcular_energia_mecanica(masa, velocidad, altura):
    """Calcula Energía Cinética (Ec), Energía Potencial (Ep) y Energía Mecánica Total (Em)."""
    g = 9.81
    ec = 0.5 * masa * (velocidad ** 2)
    ep = masa * g * altura
    em = ec + ep
    return {"energia_cinetica_J": round(ec, 2), "energia_potencial_J": round(ep, 2), "energia_mecanica_total_J": round(em, 2)}


# =========================================================================
# 5. ONDAS, ÓPTICA (SNELL) Y TELECOMUNICACIONES
# =========================================================================
def calcular_ondas_frecuencia_longitud(velocidad_propagacion=300000000.0, frecuencia_hz=None, longitud_onda_m=None):
    """Calcula v = lambda * f (Velocidad de la luz c = 3x10^8 m/s por defecto)."""

    if frecuencia_hz is None and longitud_onda_m is not None:
        if longitud_onda_m <= 0:
            return {"error": "La longitud de onda debe ser mayor a cero."}

        f = velocidad_propagacion / longitud_onda_m
        return {"frecuencia_Hz": round(f, 2), "frecuencia_MHz": round(f / 1e6, 4), "longitud_onda_m": longitud_onda_m, "velocidad_m_s": velocidad_propagacion}

    if longitud_onda_m is None and frecuencia_hz is not None:
        if frecuencia_hz <= 0:
            return {"error": "La frecuencia debe ser mayor a cero."}

        l = velocidad_propagacion / frecuencia_hz
        return {"longitud_onda_m": round(l, 6), "longitud_onda_nm": round(l * 1e9, 2), "frecuencia_Hz": frecuencia_hz, "velocidad_m_s": velocidad_propagacion}

    return {"error": "Ingresa o bien la frecuencia (Hz) o la longitud de onda (m)."}


def calcular_refraccion_snell(n1, n2, angulo_incidencia_grados):
    """Ley de Snell: n1 * sin(theta1) = n2 * sin(theta2) (Fibra Óptica)."""
    if n1 <= 0 or n2 <= 0:
        return {"error": "Los índices de refracción deben ser mayores a cero."}

    rad1 = math.radians(angulo_incidencia_grados)
    sin_theta2 = (n1 * math.sin(rad1)) / n2

    if abs(sin_theta2) > 1.0:
        return {
            "evento": "Reflexión Total Interna (La luz queda atrapada en el núcleo de la fibra óptica)",
            "angulo_critico_grados": round(math.degrees(math.asin(n2 / n1)), 2) if n1 > n2 else "N/A",
        }

    rad2 = math.asin(sin_theta2)
    deg2 = math.degrees(rad2)
    return {"evento": "Refracción Óptica", "angulo_refraccion_grados": round(deg2, 2), "indice_n1": n1, "indice_n2": n2, "angulo_incidencia_grados": angulo_incidencia_grados}
