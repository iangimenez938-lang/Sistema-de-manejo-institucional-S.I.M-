import re 

# ========================================================================= 
# 1. ANALIZADOR SINTÁCTICO Y MORFOSINTÁCTICO DE ORACIONES 
# ========================================================================= 
CLASES_PALABRAS = { "sustantivo": ["casa", "perro", "tecnología", "estudiante", "profesor", "escuela", "sistema", "código", "materia", "lengua", "historia", "libro", "computadora", "software", "desarrollo", "proyecto", "sociedad"], "adjetivo": ["grande", "pequeño", "digital", "técnico", "interactivo", "modular", "eficiente", "rápido", "nuevo", "antiguo", "importante", "complejo", "claro", "estructurado"], "verbo": ["analiza", "escribe", "desarrolla", "estudia", "lee", "comprende", "ejecuta", "programa", "calcula", "diseña", "crea", "aprende", "explica", "conecta", "funciona", "es", "son", "fue", "fueron", "tiene", "tienen"], "adverbio": ["rápidamente", "bien", "mal", "siempre", "nunca", "hoy", "ayer", "mañana", "aquí", "allí", "muy", "más", "menos", "eficientemente"], "preposicion": ["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según", "sin", "so", "sobre", "tras", "versus", "vía"], "conjuncion": ["y", "e", "ni", "que", "o", "u", "pero", "mas", "sino", "sin embargo", "por lo tanto", "porque", "pues", "aunque"] } 

def analizar_sintaxis_oracion(oracion: str) -> dict[str, object]: 
    """Realiza un análisis morfosintáctico básico de una oración."""

    oracion_clean = oracion.strip().rstrip(".")
    if not oracion_clean or len(oracion_clean) < 3:
        return {"error": "Ingresa una oración válida de al menos 3 caracteres."}

    palabras = re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b", oracion_clean)
    palabras_lower = [p.lower() for p in palabras]
    verbos_encontrados: list[tuple[str, int]] = []

    for idx, p in enumerate(palabras_lower):
        if p in CLASES_PALABRAS["verbo"] or p.endswith(("ar", "er", "ir", "ó", "aron", "ieron", "ará", "arán", "ía", "ían")):
            verbos_encontrados.append((palabras[idx], idx))

    if not verbos_encontrados and any(w in ["llueve", "nieva", "hay", "hace"] for w in palabras_lower):
        tipo_oracion = "Oración Unimembre (sin sujeto/predicado verbal)"
        sujeto = "N/A"
        predicado = "N/A"
    elif verbos_encontrados:
        tipo_oracion = "Oración Bimembre (Sujeto + Predicado)"
        v_idx = verbos_encontrados[0][1]
        sujeto = " ".join(palabras[:v_idx]) if v_idx > 0 else "[Sujeto Tácito / Expreso al final]"
        predicado = " ".join(palabras[v_idx:])
    else:
        tipo_oracion = "Oración Unimembre / Frase Nominal"
        sujeto = " ".join(palabras)
        predicado = "Sin verbo explícito"

    clasificacion_palabras: list[dict[str, str]] = []
    for p in palabras:
        p_low = p.lower()
        clase = "Otro / Sustantivo común"
        for cat, lista in CLASES_PALABRAS.items():
            if p_low in lista:
                clase = cat.capitalize()
                break
            if cat == "adverbio" and p_low.endswith("mente"):
                clase = "Adverbio"
                break

        clasificacion_palabras.append({"palabra": p, "clase": clase})

    return {
        "oracion_original": oracion,
        "num_palabras": len(palabras),
        "tipo_oracion": tipo_oracion,
        "verbos_nucleo": [v[0] for v in verbos_encontrados],
        "sujeto_estimado": sujeto,
        "predicado_estimado": predicado,
        "analisis_morfológico": clasificacion_palabras,
    }
    
# ========================================================================= 
# 2. ANALIZADOR DE TIPOLOGÍA TEXTUAL, CONECTORES Y REDACCIÓN TÉCNICA 
# ========================================================================= 
CONECTORES_LOGICOS = { "Causales": ["porque", "ya que", "puesto que", "debido a", "dado que"], "Consecutivos": ["por lo tanto", "en consecuencia", "por consiguiente", "así que", "de modo que"], "Adversativos / Concesivos": ["pero", "sin embargo", "no obstante", "aunque", "por el contrario", "a pesar de"], "Aditivos": ["además", "asimismo", "por otra parte", "también", "incluso"], "Organizadores": ["en primer lugar", "por un lado", "por último", "en conclusión", "en resumen"] } 

