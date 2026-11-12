import sys
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

HAS_TKINTER: bool = False
tk: Any = None
ttk: Any = None
messagebox: Any = None

if TYPE_CHECKING:
    import tkinter as tk
    from tkinter import ttk, messagebox
    HAS_TKINTER = True
else:
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        HAS_TKINTER = True
    except (ImportError, Exception):
        HAS_TKINTER = False
        tk = cast(Any, None)
        ttk = cast(Any, None)
        messagebox = cast(Any, None)

try:
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales
    from .docentes_manager import DocentesManager as _DocentesManager
except ImportError:
    def cargar_configuracion() -> dict[str, Any]:
        return {}

    def aplicar_estilos_globales(root: Any, config: dict[str, Any]) -> None:
        return None

    class FallbackDocentesManager:
        def obtener_docente_materia(self, c, a, e, m):
            return {
                "nombre": "Docente a designar",
                "cursos": f"{a}º Año {e}",
                "telefono": "+54 3777 0000-0000",
                "email": "consultas@escuelatecnica.edu.ar",
                "horarios_tabla": [],
            }

        def asignar_docente(self, c, a, e, m, d):
            return True

    DocentesManager = FallbackDocentesManager
else:
    DocentesManager = _DocentesManager

BaseFrame = tk.Frame if HAS_TKINTER else object


