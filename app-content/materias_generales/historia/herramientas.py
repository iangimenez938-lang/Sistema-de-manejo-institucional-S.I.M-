import json 
import re 

# ========================================================================= 
# 1. GENERADOR Y GESTOR DE LÍNEAS DE TIEMPO (TIMELINE) 
# ========================================================================= 
EVENTOS_HISTORICOS_PREDEFINIDOS = [ 
    {
        "anio": 1789, 
        "evento": "Revolución Francesa", 
        "categoria": "Modernidad y Estado", 
        "descripcion": "Caída de la monarquía absoluta e inicio de la era contemporánea y los derechos del ciudadano."
    }, 
    {
        "anio": 1810, 
        "evento": "Revolución de Mayo (Argentina)", 
        "categoria": "Historia Argentina", 
        "descripcion": "Creación de la Primera Junta de Gobierno e inicio del proceso independentista en el Río de la Plata."
    }, 
    {
        "anio": 1816, 
        "evento": "Declaración de la Independencia Argentina", 
        "categoria": "Historia Argentina", 
        "descripcion": "Congreso de Tucumán proclama la independencia de las Provincias Unidas de Sudamérica."
    }, 
    {
        "anio": 1853, 
        "evento": "Sanción de la Constitución Nacional Argentina", 
        "categoria": "Historia Argentina", 
        "descripcion": "Establecimiento de la República representativa, republicana y federal."
    }, 
    {
        "anio": 1914, 
        "evento": "Inicio de la Primera Guerra Mundial", 
        "categoria": "Siglo XX", 
        "descripcion": "Conflicto bélico global entre la Triple Entente y las Potencias Centrales."
    }, 
    {
        "anio": 1936, 
        "evento": "Máquina Universal de Turing", 
        "categoria": "Historia de la Informática", 
        "descripcion": "Alan Turing formaliza el concepto de algoritmo y computación teórica."
    }, 
    {
        "anio": 1939, 
        "evento": "Inicio de la Segunda Guerra Mundial", 
        "categoria": "Siglo XX", 
        "descripcion": "Estallido del conflicto global entre los Aliados y el Eje."
    }, 
    {
        "anio": 1945, 
        "evento": "Inicio de la Guerra Fría", 
        "categoria": "Guerra Fría y Tecnología", 
        "descripcion": "Enfrentamiento ideológico, político y tecnológico entre EE.UU. (capitalismo) y la URSS (socialismo)."
    }, 
    {
        "anio": 1969, 
        "evento": "Creación de ARPANET (Origen de Internet)", 
        "categoria": "Historia de la Informática", 
        "descripcion": "Primera red interconectada de computadoras desarrollada por el Departamento de Defensa de EE.UU."
    }, 
    {
        "anio": 1976, 
        "evento": "Golpe de Estado en Argentina (Dictadura 1976-1983)", 
        "categoria": "Historia Argentina", 
        "descripcion": "Inicio del gobierno militar de facto y el terrorismo de Estado en la Argentina."
    }, 
    {
        "anio": 1983, 
        "evento": "Retorno a la Democracia en Argentina", 
        "categoria": "Historia Argentina", 
        "descripcion": "Elección presidencial de Raúl Alfonsín y restauración de la institucionalidad democrática."
    }, 
    {
        "anio": 1991, 
        "evento": "World Wide Web (Nacimiento de la Web Pública)", 
        "categoria": "Historia de la Informática", 
        "descripcion": "Tim Berners-Lee abre el sistema hipertexto WWW al público general."
    }, 
] 

def obtener_eventos_ordenados(lista_custom=None): 
    """Devuelve la lista de eventos ordenada cronológicamente.""" 
    eventos = lista_custom if lista_custom is not None else EVENTOS_HISTORICOS_PREDEFINIDOS 
    return sorted(eventos, key=lambda x: x["anio"]) 

