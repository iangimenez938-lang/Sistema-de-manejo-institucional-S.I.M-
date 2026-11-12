import math 
import re 

# ========================================================================= 
# 1. HERRAMIENTAS DE CÁLCULO FINANCIERO Y MICROECONOMÍA 
# ========================================================================= 
def calcular_punto_equilibrio(costos_fijos, precio_unitario, costo_variable_unitario, unidades_estimadas=0): 
    """ Calcula el punto de equilibrio en unidades e ingresos, y estima utilidades según un volumen de producción/ventas. """ 
    margen_contribucion = precio_unitario - costo_variable_unitario 
    
    if margen_contribucion <= 0: 
        return { "error": "El precio unitario debe ser mayor al costo variable unitario para tener margen de contribución positivo." } 
    
    pe_unidades = costos_fijos / margen_contribucion 
    pe_ingresos = pe_unidades * precio_unitario 
    ratio_margen = (margen_contribucion / precio_unitario) * 100 
    res = { "punto_equilibrio_unidades": math.ceil(pe_unidades), "punto_equilibrio_exacto": round(pe_unidades, 2), "ingreso_equilibrio": round(pe_ingresos, 2), "margen_contribucion_unitario": round(margen_contribucion, 2), "ratio_margen_contribucion": round(ratio_margen, 2) } 
    
    if unidades_estimadas > 0: 
        ingresos_est = unidades_estimadas * precio_unitario 
        costos_totales_est = costos_fijos + (unidades_estimadas * costo_variable_unitario) 
        utilidad = ingresos_est - costos_totales_est 
        res.update({ "unidades_estimadas": unidades_estimadas, "ingreso_estimado": round(ingresos_est, 2), "costo_total_estimado": round(costos_totales_est, 2), "utilidad_estimada": round(utilidad, 2), "estado_proyecto": "Ganancia" if utilidad > 0 else ("Pérdida" if utilidad < 0 else "Equilibrio exacto") }) 
    return res 

def simular_mercado_oferta_demanda(a_dem, b_dem, a_ofe, b_ofe, precio_evaluado=None): 
    """ Modela ecuaciones de mercado: Demanda: Qd = a_dem - b_dem * P Oferta: Qo = a_ofe + b_ofe * P """ 
    
    if (b_dem + b_ofe) <= 0: 
        return {"error": "Los coeficientes de sensibilidad al precio deben ser mayores a 0."} 
    
    p_eq = (a_dem - a_ofe) / (b_dem + b_ofe) 
    if p_eq <= 0: 
        return {"error": "Las ecuaciones ingresadas no producen un precio de equilibrio positivo."} 
    
    q_eq = a_dem - (b_dem * p_eq) 
    
    res = { "precio_equilibrio": round(p_eq, 2), "cantidad_equilibrio": round(q_eq, 2) } 
    
    if precio_evaluado is not None: 
        qd = a_dem - (b_dem * precio_evaluado) 
        qo = a_ofe + (b_ofe * precio_evaluado) 
        qd = max(0, qd) 
        qo = max(0, qo) 
        diferencia = qo - qd 
        
        if diferencia > 0: 
            situacion = f"Exceso de Oferta (Superávit de {round(diferencia, 2)} unidades)" 
        elif diferencia < 0: 
            situacion = f"Exceso de Demanda (Escasez de {round(abs(diferencia), 2)} unidades)" 
        else: 
            situacion = "Mercado en Equilibrio Exacto" 
            
        res.update({ "precio_evaluado": precio_evaluado, "demanda_actual": round(qd, 2), "oferta_actual": round(qo, 2), "situacion_mercado": situacion }) 
    return res 

