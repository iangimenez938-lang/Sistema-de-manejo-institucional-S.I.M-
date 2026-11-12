import math 

# ========================================================================= 
# 1. ANÁLISIS DE SISTEMAS Y PROCESOS TECNOLÓGICOS 
# ========================================================================= 
def analizar_sistema_tecnologico(nombre_sistema: str, entrada_materia: str, entrada_energia: str, entrada_informacion: str, proceso_transformacion: str): 
    """ Modela un sistema tecnológico según el enfoque sistémico: Entradas (Materia, Energía, Información) -> Proceso -> Salidas + Realimentación. """ 
    if not nombre_sistema: 
        return {"error": "Ingresa el nombre del sistema tecnológico a analizar."} 
    
    salida_materia = f"Producto transformado / Residuos de {entrada_materia or 'insumos'}" 
    salida_energia = f"Energía útil + Disipación térmica de {entrada_energia or 'energía'}" 
    salida_informacion = f"Datos de estado / Resultados de {entrada_informacion or 'señales de entrada'}" 
    realimentacion = f"Sensores y controles ajustan {proceso_transformacion or 'el proceso'} en función de la calidad y rendimiento de la salida." 
    return { "sistema": nombre_sistema, "entradas": { "materia": entrada_materia or "Insumos / Materiales primarios", "energia": entrada_energia or "Energía eléctrica / mecánica", "informacion": entrada_informacion or "Órdenes de control / Datos" }, "proceso": proceso_transformacion or "Transformación automatizada / Procesamiento", "salidas": { "materia": salida_materia, "energia": salida_energia, "informacion": salida_informacion }, "realimentacion_feedback": realimentacion } 

# ========================================================================= 
# 2. PROYECTO TECNOLÓGICO Y PLANIFICACIÓN DE ETAPAS 
# ========================================================================= 
ETAPAS_PROYECTO_TECNOLOGICO = [ { "etapa": "1. Identificación de la Necesidad / Problema", "descripcion": "Definición clara del problema a resolver, usuario destinatario y restricciones técnicas/económicas.", "entregable": "Documento de Especificación de Requerimientos" }, { "etapa": "2. Diseño de la Solución (Boceto / Plano / Diagrama)", "descripcion": "Investigación de antecedentes, alternativas de diseño, diagramas de flujo y selección de materiales/componentes.", "entregable": "Planos técnicos, diagramas de bloque y prototipo conceptual" }, { "etapa": "3. Organización y Gestión (Planificación)", "descripcion": "Asignación de tareas, cronograma (Gantt), presupuesto de costos y distribución del equipo de trabajo.", "entregable": "Planilla de costos y cronograma de ejecución" }, { "etapa": "4. Ejecución y Construcción / Programación", "descripcion": "Fabricación del prototipo, ensamblaje de hardware, codificación de software e integración de partes.", "entregable": "Prototipo funcional" }, { "etapa": "5. Evaluación, Pruebas y Perfeccionamiento", "descripcion": "Ensayo de funcionamiento, pruebas con usuarios, detección de fallos y optimización continua.", "entregable": "Informe técnico final y manual de usuario" } ] 

def calcular_presupuesto_proyecto_tec(items_materiales: list, horas_trabajo: float, costo_hora: float): 
    """ Calcula el costo total de un proyecto tecnológico: Costos de Insumos/Componentes + Costos de Mano de Obra/Desarrollo + Margen de Contingencia (10%). """ 
    total_materiales = sum(item.get("costo", 0) for item in items_materiales) 
    total_mano_obra = horas_trabajo * costo_hora 
    subtotal = total_materiales + total_mano_obra 
    contingencia = subtotal * 0.10 
    total_general = subtotal + contingencia 
    return { "costo_materiales_componentes": round(total_materiales, 2), "costo_mano_obra_desarrollo": round(total_mano_obra, 2), "subtotal": round(subtotal, 2), "contingencia_10pct": round(contingencia, 2), "costo_total_proyecto": round(total_general, 2), "items_desglosados": items_materiales } 
    
# ========================================================================= 
# 3. MATRIZ DE EVALUACIÓN DE IMPACTO Y SUSTENTABILIDAD AMBIENTAL 
# ========================================================================= 
MATRIZ_IMPACTO_TECNOLOGICO = { "Obsolescencia Programada vs Percibida": { "definicion": "Planificación deliberada del fin de vida útil de un producto (hardware/dispositivos) o inducción psicológica al recambio constante.", "impacto_ambiental": "Generación masiva de chatarra electrónica (e-waste) y agotamiento de minerales raros.", "alternativa_sostenible": "Diseño modular, derecho a la reparación (Right to Repair) y economía circular." }, "Huella de Carbono Digital & Centros de Datos": { "definicion": "Consumo masivo de energía eléctrica y agua requeridos para enfriar servidores de IA, minería y servicios cloud 24/7.", "impacto_ambiental": "Emisiones indirectas de CO2 si la matriz energética depende de combustibles fósiles.", "alternativa_sostenible": "Uso de energías renovables (solar/eólica) y servidores de alta eficiencia (PUE low)." }, "Economía Circular en Tecnología": { "definicion": "Modelo de producción y consumo que implica reutilizar, reparar, renovar y reciclar materiales tecnológicos existentes.", "impacto_ambiental": "Reducción dramática del uso de materias primas vírgenes y disposición de residuos tóxicos.", "alternativa_sostenible": "Recuperación de cobre, oro y litio de placas madre y baterías en desuso." } } 

# ========================================================================= 
# 4. GLOSARIO DE INNOVACIÓN Y TECNOLOGÍAS EMERGENTES 
# ========================================================================= 
DICCIONARIO_TECNOLOGIA = { "Enfoque Sistémico": "Método de análisis que estudia los objetos y procesos como conjuntos de partes interconectadas (sistemas) que interactúan entre sí.", "Prototipo": "Primer modelo o versión preliminar de un producto o sistema tecnológico utilizado para probar su viabilidad y diseño.", "Biotecnología": "Técnica que utiliza organismos vivos o sus componentes para crear o modificar productos y procesos para usos específicos.", "Internet de las Cosas (IoT)": "Red de objetos físicos ('cosas') equipados con sensores, software y tecnologías para conectar e intercambiar datos con otros dispositivos.", "Industria 4.0": "Cuarta revolución industrial basada en la integración de sistemas ciberfísicos, computación en la nube e inteligencia artificial.", "Manual de Usuario": "Documentación técnica destinada a brindar asistencia a las personas que utilizan un sistema o producto tecnológico." }