def calcular_lapso_temporal(anio_inicio, anio_fin): 
    """Calcula la distancia en años y siglos entre dos momentos históricos.""" 
    diferencia = abs(anio_fin - anio_inicio) 
    siglos = diferencia / 100.0 
    return { "anio_inicio": anio_inicio, "anio_fin": anio_fin, "diferencia_anios": diferencia, "diferencia_siglos": round(siglos, 2) } 

# ========================================================================= 
# 2. CUADROS COMPARATIVOS HISTÓRICO-POLÍTICOS 
# ========================================================================= 
CUADROS_COMPARATIVOS = { 
    "Unitarios vs Federales (Argentina S. XIX)": { 
        "ejes": ["Proyecto Político", "Modelo Económico", "Base Social / Regional", "Líderes Emblemáticos"], 
        "A": { 
            "nombre": "Unitarios", 
            "detalles": [ "Gobierno centralizado con sede en Buenos Aires.", "Libre comercio, control exclusivo de la Aduana e inversión extranjera.", "Intelectuales, comerciantes del puerto y elites urbanas de Buenos Aires.", "Bernardino Rivadavia, General Paz, Salvador María del Carril." ] }, 
        "B": { 
            "nombre": "Federales", 
            "detalles": [ "Autonomía provincial y confederación de provincias soberanas.", "Proteccionismo para economías regionales y reparto de rentas aduaneras.", "Sectores rurales, gauchos, hacendados y provincias del Litoral e Interior.", "Juan Manuel de Rosas, Facundo Quiroga, Justo José de Urquiza, Gervasio Artigas." ] 
            } 
        }, 
    "Primera vs Segunda Revolución Industrial": { 
        "ejes": ["Época / Siglo", "Fuentes de Energía", "Industrias Clave", "Tecnología de Transporte / Com."], 
        "A": { 
            "nombre": "Primera Revolución Industrial (S. XVIII)", 
            "detalles": [ "Segunda mitad del Siglo XVIII (Gran Bretaña).", "Carbón mineral y vapor de agua (Máquina de vapor).", "Textil y Siderurgia pesada (hierro).", "Ferrocarril a vapor y barco de vapor." ] 
            }, 
        "B": { 
            "nombre": "Segunda Revolución Industrial (S. XIX-XX)", 
            "detalles": [ "Fines del Siglo XIX a principios del XX (EE.UU., Alemania).", "Petróleo y Electricidad.", "Química, Automotriz, Acero y Telecomunicaciones.", "Automóvil, aviación, telégrafo, teléfono y radio." ] 
            } 
        }, 
    "Guerra Fría: Capitalismo vs Socialismo": { 
        "ejes": ["Líder del Bloque", "Sistema Económico", "Organización Política", "Alianza Militar"], 
        "A": { 
            "nombre": "Bloque Occidental (Capitalista)", 
            "detalles": [ "Estados Unidos (EE.UU.).", "Economía de libre mercado y propiedad privada.", "Democracia liberal parlamentaria o presidencialista.", "OTAN (Organización del Tratado del Atlántico Norte)." ] 
            }, 
        "B": { 
            "nombre": "Bloque Oriental (Socialista)", 
            "detalles": [ "Unión Soviética (URSS).", "Economía planificada centralizada y colectivización de medios de producción.", "Unipartidismo comunista (Estado socialista).", "Pacto de Varsovia." ] 
            } 
        } 
    } 

# ========================================================================= 
# 3. ANALIZADOR DE TEXTOS HISTÓRICOS Y FUENTES PRIMARIAS/SECUNDARIAS 
# ========================================================================= 
PALABRAS_CLAVE_HISTORIA = [ 
    "revolución", "estado", "soberanía", "constitución", "democracia", "dictadura", 
    "guerra", "independencia", "unitarios", "federales", "memoria", "derechos", 
    "territorio", "sociedad", "tecnología", "política", "imperio", "colonia", 
    "liberalismo", "socialismo", "totalitarismo", "ciudadanía", "sindicato", "pueblo" 
] 