class VistaDocentePage(BaseFrame):
    """ Pantalla interactiva completa de Ficha de Docente: - Visualización y edición emergente de datos de contacto (Nombre, Cursos, Teléfono, Mail) - Formulario dinámico para agregar, editar y eliminar filas en la Tabla de Horarios - Persistencia automática de cambios en JSON a través de DocentesManager """ 
    def __init__(self, parent=None, contexto: dict | None = None, on_back_callback=None): 
        if not HAS_TKINTER:
            return
        self.config = cargar_configuracion() or {}
        self.bg_main = self.config.get("bg_color", "#ffffff")
        self.fg_main = self.config.get("fg_color", "#212529") 
        self.panel_bg = self.config.get("panel_bg", "#f8f9fa") 
        self.accent = self.config.get("accent_color", "#007acc") 
        self.font_family = self.config.get("font_family", "Arial") 
        self.font_size = self.config.get("font_size", 10) 
        super().__init__(parent, bg=self.panel_bg, padx=20, pady=16) 
        self.pack(fill="both", expand=True) 
        self.contexto = contexto or {} 
        self.on_back = on_back_callback 
        self.manager = DocentesManager() 
        aplicar_estilos_globales(self, self.config)
        self._build_ui() 
        
    def _obtener_contexto_curso(self): 
        ciclo_raw = self.contexto.get("ciclo") 
        ciclo = str(ciclo_raw or "Ciclo Básico") 
        anio_raw = self.contexto.get("anio") 
        
        try: 
            anio = int(anio_raw) if anio_raw is not None else 1 
        except (TypeError, ValueError): 
            anio = 1 
            
        esp_div_raw = self.contexto.get("division") if ciclo == "Ciclo Básico" else self.contexto.get("especialidad") 
        esp_div = str(esp_div_raw or "A") 
        materia = str(self.contexto.get("materia") or "Materia") 
    
        return ciclo, anio, esp_div, materia 
    
    def _build_ui(self): 
        # Limpiar interfaz anterior 
        for child in self.winfo_children(): 
            child.destroy() 
            
        ciclo, anio, esp_div, materia = self._obtener_contexto_curso() 
        doc = self.manager.obtener_docente_materia(ciclo, anio, esp_div, materia) 
        base_font = (self.font_family, self.font_size) 
        title_font = (self.font_family, max(12, self.font_size + 3), "bold") 
        subtitle_font = (self.font_family, max(10, self.font_size + 1), "bold") 
        
        # 📜 Scrollable Canvas principal 
        scroll_canvas = tk.Canvas(self, bg=self.panel_bg, highlightthickness=0, bd=0) 
        scroll_canvas.pack(side="left", fill="both", expand=True) 
        
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=scroll_canvas.yview) 
        v_scrollbar.pack(side="right", fill="y") 
        scroll_canvas.configure(yscrollcommand=v_scrollbar.set) 
        content = tk.Frame(scroll_canvas, bg=self.panel_bg, padx=10, pady=10) 
        canvas_window = scroll_canvas.create_window((0, 0), window=content, anchor="nw") 
        
        def _update_scrollregion(event=None): 
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")) 
            
        def _resize_content(event=None): 
            width = getattr(event, "width", scroll_canvas.winfo_width()) 
            
            scroll_canvas.itemconfigure(canvas_window, width=max(420, width)) 
        
        content.bind("<Configure>", _update_scrollregion)
        scroll_canvas.bind("<Configure>", _resize_content)

        # ⬅️ Botón Volver 
        if self.on_back: 
            btn_volver = tk.Button( content, text="⬅️ Volver a la Vista del Curso", command=self.on_back, bg="#ffffff", fg=self.accent, font=(self.font_family, max(9, self.font_size - 1), "bold"), relief="groove", bd=1, padx=10, pady=4, cursor="hand2" ) 
            btn_volver.pack(anchor="w", pady=(0, 12)) 
            
        # 👨‍🏫 Encabezado de la Ficha 
        header_frame = tk.Frame(content, bg=self.accent, padx=12, pady=8, bd=1, relief="solid") 
        header_frame.pack(fill="x", pady=(0, 14)) 
        
        tk.Label( header_frame, text=f"👨‍🏫 Ficha Interactiva del Docente - {materia}", font=title_font, fg="#ffffff", bg=self.accent ).pack(side="left", anchor="w") 
        
        btn_editar = tk.Button( header_frame, text="✏️ Editar Datos Personales", command=self._abrir_modal_edicion, bg="#28a745", fg="#ffffff", font=(self.font_family, max(9, self.font_size - 1), "bold"), relief="groove", cursor="hand2", padx=10, pady=3 ) 
        btn_editar.pack(side="right") 
        
        # 📋 Información Personal / Contacto 
        info_frame = tk.LabelFrame(content, text="📌 Datos del Profesor y Contacto Institucional", bg=self.panel_bg, fg=self.accent, font=subtitle_font, padx=12, pady=10) 
        info_frame.pack(fill="x", pady=(0, 16)) 
        
        nombre = doc.get("nombre", "Docente a designar") 
        cursos = doc.get("cursos", f"{anio}º Año {esp_div}") 
        telefono = doc.get("telefono", "+54 3777 0000-0000") 
        email = doc.get("email", "consultas@escuelatecnica.edu.ar") 
        
        tk.Label(info_frame, text=f"• Profesor/a: {nombre}", font=(self.font_family, self.font_size + 1, "bold"), bg=self.panel_bg, fg=self.fg_main).pack(anchor="w", pady=2) 
        tk.Label(info_frame, text=f"• Cursos a cargo: {cursos}", font=base_font, bg=self.panel_bg, fg=self.fg_main).pack(anchor="w", pady=2) 
        tk.Label(info_frame, text=f"• Teléfono de contacto: {telefono}", font=base_font, bg=self.panel_bg, fg=self.fg_main).pack(anchor="w", pady=2) 
        tk.Label(info_frame, text=f"• Correo electrónico (Mail): {email}", font=base_font, bg=self.panel_bg, fg=self.fg_main).pack(anchor="w", pady=2) 
        
        # 📅 Tabla Interactiva de Horarios y Aulas
        table_palette = {
            "panel": "#edf6ff",
            "outer": "#edf6ff",
            "header": "#1d4ed8",
            "header_fg": "#ffffff",
            "hours": "#dbeafe",
            "hours_fg": "#1e3a8a",
            "cell": "#f8fbff",
            "cell_alt": "#eef6ff",
            "cell_fg": "#334155",
            "button_bg": "#ffffff",
            "button_fg": "#1f2937",
        }
        pnl_hor = tk.LabelFrame(content, text="📅 Tabla Interactiva de Horarios y Aulas", bg=table_palette["panel"], fg="#1d4ed8", font=subtitle_font, padx=12, pady=10)
        pnl_hor.pack(fill="both", expand=True)

        # Tabla semanal de horarios: grilla real con 5 columnas por día y filas por franja horaria
        tabla_horarios = list(doc.get("horarios_tabla", []))
        DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        FRANJAS_BASE = [
            "M1 (07:00 - 07:40)",
            "M2 (07:40 - 08:20)",
            "M3 (08:30 - 09:10)",
            "M4 (09:10 - 09:50)",
            "M5 (09:50 - 10:30)",
            "M6 (10:35 - 11:15)",
            "M7 (11:15 - 11:55)",
            "T1 (14:00 - 14:40)",
            "T2 (14:40 - 15:20)",
            "T3 (15:30 - 16:10)",
            "T4 (16:10 - 16:50)",
            "T5 (17:00 - 17:40)",
            "T6 (17:40 - 18:20)",
        ]

        def _buscar_item_por_celda(dia: str, horario: str):
            for idx, item in enumerate(tabla_horarios):
                if str(item.get("dia", "")).strip() == dia and str(item.get("horario", "")).strip() == horario:
                    return idx, item
            return None, None

        def _valor_celda(dia: str, horario: str) -> str:
            _, item = _buscar_item_por_celda(dia, horario)
            if item:
                actividad = str(item.get("actividad", "")).strip()
                aula = str(item.get("aula", "")).strip()
                if actividad and aula:
                    return f"{actividad}\n{aula}"
                return actividad or aula or "Libre"
            return "Libre"

        def _abrir_editor_celda(dia: str, horario: str):
            idx, item = _buscar_item_por_celda(dia, horario)
            top = tk.Toplevel(self)
            top.title(f"Editar horario - {dia} - {horario}")
            top.geometry("380x260")
            top.configure(bg=self.panel_bg)
            top.transient(self.winfo_toplevel())
            top.grab_set()

            tk.Label(top, text=f"✏️ {dia} · {horario}", bg=self.panel_bg, fg=self.accent, font=(self.font_family, 11, "bold")).pack(pady=(14, 8))

            form = tk.Frame(top, bg=self.panel_bg, padx=16, pady=8)
            form.pack(fill="both", expand=True)

            tk.Label(form, text="Actividad:", bg=self.panel_bg, fg=self.fg_main, font=(self.font_family, self.font_size, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 6))
            ent_actividad = tk.Entry(form, width=28, font=(self.font_family, self.font_size), bd=1, relief="solid")
            ent_actividad.grid(row=0, column=1, sticky="ew", pady=(0, 6), padx=(10, 0))
            ent_actividad.insert(0, str(item.get("actividad", "")) if item else materia)

            tk.Label(form, text="Aula:", bg=self.panel_bg, fg=self.fg_main, font=(self.font_family, self.font_size, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 10))
            ent_aula = tk.Entry(form, width=28, font=(self.font_family, self.font_size), bd=1, relief="solid")
            ent_aula.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))
            ent_aula.insert(0, str(item.get("aula", "")) if item else "Aula 4B")

            form.columnconfigure(1, weight=1)

            def _guardar_celda():
                nueva_actividad = ent_actividad.get().strip() or materia
                nueva_aula = ent_aula.get().strip() or "A confirmar"
                nuevo_item = {"dia": dia, "horario": horario, "actividad": nueva_actividad, "aula": nueva_aula}

                if item is not None and idx is not None:
                    tabla_horarios[idx] = nuevo_item
                else:
                    tabla_horarios.append(nuevo_item)

                recargar_tabla()
                top.destroy()

            def _vaciar_celda():
                if item is not None and idx is not None:
                    tabla_horarios.pop(idx)
                recargar_tabla()
                top.destroy()

            btns = tk.Frame(top, bg=self.panel_bg)
            btns.pack(fill="x", pady=(0, 12))

            tk.Button(btns, text="✅ Confirmar", command=_guardar_celda, bg="#28a745", fg="#ffffff", font=(self.font_family, 9, "bold"), relief="groove", cursor="hand2", padx=12).pack(side="left", padx=(16, 6))
            tk.Button(btns, text="🗑️ Libre / borrar", command=_vaciar_celda, bg="#dc3545", fg="#ffffff", font=(self.font_family, 9, "bold"), relief="groove", cursor="hand2", padx=12).pack(side="left", padx=(0, 6))
            tk.Button(btns, text="❌ Cancelar", command=top.destroy, bg="#6c757d", fg="#ffffff", font=(self.font_family, 9, "bold"), relief="groove", cursor="hand2", padx=12).pack(side="right", padx=(0, 16))

        def recargar_tabla():
            for child in grid_horarios.winfo_children():
                child.destroy()

            for col_idx, dia in enumerate(DIAS_SEMANA, start=1):
                header_label = tk.Label(
                    grid_horarios,
                    text=dia,
                    font=(self.font_family, self.font_size, "bold"),
                    bg=table_palette["header"],
                    fg=table_palette["header_fg"],
                    padx=6,
                    pady=6,
                    bd=1,
                    relief="solid",
                )
                setattr(header_label, "_skip_theme", True)
                header_label.grid(row=0, column=col_idx, sticky="nsew")

            for row_idx, horario in enumerate(FRANJAS_BASE, start=1):
                hour_label = tk.Label(
                    grid_horarios,
                    text=horario,
                    font=(self.font_family, self.font_size, "bold"),
                    bg=table_palette["hours"],
                    fg=table_palette["hours_fg"],
                    padx=6,
                    pady=8,
                    bd=1,
                    relief="solid",
                )
                setattr(hour_label, "_skip_theme", True)
                hour_label.grid(row=row_idx, column=0, sticky="nsew")

                for col_idx, dia in enumerate(DIAS_SEMANA, start=1):
                    valor = _valor_celda(dia, horario)
                    is_libre = valor == "Libre"
                    bg_cell = table_palette["cell_alt"] if is_libre else table_palette["cell"]
                    fg_cell = table_palette["cell_fg"]
                    celda_container = tk.Frame(grid_horarios, bg=bg_cell, bd=1, relief="solid", highlightbackground="#cfe0ff", highlightthickness=1)
                    setattr(celda_container, "_skip_theme", True)
                    celda_container.grid(row=row_idx, column=col_idx, sticky="nsew")

                    celda = tk.Label(
                        celda_container,
                        text=valor,
                        font=(self.font_family, self.font_size - 1),
                        bg=bg_cell,
                        fg=fg_cell,
                        justify="center",
                        wraplength=140,
                        padx=4,
                        pady=8,
                    )
                    setattr(celda, "_skip_theme", True)
                    celda.pack(fill="both", expand=True)

                    btn_editar_celda = tk.Button(
                        celda_container,
                        text="✎",
                        width=3,
                        bg=table_palette["button_bg"],
                        fg=table_palette["button_fg"],
                        relief="groove",
                        bd=1,
                        padx=0,
                        pady=0,
                        command=lambda d=dia, h=horario: _abrir_editor_celda(d, h),
                    )
                    setattr(btn_editar_celda, "_skip_theme", True)
                    btn_editar_celda.pack(anchor="e", padx=(0, 4), pady=(0, 4))

            for col_idx in range(0, len(DIAS_SEMANA) + 1):
                grid_horarios.columnconfigure(col_idx, weight=1)
            for row_idx in range(1, len(FRANJAS_BASE) + 1):
                grid_horarios.rowconfigure(row_idx, weight=1)

        grid_horarios = tk.Frame(pnl_hor, bg=table_palette["outer"], padx=4, pady=4)
        setattr(grid_horarios, "_skip_theme", True)
        grid_horarios.pack(fill="both", expand=True)
        recargar_tabla()

        def _guardar_tabla_completa(): 
            doc_actual = self.manager.obtener_docente_materia(ciclo, anio, esp_div, materia)
            doc_actual["horarios_tabla"] = tabla_horarios
            if self.manager.asignar_docente(ciclo, anio, esp_div, materia, doc_actual):
                if HAS_TKINTER: messagebox.showinfo("💾 Guardado", "¡La tabla de horarios fue guardada con éxito en el sistema!")
            _update_scrollregion()

        btn_box = tk.Frame(pnl_hor, bg=self.panel_bg)
        btn_box.pack(fill="x", pady=(8, 0))
        tk.Button(btn_box, text="💾 Guardar Cambios en JSON", command=_guardar_tabla_completa, bg="#28a745", fg="#ffffff", font=(self.font_family, 8, "bold"), relief="groove", cursor="hand2", padx=10).pack(side="right", padx=4)

        _update_scrollregion()
            

    def _abrir_modal_edicion(self):
        ciclo, anio, esp_div, materia = self._obtener_contexto_curso()
        doc_actual = self.manager.obtener_docente_materia(ciclo, anio, esp_div, materia)

        top = tk.Toplevel(self)
        top.title(f"✏️ Editar Ficha: {doc_actual.get('nombre', 'Docente')}")
        top.geometry("460x490")
        top.configure(bg="#ffffff")
        top.transient(self.winfo_toplevel())
        top.grab_set()

        tk.Label(top, text="✏️ Actualizar Datos Personales del Profesor", font=("Arial", 11, "bold"), fg="#007acc", bg="#ffffff").pack(pady=12)
        form = tk.Frame(top, bg="#ffffff", padx=20)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Nombre del Profesor/a:", font=("Arial", 8, "bold"), bg="#ffffff").pack(anchor="w")
        ent_nombre = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid")
        ent_nombre.pack(fill="x", pady=(0, 6))
        ent_nombre.insert(0, doc_actual.get("nombre", ""))

        tk.Label(form, text="Cursos a cargo:", font=("Arial", 8, "bold"), bg="#ffffff").pack(anchor="w")
        ent_cursos = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid")
        ent_cursos.pack(fill="x", pady=(0, 6))
        ent_cursos.insert(0, doc_actual.get("cursos", f"{anio}º Año {esp_div}"))

        tk.Label(form, text="Teléfono de contacto:", font=("Arial", 8, "bold"), bg="#ffffff").pack(anchor="w")
        ent_tel = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid")
        ent_tel.pack(fill="x", pady=(0, 6))
        ent_tel.insert(0, doc_actual.get("telefono", ""))

        tk.Label(form, text="Correo electrónico (Mail):", font=("Arial", 8, "bold"), bg="#ffffff").pack(anchor="w")
        ent_email = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid")
        ent_email.pack(fill="x", pady=(0, 6))
        ent_email.insert(0, doc_actual.get("email", ""))

        def _guardar_modal():
            nuevos = {
                "nombre": ent_nombre.get().strip() or "Docente a designar",
                "cursos": ent_cursos.get().strip() or f"{anio}º Año {esp_div}",
                "telefono": ent_tel.get().strip() or "Sin registrar",
                "email": ent_email.get().strip() or "consultas@escuelatecnica.edu.ar",
                "horarios_tabla": doc_actual.get("horarios_tabla", []),
            }

            self.manager.asignar_docente(ciclo, anio, esp_div, materia, nuevos)
            if HAS_TKINTER:
                messagebox.showinfo("💾 Guardado", "¡Información del docente actualizada!")

            top.destroy()
            self._build_ui()

        tk.Button(top, text="💾 Guardar Cambios", command=_guardar_modal, bg="#28a745", fg="#ffffff", font=("Arial", 10, "bold"), relief="groove", padx=15, pady=6, cursor="hand2").pack(pady=12)
