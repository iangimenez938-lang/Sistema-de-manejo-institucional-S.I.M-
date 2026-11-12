import math 

# ========================================================================= 
# 1. EVALUACIÓN FÍSICA: IMC, FRECUENCIA CARDÍACA Y ZONAS DE ENTRENAMIENTO 
# ========================================================================= 
def calcular_imc_y_composicion(peso_kg: float, altura_m: float): 
    """Calcula el Índice de Masa Corporal (IMC) y categorización de salud según la OMS."""

    if peso_kg <= 0 or altura_m <= 0:
        return {"error": "El peso y la altura deben ser valores mayores a cero."}

    imc = peso_kg / (altura_m ** 2)
    imc_round = round(imc, 2)

    if imc < 18.5:
        categoria = "Bajo Peso"
        recomendacion = "Se sugiere acompañamiento nutricional para aumentar masa muscular mediante trabajo de fuerza."
    elif 18.5 <= imc < 25.0:
        categoria = "Peso Normal / Saludable"
        recomendacion = "Mantener hábitos de actividad física aeróbica y de fuerza equilibrados."
    elif 25.0 <= imc < 30.0:
        categoria = "Sobrepeso"
        recomendacion = "Incrementar el volumen de ejercicio aeróbico regular y coordinar un plan nutricional adecuado."
    else:
        categoria = "Obesidad"
        recomendacion = "Realizar ejercicio adaptado de bajo impacto articular (natación, caminata) con supervisión médica."

    return {"peso_kg": peso_kg, "altura_m": altura_m, "imc": imc_round, "categoria": categoria, "recomendacion": recomendacion}

def calcular_frecuencia_cardiaca_zonas(edad: int, fc_reposo: int = 70): 
    """Calcula la Frecuencia Cardíaca Máxima (FCM) y las zonas de entrenamiento usando Karvonen."""

    if edad <= 0 or edad >= 110:
        return {"error": "Ingresa una edad válida."}

    fc_max = 220 - edad
    fc_reserva = fc_max - fc_reposo

    def z(pct_min, pct_max):
        f_min = round(fc_reposo + (fc_reserva * pct_min))
        f_max = round(fc_reposo + (fc_reserva * pct_max))
        return f"{f_min} - {f_max} PPM"

    zonas = {
        "Zona 1 - Recuperación / Calentamiento (50%-60%)": z(0.50, 0.60),
        "Zona 2 - Quema de Grasa / Resistencia Aeróbica Base (60%-70%)": z(0.60, 0.70),
        "Zona 3 - Capacidad Aeróbica / Eficiencia Cardiovascular (70%-80%)": z(0.70, 0.80),
        "Zona 4 - Umbral Anaeróbico / Rendimiento Intenso (80%-90%)": z(0.80, 0.90),
        "Zona 5 - Esfuerzo Máximo / Velocidad y Potencia (90%-100%)": z(0.90, 1.00),
    }

    return {"edad": edad, "fc_reposo": fc_reposo, "fc_maxima_fcm": fc_max, "fc_reserva": fc_reserva, "zonas_entrenamiento": zonas}

def evaluar_test_ruffier(p0_reposo: int, p1_post_ejercicio: int, p2_recuperacion: int): 
    """Evalúa la resistencia cardíaca y la capacidad de recuperación mediante Ruffier-Dickson."""
    indice = (p0_reposo + p1_post_ejercicio + p2_recuperacion - 200) / 10.0
    i_round = round(indice, 2)

    if i_round < 0:
        condicion = "Excelente (Corazón de atleta de alto rendimiento)"
    elif i_round <= 5:
        condicion = "Buena (Apto para actividad física intensa)"
    elif i_round <= 10:
        condicion = "Media / Aceptable (Estado físico promedio)"
    elif i_round <= 15:
        condicion = "Insuficiente (Requiere acondicionamiento paulatino)"
    else:
        condicion = "Mala (Se sugiere chequeo cardiovascular médico antes de realizar esfuerzo)"

    return {"indice_ruffier": i_round, "p0_reposo": p0_reposo, "p1_post_ejercicio": p1_post_ejercicio, "p2_recuperacion": p2_recuperacion, "evaluacion": condicion}

# ========================================================================= 
# 2. NUTRICIÓN DEPORTIVA, TASA METABÓLICA Y HIDRATACIÓN 
# ========================================================================= 
def calcular_metabolismo_y_calorias(peso_kg: float, altura_cm: float, edad: int, genero: str = "M", nivel_actividad: str = "moderado"):
    """Calcula la Tasa Metabólica Basal (TMB) y necesidades calóricas diarias."""
    if peso_kg <= 0 or altura_cm <= 0 or edad <= 0:
        return {"error": "Ingresa parámetros válidos."}
    if genero.upper() == "M":
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * edad) + 5
    else:
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * edad) - 161

    factores = {"sedentario": 1.2, "ligero": 1.375, "moderado": 1.55, "intenso": 1.725, "atleta": 1.9}
    f = factores.get(nivel_actividad.lower(), 1.55)
    calorias_totales = tmb * f
    agua_litros = (peso_kg * 0.035) + 0.5
    return {"tmb_watts_calorias": round(tmb, 1), "nivel_actividad": nivel_actividad.capitalize(), "calorias_mantenimiento_diarias": round(calorias_totales, 1), "hidratacion_diaria_recomendada_litros": round(agua_litros, 2)}

