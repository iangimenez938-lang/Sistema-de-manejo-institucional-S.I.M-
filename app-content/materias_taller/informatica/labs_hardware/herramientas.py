# ========================================================================= 
# 1. DIAGNÓSTICO Y TROUBLESHOOTING DE HARDWARE (FALLAS &amp; SÍNTOMAS) 
# ========================================================================= 
MATRIZ_FALLAS_HARDWARE = { 
    "Pitidos al Encender (Beep Codes)": { 
        "sintoma": "El equipo emite un patrón de pitidos al presionar el botón de encendido y no muestra imagen.", 
        "causas_probables": [ 
            "Memoria RAM mal colocada, sucia o defectuosa (1 pitido largo repetido o 3 pitidos cortos).", 
            "Falla en la tarjeta gráfica/video (1 largo y 2 o 3 cortos).", 
            "Falla de procesador CPU o socket dañados.", 
            "Pila CMOS desgastada o configuración corrupta de BIOS." 
        ], 
        "solucion_paso_a_paso": [ 
            "1. Apagar el equipo y desconectar la fuente de alimentación.", 
            "2. Retirar los módulos de memoria RAM y limpiar los contactos dorados con una goma de borrar suave.", 
            "3. Probar encender el equipo instalando un solo módulo de RAM a la vez en diferentes zócalos (DIMM).", 
            "4. Verificar la correcta inserción de la placa de video dedicada y conectores PCIe.", 
            "5. Realizar un 'Clear CMOS' quitando la pila CR2032 durante 5 minutos para restaurar valores de fábrica." 
        ] 
    }, 
    "Sobrecalentamiento / Apagado Repentino": { "sintoma": "La PC se apaga automáticamente a los pocos minutos de juego o procesamiento intenso.", "causas_probables": [ "Pasta térmica seca o mal aplicada en el disipador del procesador (CPU).", "Coolers o ventiladores obstruidos por polvo o averiados.", "Flujo de aire deficiente dentro del gabinete (chasis)." ], "solucion_paso_a_paso": [ "1. Verificar la temperatura de la CPU desde la BIOS o software de monitoreo (normal: 35-50°C idle, <85°C carga).", "2. Limpiar el polvo acumulado en disipadores y ventiladores con aire comprimido o pincel antiestático.", "3. Desmontar el cooler, limpiar la pasta térmica vieja con alcohol isopropílico y aplicar una gota nueva.", "4. Comprobar que los coolers estén girando a las RPM adecuadas." ] }, 
    "Pantallazos Azules (BSOD) / Congelamientos": { "sintoma": "Aparece una pantalla azul con código de error (MEMORY_MANAGEMENT, WHEA_UNCORRECTABLE_ERROR) y se reinicia.", "causas_probables": [ "Sectores defectuosos en la memoria RAM.", "Inestabilidad o degradación en la Fuente de Alimentación (PSU).", "Drivers incompatibles o sobrecalentamiento de GPU/CPU." ], "solucion_paso_a_paso": [ "1. Anotar el código de error stop que muestra Windows.", "2. Ejecutar la herramienta 'Diagnóstico de Memoria de Windows' o MemTest86 desde un pendrive booteable.", "3. Verificar los voltajes de la fuente (+12V, +5V, +3.3V) desde el setup de la BIOS.", "4. Actualizar o desinstalar controladores de video utilizando DDU (Display Driver Uninstaller)." ] }, 
    "Disco No Detectado / Error de Booteo": { "sintoma": "Muestra el mensaje 'Reboot and Select proper Boot device' o el disco SSD/HDD no figura en la BIOS.", "causas_probables": [ "Cable de datos SATA o cable de energía desconectado/defectuoso.", "Falla lógica en la tabla de particiones (MBR/GPT) o falla física en el controlador del disco.", "Configuración de modo SATA incorrecta (AHCI vs IDE / UEFI vs Legacy)." ], "solucion_paso_a_paso": [ "1. Revisar las conexiones físicas SATA y conectores de alimentación M.2/SATA.", "2. Entrar a la BIOS/UEFI y verificar si la unidad aparece identificada con su modelo y capacidad.", "3. Comprobar que el modo de booteo (UEFI o CSM/Legacy) coincida con la instalación del sistema operativo.", "4. Comprobar el estado de salud del disco utilizando datos S.M.A.R.T." ] } } 

def diagnosticar_falla_hardware(nombre_falla: str): 
    data = MATRIZ_FALLAS_HARDWARE.get(nombre_falla) 
    
    if not data: 
        return {"error": "Falla de hardware no encontrada en el catálogo."} 
    
    return data 