def calcular_elasticidad_precio(q1, q2, p1, p2): 
    """Calcula la elasticidad precio de la demanda por método del punto medio o arco.""" 
    
    if p1 == p2 or (p1 + p2) == 0: 
        return {"error": "Los precios no pueden ser idénticos ni sumar cero."} 
        
    if (q1 + q2) == 0: 
        return {"error": "Las cantidades no pueden sumar cero."} 
    
    delta_q = (q2 - q1) / ((q1 + q2) / 2) 
    delta_p = (p2 - p1) / ((p1 + p2) / 2) 
    ep = delta_q / delta_p 
    ep_abs = abs(ep) 
    
    if ep_abs > 1: 
        tipo = "Elástica (Muy sensible a cambios de precio)" 
    elif ep_abs < 1: 
        tipo = "Inelástica (Poco sensible a cambios de precio)" 
    else: 
        tipo = "Elasticidad Unitaria" 
        
    return { 
        "elasticidad": round(ep, 4), 
        "valor_absoluto": round(ep_abs, 4), 
        "tipo_elasticidad": tipo, 
        "var_porcentual_q": round(delta_q * 100, 2), 
        "var_porcentual_p": round(delta_p * 100, 2) 
    } 
    
def evaluar_viabilidad_van(inversion_inicial, flujos_caja, tasa_descuento_pct): 
    """Calcula el Valor Actual Neto (VAN) y tiempo de recuperación (Payback).""" 
    
    r = tasa_descuento_pct / 100.0 
    van = -inversion_inicial 
    flujos_descontados = [] 
    acumulado = -inversion_inicial 
    periodo_recuperacion = None 
    
    for i, flujo in enumerate(flujos_caja, start=1): 
        f_desc = flujo / ((1 + r) ** i) 
        flujos_descontados.append(round(f_desc, 2)) 
        van += f_desc 
        acumulado_anterior = acumulado 
        acumulado += flujo 
        if acumulado >= 0 and periodo_recuperacion is None: 
            if flujo != 0: 
                fraccion = abs(acumulado_anterior) / flujo 
                periodo_recuperacion = round((i - 1) + fraccion, 1) 
            else: 
                periodo_recuperacion = i 
                
    es_viable = van > 0
                
    return { 
        "inversion_inicial": inversion_inicial, 
        "tasa_descuento_pct": tasa_descuento_pct, 
        "van": round(van, 2), 
        "es_viable": es_viable, 
        "flujos_descontados": flujos_descontados, 
        "periodo_recuperacion_periodos": periodo_recuperacion if periodo_recuperacion else "Más de los períodos evaluados", 
        "dictamen": "PROYECTO VIABLE (VAN > 0)" if es_viable else "PROYECTO NO VIABLE / RIESGOSO (VAN ≤ 0)" 
    } 

# ========================================================================= 
# 2. ANALIZADOR DE TEXTOS ECONÓMICOS Y EXTRACTOR DE TEMAS/RESPUESTAS 
# ========================================================================= 
PALABRAS_CLAVE_ECONOMIA = [ "inflación", "costos", "oferta", "demanda", "mercado", "precio", "equilibrio", "pyme", "empresa", "inversión", "capital", "recursos", "escasez", "trabajo", "empleo", "salario", "impuesto", "subsidio", "exportación", "importación", "moneda", "banco", "interés", "tecnología", "digital", "productividad", "utilidad", "ganancia", "pérdida", "monopolio", "competencia", "pbi", "crecimiento", "desarrollo", "sostenible", "rse", "presupuesto", "financiamiento" ] 

def analizar_texto_economico(texto: str): 
    """ Analiza un texto o noticia económica ingresada por el estudiante: 1. Extrae oraciones principales y genera un resumen estructurado. 2. Identifica conceptos y palabras clave encontradas. 3. Genera una guía de preguntas y respuestas de comprensión lectora sobre el texto. """ 
    
    if not texto or len(texto.strip()) < 20: 
        return {"error": "Ingresa un texto o artículo económico más extenso para analizar (mínimo 20 caracteres)."} 
    
    oraciones = [o.strip() for o in re.split(r'[.!?]+', texto) if len(o.strip()) > 15] 
    palabras = re.findall(r'\b[a-zA-AáéíóúÁÉÍÓÚñÑ]{4,}\b', texto.lower()) 
    
    claves_encontradas = sorted(list(set([p for p in palabras if p in PALABRAS_CLAVE_ECONOMIA]))) 
    if not claves_encontradas: 
        claves_encontradas = sorted(list(set(palabras[:8]))) 
        
    resumen_oraciones = oraciones[:4] if len(oraciones) >= 4 else oraciones 
    preguntas_respuestas = [] 
    if len(oraciones) > 0: 
        preguntas_respuestas.append({ "pregunta": "¿Cuál es la idea central expuesta en el inicio del texto?", "respuesta": oraciones[0] + "." }) 
        
    if len(oraciones) > 1: 
        preguntas_respuestas.append({ "pregunta": "¿Qué aspecto o contexto complementario se desarrolla en el párrafo?", "respuesta": oraciones[1] + "." }) 
    
    if len(claves_encontradas) > 0: 
        preguntas_respuestas.append({ "pregunta": f"¿Qué conceptos económicos clave destacan en este análisis?", "respuesta": f"Se destacan términos fundamentales como: {', '.join(claves_encontradas[:6])}." }) 
    
    if len(oraciones) > 2: 
        preguntas_respuestas.append({ "pregunta": "¿A qué conclusión o implicancia económica arriba el documento?", "respuesta": oraciones[-1] + "." }) 
        
    return { "num_palabras": len(palabras), "num_oraciones": len(oraciones), "palabras_clave": claves_encontradas, "resumen_ejecutivo": " ".join([o + "." for o in resumen_oraciones]), "guia_preguntas_respuestas": preguntas_respuestas } 