# ========================================================================= 
# 3. REGLAMENTOS DEPORTIVOS Y CAPACIDADES FÍSICAS BÁSICAS 
# ========================================================================= 
REGLAMENTO_DEPORTES = { 
    "Vóley": { 
        "jugadores_en_cancha": "6 jugadores por equipo.", 
        "dimensiones_cancha": "18 m x 9 m, dividida por una red a 2.43 m (masculino) / 2.24 m (femenino).", 
        "reglas_principales": [ 
            "Máximo 3 toques por equipo antes de pasar la pelota al campo contrario.", 
            "Rotación obligatoria en sentido de las agujas del reloj al recuperar el saque.", 
            "No se permite agarrar, retener o acompañar el balón (falta de retención).", 
            "Partido al mejor de 5 sets (primeros 4 sets a 25 puntos, 5to set a 15 puntos con diferencia de 2)." 
        ] 
    }, 
    "Básquet": { 
        "jugadores_en_cancha": "5 jugadores por equipo.", 
        "dimensiones_cancha": "28 m x 15 m, aro a 3.05 m de altura.", 
        "reglas_principales": [ 
            "Posesión de ataque limitada a 24 segundos.", 
            "Regla de 8 segundos para pasar la pelota de la cancha trasera a la delantera.", 
            "Valor de enceste: 1 punto (tiro libre), 2 puntos (dentro del área), 3 puntos (fuera del triple).", 
            "Máximo 5 faltas personales por jugador antes de ser descalificado." 
        ] 
    }, 
    "Hándbol": { 
        "jugadores_en_cancha": "7 jugadores por equipo (6 de campo + 1 arquero).", 
        "dimensiones_cancha": "40 m x 20 m, arcos de 3 m x 2 m con área exclusiva de arquero a 6 m.", 
        "reglas_principales": [ 
            "Máximo 3 pasos permitidos con la pelota en la mano sin picar.", 
            "Retención máxima del balón durante 3 segundos sin picar ni pasar.", 
            "No se permite pisar la línea del área de 6 m para realizar un tiro a arco.", 
            "Partido dividido en 2 tiempos de 30 minutos." 
        ] 
    }, 
    "Atletismo & Resistencia": { 
        "jugadores_en_cancha": "Disciplinas individuales y por relevos (4x100m, 4x400m).", 
        "dimensiones_cancha": "Pista sintética ovalada de 400 m de cuerda.", 
        "reglas_principales": [ 
            "Pruebas de Pista: Carreras de velocidad (100m, 200m, 400m), medio fondo y fondo.", 
            "Pruebas de Campo: Saltos (largo, alto, garrocha) y Lanzamientos (bala, disco, jabalina, martillo).", 
            "Salida en falso: Descalificación inmediata en competencias oficiales." 
        ] 
    } 
} 

# ========================================================================= 
# 4. GLOSARIO DE EDUCACIÓN FÍSICA Y SALUD 
# ========================================================================= 
DICCIONARIO_ED_FISICA = { 
    "Acondicionamiento Físico": "Desarrollo planificado de las capacidades físicas básicas (fuerza, resistencia, velocidad, flexibilidad) para mejorar la salud y rendimiento.", 
    "VO2 Máx (Consumo Máximo de Oxígeno)": "Volumen máximo de oxígeno que el organismo puede transportar y consumir por unidad de tiempo durante un esfuerzo intenso.", 
    "Lactato / Ácido Láctico": "Subproducto metabólico generado durante el ejercicio anaeróbico de alta intensidad que contribuye a la fatiga muscular temporal.", 
    "Hipertrofia Muscular": "Aumento del tamaño y volumen de las fibras musculares como respuesta al entrenamiento sistemático de fuerza.", 
    "Flexibilidad": "Capacidad de las articulaciones de realizar movimientos con la máxima amplitud articular sin lesionarse.", 
    "Frecuencia Cardíaca de Reserva": "Diferencia entre la Frecuencia Cardíaca Máxima y la Frecuencia Cardíaca en Reposo, utilizada para dosificar el esfuerzo.", 
    "Ergonomía": "Estudio de las condiciones de adaptación de un lugar de trabajo o estudio a las características físicas del usuario para prevenir lesiones.", 
    "Entrada en Calor / Calentamiento": "Fase inicial preparatoria que eleva la temperatura corporal y ritmo cardíaco para reducir el riesgo de lesiones musculares." 
}