# ========================================================================= 
# 2. CALCULADORA DE CONSUMO Y ESTIMACIÓN DE FUENTE DE ALIMENTACIÓN (PSU) 
# ========================================================================= 
def calcular_consumo_psu(cpu_watts, gpu_watts, ram_modulos=2, ssd_nvme_count=1, hdd_sata_count=1, coolers_count=3): 
    ram_w = ram_modulos * 4 
    nvme_w = ssd_nvme_count * 7 
    hdd_w = hdd_sata_count * 10 
    coolers_w = coolers_count * 3 
    motherboard_w = 40 
    consumo_base = cpu_watts + gpu_watts + ram_w + nvme_w + hdd_w + coolers_w + motherboard_w 
    margen_seguridad_watts = consumo_base * 1.30 
    psu_estandar = [450, 500, 550, 600, 650, 750, 850, 1000] 
    psu_recomendada = next((p for p in psu_estandar if p >= margen_seguridad_watts), 1000) 
    
    return { 
        "consumo_estimado_watts": round(consumo_base, 1), 
        "consumo_con_margen_30pct": round(margen_seguridad_watts, 1), 
        "psu_recomendada_watts": psu_recomendada, 
        "desglose": { "CPU / Procesador": f"{cpu_watts} W", "GPU / Placa de Video": f"{gpu_watts} W", "Memoria RAM": f"{ram_w} W ({ram_modulos} módulos)", "Almacenamiento NVMe/HDD": f"{nvme_w + hdd_w} W", "Ventiladores &amp; Placa Madre": f"{coolers_w + motherboard_w} W" }, 
        "certificacion_sugerida": "80 Plus Bronze / Gold (Garantiza eficiencia > 85%)" 
    } 

# ========================================================================= 
# 3. VERIFICADOR DE COMPATIBILIDAD DE COMPONENTES 
# ========================================================================= 
COMPATIBILIDAD_SOCKETS = { 
    "AM4": {
        "marca": "AMD", 
        "ram": "DDR4", 
        "cpus": ["Ryzen 1000", "Ryzen 2000", "Ryzen 3000", "Ryzen 5000"]
    }, 
    "AM5": {
        "marca": "AMD", 
        "ram": "DDR5", 
        "cpus": ["Ryzen 7000", "Ryzen 8000", "Ryzen 9000"]
    }, 
    "LGA 1200": {
        "marca": "Intel", 
        "ram": "DDR4", 
        "cpus": ["Intel 10ma Gen", "Intel 11va Gen"]
    }, 
    "LGA 1700": {
        "marca": "Intel", 
        "ram": "DDR4 / DDR5", 
        "cpus": ["Intel 12da Gen", "Intel 13ra Gen", "Intel 14ta Gen"]
    } 
} 

def verificar_compatibilidad_ensamble(socket_mobo, tipo_ram_mobo): 
    info_socket = COMPATIBILIDAD_SOCKETS.get(socket_mobo) 
    
    if not info_socket: 
        return {"error": "Socket no reconocido en la base de datos."} 
    
    es_compatible_ram = tipo_ram_mobo.upper() in info_socket["ram"].upper() 
    return { 
        "socket": socket_mobo, 
        "marca": info_socket["marca"], 
        "cpus_soportadas": info_socket["cpus"], 
        "ram_requerida": info_socket["ram"], 
        "ram_ingresada": tipo_ram_mobo, 
        "es_compatible": es_compatible_ram, 
        "dictamen": "COMPATIBLE: Los componentes pueden ensamblarse correctamente." if es_compatible_ram else f"INCOMPATIBLE: El socket {socket_mobo} requiere memoria {info_socket['ram']}." 
    } 

# ========================================================================= 
# 4. GLOSARIO DE ARQUITECTURA DE COMPUTADORAS 
# ========================================================================= 
DICCIONARIO_HARDWARE = { 
    "CPU (Unidad Central de Procesamiento)": "El cerebro de la computadora, encargado de ejecutar las instrucciones de los programas a través de ciclos de reloj (GHz).", 
    "GPU (Unidad de Procesamiento Gráfico)": "Procesador especializado en el cálculo masivo en paralelo de gráficos, renderizado 3D e inteligencia artificial.", 
    "Memoria RAM": "Memoria de acceso aleatorio volátil y de alta velocidad utilizada por el sistema para almacenar temporalmente los programas en ejecución.", 
    "Placa Madre (Motherboard)": "Circuito impreso principal que interconecta la CPU, RAM, almacenamiento, tarjeta gráfica y periféricos.", 
    "BIOS / UEFI": "Firmware grabado en un chip de la motherboard que inicializa el hardware (POST) y carga el sistema operativo.", 
    "NVMe (Non-Volatile Memory Express)": "Protocolo de comunicación diseñado para unidades SSD M.2 conectadas directamente al bus PCIe de ultra alta velocidad.", 
    "POST (Power-On Self-Test)": "Prueba de diagnóstico inicial que realiza la BIOS al encender el equipo para verificar el funcionamiento básico de la CPU, RAM y video.", 
    "Bus de Datos": "Conjunto de líneas eléctricas que transfieren información entre los diferentes componentes internos de la computadora." 
}