# ========================================================================= 
# 3. BASE DE DATOS DE ESCUELAS DE PENSAMIENTO ECONÓMICO Y PENSADORES 
# ========================================================================= 
CATALOGO_ESCUELAS_ECONOMICAS = { 
    "Mercantilismo (S. XVI - XVIII)": { 
        "epoca": "Siglos XVI a XVIII (Europa Renacentista y Colonial)", 
        "pensadores": ["Jean-Baptiste Colbert", "Thomas Mun"], 
        "ideas_clave": [ 
            "Riqueza basada en la acumulación de metales preciosos (oro y plata).", 
            "Fuerte intervención del Estado en la economía y proteccionismo comercial.", 
            "Balanza comercial superavitaria: exportar más de lo que se importa." 
        ], 
        "contexto": "Surgió con la formación de los Estados-Nación europeos y la expansión del comercio colonial." 
    }, 
    "Fisiocracia (S. XVIII)": { 
        "epoca": "Siglo XVIII (Francia Ilustrada)", 
        "pensadores": ["François Quesnay", "Anne Robert Jacques Turgot"], 
        "ideas_clave": [ 
            "La agricultura es la única actividad verdaderamente generadora de riqueza (producto neto).", 
            "Existencia de un 'orden natural' en el funcionamiento económico.", 
            "Surgimiento de la famosa frase 'Laissez faire, laissez passer' (Dejar hacer, dejar pasar)." 
        ], 
        "contexto": "Reacción frente al control mercantilista en la Francia previa a la Revolución Francesa." 
    }, 
    "Escuela Clásica (S. XVIII - XIX)": { 
        "epoca": "Fines del Siglo XVIII y Siglo XIX (Revolución Industrial)", 
        "pensadores": ["Adam Smith", "David Ricardo", "Thomas Malthus", "John Stuart Mill"], 
        "ideas_clave": [ 
            "La 'Mano Invisible': El libre mercado autoregula la oferta, demanda y precios.", 
            "Teoría del Valor-Trabajo: El valor de las mercancías depende del trabajo necesario para producirlas.", 
            "Ventajas Comparativas (David Ricardo) para el libre comercio internacional.", 
            "Defensa de la libertad individual y propiedad privada (Liberalismo Económico)." 
        ], 
        "contexto": "Nació junto con la Primera Revolución Industrial británica y la consolidación del capitalismo." 
    }, 
    "Escuela Marxista (S. XIX)": { 
        "epoca": "Mid-Siglo XIX en adelante", 
        "pensadores": ["Karl Marx", "Friedrich Engels"], 
        "ideas_clave": [ 
            "Crítica al sistema capitalista y al concepto de plusvalía (apropiación del trabajo no pagado).", 
            "Lucha de clases entre la burguesía (dueña de los medios de producción) y el proletariado.", 
            "Propuesta de un sistema socialista con planificación estatal y abolición de la propiedad privada de medios de producción." 
        ], 
        "contexto": "Surgió en respuesta a la explotación laboral y desigualdades de la Revolución Industrial." 
    }, 
    "Escuela Neoclásica (Fines S. XIX)": { 
        "epoca": "Fines del Siglo XIX - Principios del XX", 
        "pensadores": ["Alfred Marshall", "Léon Walras", "William Stanley Jevons", "Vilfredo Pareto"], 
        "ideas_clave": [ 
            "Introducción del Análisis Marginal (Utilidad Marginal Decreciente).", 
            "Teoría del Equilibrio General y Microeconomía moderna.", 
            "El valor de los bienes está dado por su utilidad marginal y escasez, no por el costo de producción." 
        ], 
        "contexto": "Formalización matemática de la ciencia económica y nacimiento del análisis de mercado moderno." 
    }, 
    "Keynesianismo (S. XX)": { 
        "epoca": "Década de 1930 (Gran Depresión) en adelante", 
        "pensadores": ["John Maynard Keynes"], 
        "ideas_clave": [ 
            "La demanda agregada es el motor principal de la economía.", 
            "El libre mercado no garantiza el pleno empleo de forma automática.", 
            "Justificación del gasto público y políticas fiscales expansivas del Estado para combatir crisis y desempleo." 
        ],
        "contexto": "Desarrollada tras el colapso bursátil de 1929 y la crisis económica mundial." 
    }, 
    "Monetarismo / Escuela de Chicago (S. XX)": { 
        "epoca": "Años 1960 - 1980", 
        "pensadores": ["Milton Friedman", "Anna Schwartz"], 
        "ideas_clave": [ 
            "La inflación es siempre un fenómeno monetario causado por la emisión excesiva de dinero.", 
            "Prioridad del control de la masa monetaria y la estabilidad de precios.", 
            "Reducción del tamaño del Estado y regulación de mercados." 
        ], 
        "contexto": "Surgió frente a la estagflación de la década de 1970." 
    }, 
    "Economía Digital & Neoinstitucionalismo (S. XXI)": { 
        "epoca": "Época Contemporánea (Era de la Información)", 
        "pensadores": ["Douglass North", "Paul Romer", "Erik Brynjolfsson"], 
        "ideas_clave": [ 
            "El conocimiento, la tecnología y el software como motores de crecimiento ilimitado.", 
            "Importancia de las instituciones, propiedad intelectual y seguridad jurídica.", 
            "Efectos de red, economía colaborativa y transformación digital de Pymes." 
        ], 
    "contexto": "Revolución de las TIC, internet, inteligencia artificial y comercio electrónico global." 
    } 
} 