def analizar_tipologia_y_conectores(texto: str) -> dict[str, object]: 
    """Analiza la estructura del texto, conectores lógicos y su tipología."""
    if not texto or len(texto.strip()) < 20:
        return {"error": "Ingresa un texto de al menos 20 caracteres."}

    oraciones = [o.strip() for o in re.split(r"[.!?]+", texto) if len(o.strip()) > 10]
    palabras = re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b", texto.lower())
    conectores_detectados: dict[str, list[str]] = {}
    texto_low = texto.lower()

    for cat, lista in CONECTORES_LOGICOS.items():
        encontrados = [c for c in lista if c in texto_low]
        if encontrados:
            conectores_detectados[cat] = encontrados

    if any(p in texto_low for p in ["opino", "considero", "en mi opinión", "por lo tanto", "se debe", "argumento"]):
        tipologia = "Texto Argumentativo (Ensayístico / Opinión)"
    elif any(p in texto_low for p in ["informa", "exposición", "concepto", "se define", "consiste en"]):
        tipologia = "Texto Expositivo / Explicativo"
    elif any(p in texto_low for p in ["había una vez", "entonces", "luego", "dijo", "caminó", "de repente"]):
        tipologia = "Texto Narrativo (Cuento / Novela / Relato)"
    elif any(p in texto_low for p in ["código", "sistema", "paso 1", "instrucciones", "especificación", "manual"]):
        tipologia = "Texto Técnico / Instructivo"
    else:
        tipologia = "Texto Expositivo General"

    return {
        "num_palabras": len(palabras),
        "num_oraciones": len(oraciones),
        "tipologia_estimada": tipologia,
        "conectores_encontrados": conectores_detectados,
        "resumen_oraciones": oraciones[:3],
    }

# ========================================================================= 
# 3. BASE DE DATOS DE MOVIMIENTOS LITERARIOS Y GÉNEROS 
# ========================================================================= 
MOVIMIENTOS_LITERARIOS = { "Gauchesca / Literatura Argentina S. XIX": { "epoca": "Siglo XIX en Argentina", "obras_clave": ["El Gaucho Martín Fierro (José Hernández)", "El Matadero (Esteban Echeverría)", "Fausto (Estanislao del Campo)"], "caracteristicas": [ "Uso del lenguaje popular rural del gaucho y la pampa argentina.", "Denuncia social frente a la marginalidad del gaucho y las levas militares.", "Tensión entre 'Civilización y Barbarie' en la construcción nacional." ] }, "Realismo y Naturalismo (S. XIX)": { "epoca": "Segunda mitad del Siglo XIX", "obras_clave": ["Madame Bovary (Gustave Flaubert)", "Crimen y Castigo (Dostoievski)", "Las de Barranco (Gregorio de Laferrère)"], "caracteristicas": [ "Observación objetiva de la realidad social y descripción detallada.", "Crítica a la burguesía y tratamiento de problemáticas cotidianas.", "Determinismo social y psicológico de los personajes." ] }, "Modernismo (Fines S. XIX - XX)": { "epoca": "Fines del Siglo XIX a principios del XX (Hispanoamérica)", "obras_clave": ["Azul... (Rubén Darío)", "Versos Sencillos (José Martí)"], "caracteristicas": [ "Búsqueda de la belleza formal, musicalidad y refinamiento estético.", "Renovación del vocabulario poético y libertad métrica.", "Exotismo y evasión de la realidad mediocre." ] }, "Vanguardias y Realismo Mágico / Boom Latinoamericano": { "epoca": "Siglo XX (Años 1920 - 1970)", "obras_clave": ["Ficciones (Jorge Luis Borges)", "Cien Años de Soledad (García Márquez)", "Rayuela (Julio Cortázar)", "Pedro Páramo (Juan Rulfo)"], "caracteristicas": [ "Ruptura con las estructuras narrativas tradicionales (saltos temporales, laberintos).", "Integración de lo fantástico y maravilloso dentro de la cotidianidad realista.", "Juego con el lenguaje y participación activa del lector." ] } } 

# ========================================================================= 
# 4. GLOSARIO DE TÉRMINOS LITERARIOS Y GRAMATICALES 
# ========================================================================= 
DICCIONARIO_LENGUA = { "Coherencia": "Propiedad textual por la cual un texto se percibe como una unidad con sentido global y tema definido.", "Cohesión": "Red de relaciones gramaticales y léxicas entre las oraciones de un texto (uso de conectores, pronombres y sinónimos).", "Sintaxis": "Parte de la gramática que estudia las reglas para combinar las palabras y formar oraciones con sentido.", "Metáfora": "Figura retórica que consiste en identificar un término real con uno imaginario entre los cuales existe una relación de semejanza.", "Narrador Omnisciente": "Voz narrativa en tercera persona que conoce todos los pensamientos, sentimientos y hechos pasados o futuros de los personajes.", "Texto Expositivo": "Formato textual cuyo propósito principal es informar y explicar conceptos o fenómenos de manera objetiva y clara.", "Ensayo": "Género literario y académico en el que el autor analiza, interpreta o evalúa un tema de forma reflexiva y argumentativa." }