def analizar_texto_historico(texto: str): 
    """Analiza una fuente histórica: extrae palabras clave, resume el contenido y genera una guía de preguntas."""
    if not texto or not texto.strip():
        return {"error": "Ingresa un texto o documento histórico para analizar."}

    texto_limpio = texto.strip()
    if len(texto_limpio) < 20:
        return {"error": "Ingresa un texto o documento histórico más extenso para analizar (mínimo 20 caracteres)."}

    oraciones = [o.strip() for o in re.split(r'[.!?]+', texto_limpio) if o.strip()]
    palabras = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b', texto_limpio.lower())
    claves = sorted({p for p in palabras if p in PALABRAS_CLAVE_HISTORIA})

    if not claves:
        claves = sorted(set(palabras[:8]))

    resumen = " ".join([o + "." for o in oraciones[:3]]) if oraciones else "No se pudo extraer un resumen del texto."
    preguntas_respuestas = []
    if oraciones:
        preguntas_respuestas.append({
            "pregunta": "¿Qué hecho o planteo inicial expone el texto histórico?",
            "respuesta": oraciones[0] + "."
        })
        if len(oraciones) > 1:
            preguntas_respuestas.append({
                "pregunta": "¿Qué antecedentes o contexto complementario se describen?",
                "respuesta": oraciones[1] + "."
            })
        if claves:
            preguntas_respuestas.append({
                "pregunta": "¿Cuáles son los conceptos políticos o históricos más relevantes detectados?",
                "respuesta": f"Conceptos identificados: {', '.join(claves[:6])}."
            })
        if len(oraciones) > 2:
            preguntas_respuestas.append({
                "pregunta": "¿Qué desenlace o conclusión sostiene la fuente?",
                "respuesta": oraciones[-1] + "."
            })

    return {
        "num_palabras": len(palabras),
        "num_oraciones": len(oraciones),
        "palabras_clave": claves,
        "resumen_analitico": resumen,
        "guia_preguntas_respuestas": preguntas_respuestas,
    }

# ========================================================================= 
# 4. GLOSARIO DE CONCEPTOS POLÍTICOS E HISTÓRICOS 
# ========================================================================= 
DICCIONARIO_HISTORIA = { 
    "Soberanía": "Poder supremo e independiente que reside en el pueblo y se ejerce a través de las instituciones del Estado.", 
    "Federalismo": "Sistema político en el cual el poder se distribuye y comparte entre un gobierno central y estados o provincias autónomas.", 
    "Unitarismo": "Sistema de gobierno centralizado donde el poder político y administrativo emana de una única sede nacional.", 
    "Memoria Colectiva": "Conjunto de recuerdos, relatos y valores compartidos por una comunidad o nación para interpretar su pasado y construir su identidad.", 
    "Terrorismo de Estado": "Uso ilegítimo, clandestino y sistemático de la fuerza, la violencia y la represión por parte de las estructuras gubernamentales de facto contra la población.", 
    "Guerra Fría": "Periodo de enfrentamiento global directo, idológico, militar y tecnológico entre los bloques encabezados por EE.UU. y la URSS (1945-1991).", 
    "Totalitarismo": "Régimen político en el que el Estado ejerce un control absoluto sobre la sociedad, la economía y la vida privada, suprimiendo las libertades individuales.", 
    "Democracia": "Forma de organización social y política basada en la división de poderes, el respeto a los derechos humanos y la elección periódica de representantes por voto popular.", 
    "Posverdad": "Distorsión deliberada de la realidad en el discurso público para modelar la opinión social manipulando emociones y creencias en entornos digitales.", 
    "Revolución Digital": "Transición histórica de la tecnología analógica y mecánica a la tecnología digital, caracterizada por la informática, la automatización e internet." 
}