import re 
import ast 
# ========================================================================= 
# 1. INTÉRPRETE DE PSEUDOCÓDIGO PASO A PASO CON SEGUIMIENTO DE VARIABLES 
# ========================================================================= 
def interpretar_pseudocodigo(codigo_str: str, entradas_usuario: dict[str, object] | None = None):
    """ Ejecuta pseudocódigo en español (estilo PSeInt / Algorítmico) Genera una traza de ejecución paso a paso con tabla de variables y consola. """
    if not codigo_str or len(codigo_str.strip()) == 0:
        return {"error": "Ingresa código o pseudocódigo para ejecutar."}

    entradas: dict[str, object] = entradas_usuario or {}
    lineas = [linea.strip() for linea in codigo_str.split("\n")]
    variables: dict[str, object] = {}
    consola: list[str] = []
    pasos_traza: list[dict[str, object]] = []
    max_instrucciones = 200
    contador_instrucciones = 0

    def evaluar_expresion(expr_str: str, env_vars: dict[str, object]):
        expr = expr_str.strip()
        expr = re.sub(r'\bY\b', ' and ', expr, flags=re.IGNORECASE)
        expr = re.sub(r'\bO\b', ' or ', expr, flags=re.IGNORECASE)
        expr = re.sub(r'\bNO\b', ' not ', expr, flags=re.IGNORECASE)
        if "==" not in expr and "=" in expr and not ("<=" in expr or ">=" in expr or "!=" in expr):
            expr = expr.replace("<-", "=").replace("=", "==")
        expr = expr.replace("<-", "==")

        try:
            return eval(expr, {"__builtins__": {}}, env_vars)
        except Exception:
            for var_k, var_v in env_vars.items():
                if isinstance(var_v, str):
                    expr = re.sub(rf'\b{var_k}\b', f'"{var_v}"', expr)
                else:
                    expr = re.sub(rf'\b{var_k}\b', str(var_v), expr)

            try:
                return eval(expr, {"__builtins__": {}}, {})
            except Exception:
                return expr

    idx = 0
    n_lineas = len(lineas)
    while idx < n_lineas and contador_instrucciones < max_instrucciones:
        linea = lineas[idx].strip()
        if not linea or linea.startswith("//") or linea.startswith("#"):
            idx += 1
            continue

        contador_instrucciones += 1
        linea_upper = linea.upper()

        if linea_upper.startswith(("ESCRIBIR", "MOSTRAR", "IMPRIMIR")):
            partes = linea.split(" ", 1)
            if len(partes) > 1:
                contenido = partes[1].strip()
                if (contenido.startswith('"') and contenido.endswith('"')) or (contenido.startswith("'") and contenido.endswith("'")):
                    msg = contenido[1:-1]
                elif contenido in variables:
                    msg = str(variables[contenido])
                else:
                    try:
                        msg = str(evaluar_expresion(contenido, variables))
                    except Exception:
                        msg = contenido
                consola.append(msg)
                pasos_traza.append({
                    "linea_num": idx + 1,
                    "instruccion": linea,
                    "accion": f"Salida por Consola: '{msg}'",
                    "variables": dict(variables),
                })

        elif linea_upper.startswith(("LEER", "INGRESAR")):
            partes = linea.split(" ", 1)
            if len(partes) > 1:
                var_nombre = partes[1].strip()
                val_ingresado = entradas.get(var_nombre, 10)
                variables[var_nombre] = val_ingresado
                pasos_traza.append({
                    "linea_num": idx + 1,
                    "instruccion": linea,
                    "accion": f"Lectura de Variable '{var_nombre}' = {val_ingresado}",
                    "variables": dict(variables),
                })

        elif linea_upper.startswith("SI "):
            cond_str = linea[3:].replace("ENTONCES", "").strip()
            res_cond = bool(evaluar_expresion(cond_str, variables)) if variables else True
            pasos_traza.append({
                "linea_num": idx + 1,
                "instruccion": linea,
                "accion": f"Evaluación Condicional 'SI ({cond_str})' -> {res_cond}",
                "variables": dict(variables),
            })

        elif "<-" in linea or "=" in linea:
            sep = "<-" if "<-" in linea else "="
            partes = linea.split(sep, 1)
            var_nom = partes[0].strip()
            expr_val = partes[1].strip()
            try:
                val_res = evaluar_expresion(expr_val, variables)
            except Exception:
                val_res = expr_val.strip('"\'')
            variables[var_nom] = val_res
            pasos_traza.append({
                "linea_num": idx + 1,
                "instruccion": linea,
                "accion": f"Asignación: {var_nom} = {val_res}",
                "variables": dict(variables),
            })

        idx += 1

    return {
        "num_instrucciones": contador_instrucciones,
        "variables_finales": variables,
        "consola_salida": consola,
        "traza_paso_a_paso": pasos_traza,
    }

