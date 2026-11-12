import math 
import hashlib 

# ========================================================================= 
# 1. CÁLCULO DE REDES, DIRECCIONAMIENTO IP Y SUBREDES (IPv4) 
# ========================================================================= 
def analizar_red_ip(ip_str: str, cidr: int = 24): 
    """ Calcula dirección de red, broadcast, rango de IPs útiles y total de hosts para una dirección IPv4 dada con su máscara CIDR (ej: /24, /16, /8). """ 
    try: 
        octetos = [int(o) for o in ip_str.strip().split(".")] 
        if len(octetos) != 4 or any(o < 0 or o > 255 for o in octetos): 
            return {"error": "Ingresa una dirección IPv4 válida (ejemplo: 192.168.1.50)."} 
        
        if cidr < 8 or cidr > 30: 
            return {"error": "La máscara CIDR debe estar entre /8 y /30."} 
    
    except Exception: 
        return {"error": "Formato de dirección IP inválido."} 
    
    mask_int = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF 
    ip_int = (octetos[0] << 24) | (octetos[1] << 16) | (octetos[2] << 8) | octetos[3] 
    net_int = ip_int & mask_int 
    bcast_int = net_int | (~mask_int & 0xFFFFFFFF) 
        
    def int_to_ip(val): 
        return f"{(val >> 24) & 0xFF}.{(val >> 16) & 0xFF}.{(val >> 8) & 0xFF}.{val & 0xFF}" 
        
    total_hosts = (2 ** (32 - cidr)) - 2 
    f_ip_int = net_int + 1 
    l_ip_int = bcast_int - 1 

    clase_ip = "A" if octetos[0] < 128 else ("B" if octetos[0] < 192 else ("C" if octetos[0] < 224 else "D/E")) 
    tipo_ip = "Privada" if ( 
        octetos[0] == 10 
        or (octetos[0] == 172 and 16 <= octetos[1] <= 31) 
        or (octetos[0] == 192 and octetos[1] == 168) 
    ) else "Pública" 

    return { "ip_ingresada": ip_str, "cidr": f"/{cidr}", "mascara_subred": int_to_ip(mask_int), "direccion_red": int_to_ip(net_int), "direccion_broadcast": int_to_ip(bcast_int), "primera_ip_util": int_to_ip(f_ip_int), "ultima_ip_util": int_to_ip(l_ip_int), "total_hosts_utiles": total_hosts, "clase_ip": clase_ip, "tipo_ip": tipo_ip } 

# ========================================================================= 
# 2. CIBERSEGURIDAD, CIFRADO Y GENERACIÓN DE HASH 
# ========================================================================= 
def generar_hashes_seguridad(texto: str): 
    """Genera huellas digitales (Hashes) MD5, SHA-1 y SHA-256 para demostración de integridad.""" 
    if not texto: 
        return {"error": "Ingresa un texto o mensaje para calcular su hash."} 
    
    b_text = texto.encode('utf-8') 
    
    return { "texto_original": texto, "md5": hashlib.md5(b_text).hexdigest(), "sha1": hashlib.sha1(b_text).hexdigest(), "sha256": hashlib.sha256(b_text).hexdigest() } 

def cifrado_cesar_simulado(texto: str, desplazamiento: int = 3, modo="cifrar"): 
    """Simula cifrado y descifrado por sustitución alfabética (César).""" 
    
    resultado = "" 
    shift = desplazamiento if modo == "cifrar" else -desplazamiento 
    for char in texto: 
        if char.isalpha(): 
            ascii_offset = 65 if char.isupper() else 97 
            resultado += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset) 
        else: 
            resultado += char 
            
    return { "modo": modo.upper(), "desplazamiento": desplazamiento, "resultado": resultado } 

# ========================================================================= 
# 3. DIRECTORIO DE PROTOCOLOS, PUERTOS Y SERVICIOS WEB 
# ========================================================================= 
PUERTOS_Y_SERVICIOS_TIC = { 
    80: {"protocolo": "HTTP", "servicio": "Navegación Web Estándar", "seguro": False, "descripcion": "Protocolo de transferencia de hipertexto sin cifrar."}, 
    443: {"protocolo": "HTTPS", "servicio": "Navegación Web Segura (SSL/TLS)", "seguro": True, "descripcion": "Transmisión web cifrada para banca, correo y credenciales."}, 
    21: {"protocolo": "FTP", "servicio": "Transferencia de Archivos", "seguro": False, "descripcion": "Envío y descarga de archivos en servidores de almacenamiento."}, 
    22: {"protocolo": "SSH", "servicio": "Consola Remota Segura", "seguro": True, "descripcion": "Acceso por línea de comandos cifrada a servidores Linux/Unix."}, 
    25: {"protocolo": "SMTP", "servicio": "Envío de Correo Electrónico", "seguro": False, "descripcion": "Protocolo de transporte de correo entre servidores e-mail."}, 
    53: {"protocolo": "DNS", "servicio": "Resolución de Nombres de Dominio", "seguro": True, "descripcion": "Traduce nombres web (ej: google.com) a direcciones IP numéricas."}, 
    110: {"protocolo": "POP3", "servicio": "Recepción de Correo Electrónico", "seguro": False, "descripcion": "Descarga mensajes de correo desde el servidor al cliente local."}, 143: {"protocolo": "IMAP", "servicio": "Sincronización de Correo Electrónico", "seguro": True, "descripcion": "Mantiene el correo sincronizado entre múltiples dispositivos."}, 
    3306: {"protocolo": "MySQL", "servicio": "Base de Datos Relacional", "seguro": True, "descripcion": "Puerto por defecto para conexiones a motores de bases de datos MySQL/MariaDB."}, 
} 

# ========================================================================= 
# 4. GLOSARIO Y CONCEPTOS CLAVE DE TIC 
# ========================================================================= 
DICCIONARIO_TIC = { 
    "Modelo OSI": "Modelo de referencia conceptual de 7 capas que estandariza la comunicación en redes informáticas.", 
    "TCP/IP": "Conjunto de protocolos de red que impulsan internet, organizados en 4 capas.", 
    "Cloud Computing": "Modelo de prestación de servicios tecnológicos (servidores, almacenamiento, software) a través de internet.", 
    "Firewall (Cortafuegos)": "Sistema de seguridad que monitorea y filtra el tráfico de red entrante y saliente según reglas establecidas.", 
    "Ancho de Banda": "Cantidad máxima de datos transmitidos a través de una conexión de red en un periodo determinado.", 
    "VPN (Virtual Private Network)": "Red privada virtual que cifra la conexión a internet para garantizar privacidad.", 
    "Ciberseguridad": "Práctica de proteger sistemas, redes y programas digitales contra ataques o accesos no autorizados.", 
    "Phishing": "Técnica de ingeniería social para engañar a usuarios y obtener contraseñas o datos bancarios." 
}
