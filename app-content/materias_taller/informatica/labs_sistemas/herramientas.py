# ========================================================================= 
# 1. CALCULADORA DE PERMISOS POSIX / LINUX (CHMOD / CHOWN) 
# ========================================================================= 
def calcular_permisos_posix(octal_str: str = "755"): 
    if len(octal_str) != 3 or not octal_str.isdigit(): 
        return {"error": "Ingresa un número octal de 3 dígitos (ejemplo: 755, 644, 777)."} 
    
    MAPPING = { '0': '---', '1': '--x', '2': '-w-', '3': '-wx', '4': 'r--', '5': 'r-x', '6': 'rw-', '7': 'rwx' } 
    
    u, g, o = octal_str[0], octal_str[1], octal_str[2] 
    sym = f"-{MAPPING[u]}{MAPPING[g]}{MAPPING[o]}" 
    
    def parse_desc(digit, role): 
        val = int(digit) 
        perms = [] 
        if val & 4: perms.append("Lectura (r)") 
        if val & 2: perms.append("Escritura (w)") 
        if val & 1: perms.append("Ejecución (x)") 
        return f"{role}: " + (", ".join(perms) if perms else "Sin permisos (---)") 
    
    return { "octal": octal_str, "notacion_simbolica": sym, "owner": parse_desc(u, "Propietario (Owner)"), "group": parse_desc(g, "Grupo (Group)"), "others": parse_desc(o, "Otros Usuarios (Others)"), "recomendacion_uso": "Permisos restrictivos recomendados para scripts/ejecutables (755)" if octal_str == "755" else "Permiso estándar de lectura/escritura (644)" } 

# ========================================================================= 
# 2. GUÍA INTERACTIVA DE COMANDOS CLI (BASH / LINUX / WINDOWS CMD) 
# ========================================================================= 
COMANDOS_SISTEMA_DICCIONARIO = { "ls -la": {"categoria": "Archivos y Directorios", "efecto": "Lista todos los archivos y carpetas, incluyendo ocultos, con detalles de permisos y tamaño.", "ejemplo": "ls -la /var/log"}, "systemctl status": {"categoria": "Gestión de Servicios", "efecto": "Muestra el estado de un servicio del sistema (activo, detenido, con fallas).", "ejemplo": "systemctl status nginx"}, "ps aux": {"categoria": "Gestión de Procesos", "efecto": "Muestra todos los procesos en ejecución en el sistema con su PID y consumo de memoria/CPU.", "ejemplo": "ps aux | grep python"}, "df -h": {"categoria": "Almacenamiento", "efecto": "Muestra el espacio usado y disponible en los discos montados en formato legible (GB/MB).", "ejemplo": "df -h"}, "ip a / ifconfig": {"categoria": "Redes", "efecto": "Muestra las interfaces de red configuradas y sus direcciones IP asignadas.", "ejemplo": "ip a show eth0"} } 

def consultar_comando_cli(comando_key): 
    return COMANDOS_SISTEMA_DICCIONARIO.get(comando_key, {"error": "Comando no encontrado."}) 

# ========================================================================= 
# 3. DIAGNÓSTICO DE RECURSOS DEL SISTEMA 
# ========================================================================= 
def diagnosticar_recursos_sistema(cpu_percent: float = 50, memoria_percent: float = 60, disco_percent: float = 70, red_estado: str = "normal"):
    """Evalúa el estado general del sistema a partir de métricas simples."""
    if cpu_percent < 0 or memoria_percent < 0 or disco_percent < 0:
        return {"error": "Las métricas de uso no pueden ser negativas."}

    score = (cpu_percent + memoria_percent + disco_percent) / 3.0

    if score < 40:
        estado = "Óptimo"
        recomendacion = "El sistema se encuentra estable y sin presión de recursos."
    elif score < 70:
        estado = "Aceptable"
        recomendacion = "El sistema está funcionando, pero conviene controlar uso de memoria y CPU."
    elif score < 85:
        estado = "Alerta"
        recomendacion = "Se recomienda cerrar procesos pesados y revisar almacenamiento."
    else:
        estado = "Crítico"
        recomendacion = "Se detecta presión alta del sistema; revisar procesos, swaps y espacio libre."

    red = str(red_estado or "normal").strip().lower()
    if red not in {"normal", "lento", "caido"}:
        red = "normal"

    if red == "caido":
        recomendacion += " La red presenta fallas y requiere revisión de drivers o enlace."
    elif red == "lento":
        recomendacion += " La conexión está lenta; revisar ancho de banda y tráfico activo."

    return {
        "cpu_percent": round(cpu_percent, 1),
        "memoria_percent": round(memoria_percent, 1),
        "disco_percent": round(disco_percent, 1),
        "red_estado": red,
        "estado_general": estado,
        "recomendacion": recomendacion,
        "score_promedio": round(score, 1),
    }

# ========================================================================= 
# 4. PLANIFICADOR DE PROCESOS (CPU SCHEDULING SIMULATOR) 
# ========================================================================= 
def simular_planificacion_cpu(procesos_lista, algoritmo="FIFO"): 
    if not procesos_lista: 
        return {"error": "Ingresa una lista de procesos válida."} 
    
    resultado_pasos = [] 
    tiempo_actual = 0 
    tiempos_espera = [] 
    
    for p in procesos_lista: 
        pid = p.get("pid", "P?") 
        rafaga = p.get("rafaga", 5) 
        
        t_espera = tiempo_actual 
        tiempos_espera.append(t_espera) 
        
        resultado_pasos.append({ "pid": pid, "inicio": tiempo_actual, "fin": tiempo_actual + rafaga, "espera": 
        t_espera }) 
        tiempo_actual += rafaga 
        
    promedio_espera = sum(tiempos_espera) / len(tiempos_espera) 
        
    return { "algoritmo": algoritmo, "secuencia_ejecucion": resultado_pasos, "tiempo_total_ms": tiempo_actual, "tiempo_espera_promedio_ms": round(promedio_espera, 2) } 

# ========================================================================= 
# 5. GLOSARIO DE SISTEMAS OPERATIVOS 
# ========================================================================= 
DICCIONARIO_SISTEMAS = { 
    "Kernel (Núcleo)": "Componente central del sistema operativo que gestiona el acceso seguro al hardware, memoria y CPU.", 
    "Proceso": "Programa en ejecución cargado en la memoria RAM con su propio espacio de direcciones y estado.", 
    "Hilo (Thread)": "Unidad mínima de ejecución dentro de un proceso que comparte recursos con otros hilos.", 
    "Sistema de Archivos (ext4 / NTFS)": "Estructura lógica que organiza y administra el almacenamiento de datos en los discos.", 
    "Shell / Bash": "Intérprete de comandos que proporciona una interfaz entre el usuario y el sistema operativo.",
    "Permiso POSIX": "Modelo de permisos basado en lectura, escritura y ejecución para propietario, grupo y otros usuarios.",
    "Planificador de CPU": "Algoritmo del sistema operativo que decide qué proceso ejecuta la CPU y cuándo.",
    "Memoria Virtual": "Espacio de direcciones que simula memoria principal adicional mediante intercambio con almacenamiento secundario.",
    "Servicio del Sistema": "Programa que se ejecuta en segundo plano para ofrecer funciones del sistema operativo o aplicaciones."
}