# ========================================================================= 
# 2. GENERADOR DE DIAGRAMA DE FLUJO DE DATOS (NODOS Y FIGURAS) 
# ========================================================================= 
def generar_diagrama_flujo(codigo_str: str): 
    """ Analiza un algoritmo o pseudocódigo y construye una estructura de nodos de diagrama de flujo (Inicio, Proceso, Decisión, Entrada/Salida, Fin). """ 
    lineas = [l.strip() for l in codigo_str.split("\n") if l.strip() and not l.strip().startswith("//")] 
    nodos = [] 
    
    # Nodo Inicial 
    nodos.append({"id": 1, "tipo": "inicio_fin", "texto": "INICIO", "color": "#28a745", "icono": "🏁"}) 
    node_id = 2 
    for l in lineas: 
        l_upper = l.upper() 
        if l_upper.startswith(("INICIO", "ALGORITMO", "PROCESO")): 
            continue 
        elif l_upper.startswith(("FIN", "FINALGORITMO", "FINPROCESO")): 
            continue 
        elif l_upper.startswith(("ESCRIBIR", "MOSTRAR", "IMPRIMIR", "LEER", "INGRESAR")): 
            nodos.append({"id": node_id, "tipo": "entrada_salida", "texto": l, "color": "#007acc", "icono": "📤" if "ESCRIBIR" in l_upper or "MOSTRAR" in l_upper else "📥"}) 
        elif l_upper.startswith("SI "): 
            nodos.append({"id": node_id, "tipo": "decision", "texto": f"¿{l.replace('SI', '').replace('ENTONCES', '').strip()}?", "color": "#ff922b", "icono": "❓"}) 
        elif l_upper.startswith(("MIENTRAS", "PARA")): 
            nodos.append({"id": node_id, "tipo": "bucle", "texto": l, "color": "#845ef7", "icono": "🔄"}) 
        else: 
            nodos.append({"id": node_id, "tipo": "proceso", "texto": l, "color": "#20c997", "icono": "⚙️"}) 
        node_id += 1 
        
    # Nodo Final 
    nodos.append({"id": node_id, "tipo": "inicio_fin", "texto": "FIN", "color": "#dc3545", "icono": "🛑"}) 
    return { "total_nodos": len(nodos), "diagrama_nodos": nodos } 

# ========================================================================= 
# 3. EVALUADOR DE TABLAS DE VERDAD Y LÓGICA BOOLEANA 
# ========================================================================= 
def generar_tabla_verdad(expresion_booleana: str): 
    """ Genera la tabla de verdad completa para expresiones lógicas con variables A, B (y C si aplica). Soporta AND, OR, NOT, XOR. """ 
    expr = expresion_booleana.upper().replace("Y", "and").replace("O", "or").replace("NO", "not").replace("XOR", "^") 
    vars_posibles = ["A", "B", "C"] 
    vars_usadas = [v for v in vars_posibles if v in expresion_booleana.upper()] 
    if not vars_usadas: 
        vars_usadas = ["A", "B"] 
    
    n_vars = len(vars_usadas) 
    filas = [] 
    for i in range(2 ** n_vars): 
        vals = {} 
        for j, v in enumerate(vars_usadas): 
            vals[v] = bool((i >> (n_vars - 1 - j)) & 1) 
        
        eval_expr = expr 
        for v in vars_usadas: 
            eval_expr = re.sub(rf'\b{v}\b', str(vals[v]), eval_expr) 
        
        try: 
            res = bool(eval(eval_expr, {"__builtins__": {}}, {})) 
        except Exception: 
            res = False 
            
        row_dict = {v: "V" if vals[v] else "F" for v in vars_usadas} 
        row_dict["RESULTADO"] = "VERDADERO (V)" if res else "FALSO (F)" 
        filas.append(row_dict) 
    
    return { "expresion": expresion_booleana, "variables": vars_usadas, "filas_tabla": filas } 

# ========================================================================= 
# 4. GLOSARIO DE PROGRAMACIÓN Y ESTRUCTURAS DE DATOS 
# ========================================================================= 
DICCIONARIO_PROGRAMACION = { 
    "Algoritmo": "Secuencia finita, ordenada e inequívoca de instrucciones para resolver un problema o ejecutar una tarea.", 
    "Pseudocódigo": "Lenguaje de especificación de algoritmos que combina palabras en lenguaje natural con estructuras de programación.", 
    "Variable": "Espacio de memoria reservado para almacenar un valor que puede cambiar durante la ejecución del programa.", 
    "Constante": "Valor que se mantiene inalterable a lo largo de toda la ejecución del algoritmo.", 
    "Estructura de Control": "Instrucción que dirige el flujo de ejecución de un programa (condicionales Si/Sino, bucles Mientras/Para).", 
    "Diagrama de Flujo": "Representación gráfica de un algoritmo mediante figuras geométricas estandarizadas (óvalos, rectángulos, rombos).", 
    "Bucle / Iteración": "Estructura que repite un bloque de código mientras se cumpla una condición determinada.", 
    "Función / Subrutina": "Bloque de código reutilizable diseñado para realizar una tarea específica y retornar opcionalmente un resultado.", 
    "Tabla de Verdad": "Tabla matemática utilizada en lógica proposicional para mostrar el valor de verdad de una expresión compuesta.", 
    "Compilador vs Intérprete": "El compilador traduce todo el código fuente a código máquina antes de ejecutar; el intérprete traduce y ejecuta línea por línea." 
}