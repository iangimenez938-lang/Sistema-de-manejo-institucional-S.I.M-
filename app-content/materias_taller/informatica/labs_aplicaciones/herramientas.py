import sqlite3 

# ========================================================================= 
# 1. MOTOR Y EJECUTOR DE CONSULTAS SQL EN MEMORIA (SQLITE) 
# ========================================================================= 

def ejecutar_consulta_sql_simulada(consulta_sql: str): 
    """Ejecuta sentencias SQL reales en una base de datos SQLite efímera en memoria.""" 
    
    if not consulta_sql or not consulta_sql.strip(): 
        return {"error": "Ingresa una consulta SQL para ejecutar."} 
    
    try: 
        conn = sqlite3.connect(":memory:") 
        cursor = conn.cursor() 
        cursor.execute("CREATE TABLE estudiantes (id INTEGER PRIMARY KEY, nombre TEXT, especialidad TEXT, promedio REAL);") 
        cursor.execute("INSERT INTO estudiantes VALUES (1, 'Lucas Gómez', 'Informática', 8.5);") 
        cursor.execute("INSERT INTO estudiantes VALUES (2, 'Sofia Martínez', 'Informática', 9.2);") 
        cursor.execute("INSERT INTO estudiantes VALUES (3, 'Mateo Fernández', 'Electrónica', 7.8);") 
        cursor.execute("INSERT INTO estudiantes VALUES (4, 'Valentina Rossi', 'Informática', 9.6);") 
        conn.commit() 
        cursor.execute(consulta_sql) 
        
        if consulta_sql.strip().upper().startswith("SELECT"): 
            columnas = [desc[0] for desc in cursor.description] 
            filas = cursor.fetchall() 
            conn.close() 
            return { "tipo_consulta": "SELECT", "columnas": columnas, "filas": filas, "total_registros": len(filas) } 
        else: 
            conn.commit() 
            conn.close() 
            return {"tipo_consulta": "DDL/DML", "mensaje": "Consulta ejecutada correctamente con éxito."} 
        
    except Exception as e: 
        return {"error": f"Error de Sintaxis SQL: {str(e)}"} 
    
# ========================================================================= 
# 2. GENERADOR DE MAQUETAS WEB (HTML5 / CSS3) 
# ========================================================================= 

PLANTILLAS_COMPONENTES_WEB = {
    "Formulario de Login": {
        "html": "<section class=\"login-card\">\n  <h2>Iniciar sesión</h2>\n  <label>Usuario</label>\n  <input type=\"text\" placeholder=\"usuario@escuela.edu\">\n  <label>Contraseña</label>\n  <input type=\"password\" placeholder=\"••••••\">\n  <button>Entrar</button>\n</section>",
        "css": ".login-card {\n  display: flex;\n  flex-direction: column;\n  gap: 12px;\n  max-width: 320px;\n  margin: 24px auto;\n  padding: 20px;\n  border-radius: 12px;\n  background: #ffffff;\n  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);\n}\n\n.login-card input, .login-card button {\n  padding: 10px 12px;\n  border-radius: 8px;\n  border: 1px solid #dfe3e8;\n}\n\n.login-card button {\n  background: #0d6efd;\n  color: white;\n  border: none;\n  cursor: pointer;\n}\n"
    },
    "Tarjeta de Producto": {
        "html": "<article class=\"product-card\">\n  <h3>Notebook Pro</h3>\n  <p>Procesador rápido, pantalla brillante y gran autonomía.</p>\n  <span>$150.00</span>\n</article>",
        "css": ".product-card {\n  border: 1px solid #dfe3e8;\n  border-radius: 12px;\n  padding: 18px;\n  text-align: center;\n  background: #f8fafc;\n}\n\n.product-card span {\n  font-size: 1.2rem;\n  font-weight: bold;\n  color: #0d6efd;\n}\n"
    },
    "Lista de Tareas": {
        "html": "<ul class=\"todo-list\">\n  <li>Revisar diseño</li>\n  <li>Programar lógica</li>\n  <li>Validar accesibilidad</li>\n</ul>",
        "css": ".todo-list {\n  list-style: none;\n  padding: 0;\n  max-width: 320px;\n}\n\n.todo-list li {\n  background: #eef2ff;\n  padding: 10px 12px;\n  margin-bottom: 8px;\n  border-radius: 8px;\n}\n"
    }
}

def obtener_plantilla_componente_web(nombre_componente):
    return PLANTILLAS_COMPONENTES_WEB.get(nombre_componente, {"error": "Componente no encontrado."})


def generar_plantilla_aplicacion(nombre_componente: str):
    """Devuelve un bloque HTML/CSS listo para mostrar en la interfaz del taller."""
    plantilla = obtener_plantilla_componente_web(nombre_componente)
    if "error" in plantilla:
        return plantilla
    return {
        "nombre": nombre_componente,
        "html": plantilla.get("html", ""),
        "css": plantilla.get("css", ""),
        "vista_previa": f"<style>{plantilla.get('css', '')}</style>{plantilla.get('html', '')}",
    }

# ========================================================================= 
# 3. GLOSARIO DE DESARROLLO WEB Y APLICACIONES 
# ========================================================================= 
DICCIONARIO_APLICACIONES = {
    "Base de Datos Relacional (RDBMS)": "Sistema que organiza los datos en tablas estructuradas con filas y columnas interrelacionadas mediante claves (PK/FK).",
    "SQL (Structured Query Language)": "Lenguaje estándar para consultar, insertar, actualizar y gestionar datos en bases de datos relacionales.",
    "Frontend": "Capa de presentación de una aplicación web con la que interactúa el usuario directamente (HTML, CSS, JavaScript).",
    "Backend": "Capa lógica de servidor que procesa las peticiones del frontend, gestiona la autenticación y conecta con las bases de datos.",
    "API (Application Programming Interface)": "Conjunto de definiciones y protocolos que permite que diferentes aplicaciones se comuniquen entre sí.",
    "Validación de Formularios": "Proceso de comprobar que los datos ingresados cumplen reglas de negocio antes de enviarse o almacenarse.",
    "Responsive Design": "Enfoque de diseño que adapta la interfaz a distintos tamaños de pantalla para mantener la usabilidad.",
    "Wireframe": "Esquema visual básico de una interfaz que muestra estructura, contenido y flujo sin detalle visual final.",
    "Query": "Consulta SQL o petición de datos realizada a una base de datos o API para obtener información específica.",
}
