import re 
from typing import Any

# ========================================================================= 
# 1. GLOSARIO DE TÉRMINOS TÉCNICOS EN IT & HARDWARE/SOFTWARE 
# ========================================================================= 

TECHNICAL_GLOSSARY_IT = { 
    "Array": {"translation": "Arreglo / Vector / Matriz", "category": "Programming", "definition": "A data structure containing a collection of elements identified by index or key."}, 
    "Bandwidth": {"translation": "Ancho de banda", "category": "Networking", "definition": "The maximum rate of data transfer across a given path or network in a given time."}, 
    "Compiler": {"translation": "Compilador", "category": "Programming", "definition": "A program that translates code written in a high-level language into machine code."}, 
    "Database": {"translation": "Base de datos", "category": "Data & Storage", "definition": "An organized collection of structured information or data stored electronically."}, 
    "Deploy": {"translation": "Desplegar / Publicar", "category": "DevOps & Web", "definition": "The process of installing, testing, and distributing software to a target environment."}, 
    "Framework": {"translation": "Entorno de trabajo / Marco de desarrollo", "category": "Programming", "definition": "A platform for developing software applications providing a foundation for code structure."}, 
    "Hardware": {"translation": "Componentes físicos / Hardware", "category": "Hardware", "definition": "The physical parts of a computer system such as CPU, RAM, GPU, and motherboard."}, 
    "Library": {"translation": "Biblioteca de código (Librería)", "category": "Programming", "definition": "A collection of non-volatile resources used by computer programs to develop software."}, 
    "Middleware": {"translation": "Capas intermedias / Software de intermediación", "category": "Architecture", "definition": "Software that bridges different applications, tools, and databases across a network."}, 
    "Operating System": {"translation": "Sistema Operativo (SO)", "category": "System", "definition": "System software that manages computer hardware, software resources, and provides common services."}, 
    "Repository": {"translation": "Repositorio", "category": "Version Control", "definition": "A central file storage location for managing and tracking code changes in Git/GitHub."}, 
    "Thread": {"translation": "Hilo de ejecución / Proceso liviano", "category": "Operating Systems", "definition": "The smallest unit of execution within a process managed independently by a scheduler."} 
} 

# ========================================================================= 
# 2. FALSE FRIENDS (FALSOS AMIGOS) EN INGLÉS TÉCNICO DE INFORMÁTICA 
# ========================================================================= 

FALSE_FRIENDS_IT = { 
    "Library": { 
        "false_translation": "Librería (tienda de libros)", 
        "correct_meaning": "Biblioteca de funciones / módulos de código.", 
        "example": "Import the math library to perform calculations." 
        }, 
    "Argument": { 
        "false_translation": "Discusión / Pelea", 
        "correct_meaning": "Argumento / Parámetro pasado a una función.", 
        "example": "Pass the variable as an argument to the function." 
        }, 
    "Directory": { 
        "false_translation": "Directiva / Directivo", 
        "correct_meaning": "Directorio / Carpeta en el sistema de archivos.", 
        "example": "Change to the root directory using the 'cd' command." 
        }, 
    "Exit": { 
        "false_translation": "Éxito", 
        "correct_meaning": "Salida / Salir del programa o consola.", 
        "example": "Type 'exit' to terminate the command terminal." 
    }, 
    "Constipado / Constipated": { 
        "false_translation": "Estar resfriado", 
        "correct_meaning": "Estreñido / Estreñimiento (Para resfriado se usa 'cold').", 
        "example": "I have a cold today (Tengo un resfrío hoy)." }, 
    "Support": { 
        "false_translation": "Soportar (aguantar dolor/molestia)", 
        "correct_meaning": "Soporte técnico / Apoyo / Compatibilidad.", 
        "example": "This operating system supports 64-bit architecture." 
    } 
} 

# ========================================================================= 
# 3. ANALIZADOR DE GRAMÁTICA TÉCNICA Y ESTRUCTURA DE MANUALES / CODE READMES 
# ========================================================================= 
GRAMMAR_PATTERNS = [ 
    {
    "pattern": r"\b(is|are|was|were)\s+([a-z]+ed|[a-z]+en)\b", 
    "rule": "Passive Voice (Voz Pasiva)", 
    "explanation": "Used in technical docs to focus on the action rather than the actor (e.g. 'Data is sent')."
    }, 
    {
    "pattern": r"\b(if|when|unless)\b", 
    "rule": "Conditionals (Condicionales)", 
    "explanation": "Used for logic flows and troubleshooting (e.g. 'If the system crashes, reboot')."
    }, 
    {
    "pattern": r"^\s*(click|run|install|open|select|download|check)\b", 
    "rule": "Imperative Mood (Imperativos)", 
    "explanation": "Used in manuals and CLI guides for step-by-step instructions (e.g. 'Run npm install')."
    }, 
    {
    "pattern": r"\b(must|should|can|may|could)\b", 
    "rule": "Modal Verbs (Verbos Modales)", 
    "explanation": "Express obligation, recommendation or permission (e.g. 'You must specify a password')."
    } 
] 

def analyze_technical_text_english(text: str) -> dict[str, Any]:
    """Anlyzes an English technical document, Readme or error log:
    1. Extracts technical keywords and false friends.
    2. Detects grammar patterns (Passive voice, Imperatives, Conditionals).
    3. Generates a summary and study Q&A.
    """
    
    if not text or len(text.strip()) < 15: 
        return {"error": "Please enter a longer English technical text or manual snippet (at least 15 characters)."} 
        
    words = re.findall(r'\b[A-Za-z]{3,}\b', text) 
    lower_words = [w.lower() for w in words] 
    found_terms = {} 
    
    for term, data in TECHNICAL_GLOSSARY_IT.items(): 
        if term.lower() in lower_words or any(term.lower() in w for w in lower_words): 
            found_terms[term] = data 
            
    found_ff = {}     
    for ff, data in FALSE_FRIENDS_IT.items(): 
        key_term = ff.split("/")[0].strip().lower() 
        if key_term in lower_words: 
            found_ff[ff] = data

    grammar_matches = [] 
    lines = text.split("\n") 
    for line in lines: 
        for p in GRAMMAR_PATTERNS: 
            if re.search(p["pattern"], line, re.IGNORECASE): 
                grammar_matches.append({"rule": p["rule"], "line": line.strip(), "explanation": p["explanation"]}) 
                                
    unique_grammar = [] 
    seen_rules = set() 
    for gm in grammar_matches: 
        if gm["rule"] not in seen_rules: 
            seen_rules.add(gm["rule"]) 
            unique_grammar.append(gm) 
                                        
    qa = [ 
           {"q": "What is the main objective or topic described in this text?", "a": f"The text discusses technical specifications and instructions containing {len(words)} words."}, 
           {"q": "Which key IT terms were identified in the document?", "a": ", ".join(list(found_terms.keys())[:5]) if found_terms else "General IT terminology."} 
        ] 
    
    return { 
        "word_count": len(words), 
        "found_terms": found_terms, 
        "found_false_friends": found_ff, 
        "grammar_insights": unique_grammar, 
        "qa_guide": qa 
    }