# ========================================================================= 
# 4. GLOSARIO ECONÓMICO INTEGRADO 
# ========================================================================= 
DICCIONARIO_ECONOMICO = { 
    "Punto de Equilibrio": "Nivel de ventas o producción en el cual los ingresos totales igualan a los costos totales, resultando en beneficio nulo (utilidad = 0).", 
    "Costos Fijos": "Gastos que no varían con el nivel de producción de la empresa (ej: alquiler, licencias de software, sueldos administrativos).", 
    "Costos Variables": "Gastos que cambian en proporción directa al volumen de producción o venta (ej: insumos, servidores por tráfico, comisiones).", 
    "Elasticidad Precio": "Medida de la sensibilidad de la cantidad demandada de un bien frente a variaciones en su precio.", 
    "Ley de Oferta y Demanda": "Principio económico que establece que el precio de un bien se determina por la interacción entre la cantidad que los productores ofrecen y la que los consumidores demandan.", 
    "Valor Actual Neto (VAN)": "Indicador financiero que mide el valor presente de los flujos de caja futuros generados por un proyecto, descontados a una tasa de interés dada.", 
    "Microeconomía": "Rama de la economía que estudia el comportamiento de los agentes individuales (consumidores, familias y empresas) y sus interacciones en mercados específicos.", 
    "Macroeconomía": "Rama de la economía que analiza los fenómenos agregados a nivel nacional o global (inflación, desempleo, PBI, políticas monetarias).", 
    "Economía Digital": "Sector de la economía que abarca los bienes, servicios y procesos comerciales basados en tecnologías digitales e internet.", 
    "Responsabilidad Social Empresarial (RSE)": "Compromiso de las empresas de actuar de manera ética y contribuir al desarrollo económico sostenible, respetando a la comunidad y al medio ambiente." 
}