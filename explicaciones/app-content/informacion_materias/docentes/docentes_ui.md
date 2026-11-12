import tkinter as tk 
from tkinter import ttk, messagebox 

try:
    HAS_TKINTER = True 
except ImportError: 
    HAS_TKINTER = False 

from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales
from .docentes_manager import DocentesManager 

class VistaDocentePage(tk.Frame): 
    """Página con la ficha detallada del Docente: Datos de contacto y Tabla de Horarios.""" 
    
    def __init__(self, parent, contexto: dict, on_back_callback=None): 
        self.config = cargar_configuracion()
        self.bg_main = self.config.get("bg_color", "#ffffff")
        self.fg_main = self.config.get("fg_color", "#212529")
        self.panel_bg = self.config.get("panel_bg", "#f8f9fa")
        self.accent = self.config.get("accent_color", "#007acc")
        self.font_family = self.config.get("font_family", "Arial")
        self.font_size = self.config.get("font_size", 10)

        super().__init__(parent, bg=self.panel_bg, padx=25, pady=20)
        self.pack(fill="both", expand=True)
        self.contexto = contexto or {}
        self.on_back = on_back_callback
        self.manager = DocentesManager()
        aplicar_estilos_globales(self, self.config)
        self._build_ui()

    def _obtener_contexto_curso(self):
        ciclo_raw = self.contexto.get("ciclo")
        ciclo = str(ciclo_raw or "Ciclo General")

        anio_raw = self.contexto.get("anio")
        try:
            anio = int(anio_raw) if anio_raw is not None else 1
        except (TypeError, ValueError):
            anio = 1

        esp_div_raw = self.contexto.get("division") if ciclo == "Ciclo Básico" else self.contexto.get("especialidad")
        esp_div = str(esp_div_raw or "General")
        materia = str(self.contexto.get("materia") or "Lengua")
        return ciclo, anio, esp_div, materia
        
    def _build_ui(self):
        ciclo, anio, esp_div, materia = self._obtener_contexto_curso()

        doc = self.manager.obtener_docente_materia(ciclo, anio, esp_div, materia)
        base_font = (self.font_family, self.font_size)
        title_font = (self.font_family, max(13, self.font_size + 4), "bold")
        subtitle_font = (self.font_family, max(10, self.font_size + 1), "bold")

        scroll_canvas = tk.Canvas(self, bg=self.panel_bg, highlightthickness=0)
        scroll_canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=scroll_canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=v_scrollbar.set)

        content = tk.Frame(scroll_canvas, bg=self.panel_bg, padx=20, pady=18)
        canvas_window = scroll_canvas.create_window((0, 0), window=content, anchor="nw")

        def _update_scrollregion(event=None):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        def _resize_content(event=None):
            width = getattr(event, "width", scroll_canvas.winfo_width())
            scroll_canvas.itemconfigure(canvas_window, width=max(420, width))

        content.bind("<Configure>", _update_scrollregion)
        scroll_canvas.bind("<Configure>", _resize_content)

        if self.on_back:
            btn_volver = tk.Button(content, text="⬅️ Volver a la Materia", command=self.on_back, bg="#e0e0e0", fg="#333333", font=(self.font_family, max(9, self.font_size - 1), "bold"), relief="groove", bd=1, cursor="hand2")
            btn_volver.pack(anchor="w", pady=(0, 15))

        header_frame = tk.Frame(content, bg=self.panel_bg)
        header_frame.pack(fill="x", pady=(0, 15))
        tk.Label(header_frame, text=f"👨‍🏫 Ficha del Docente - {materia}", font=title_font, fg=self.accent, bg=self.panel_bg).pack(side="left")

        btn_editar = tk.Button(header_frame, text="✏️ Editar Datos", command=self._abrir_modal_edicion, bg="#28a745", fg="white", font=(self.font_family, max(9, self.font_size - 1), "bold"), relief="groove", cursor="hand2")
        btn_editar.pack(side="right")

        info_frame = tk.Frame(content, bg=self.panel_bg)
        info_frame.pack(fill="x", pady=(0, 15))
        nombre = doc.get("nombre", "Docente a designar")
        cursos = doc.get("cursos", f"{anio}º Año {esp_div}")
        telefono = doc.get("telefono", "+54 3777 0000-0000")
        email = doc.get("email", "consultas@escuelatecnica.edu.ar")

        tk.Label(info_frame, text="Docente:", font=subtitle_font, fg=self.accent, bg=self.panel_bg).pack(anchor="w")
        tk.Label(info_frame, text=f" • {nombre}", font=base_font, bg=self.panel_bg, fg=self.fg_main).pack(anchor="w", pady=(0, 8))

        tk.Label(info_frame, text="Cursos:", font=subtitle_font, fg=self.accent, bg=self.panel_bg).pack(anchor="w")
        tk.Label(info_frame, text=f" • {cursos}", font=base_font, bg=self.panel_bg, fg=self.fg_main).pack(anchor="w", pady=(0, 8))

        tk.Label(info_frame, text="Contactos:", font=subtitle_font, fg=self.accent, bg=self.panel_bg).pack(anchor="w")
        tk.Label(info_frame, text=f" > Número telefónico: {telefono}", font=base_font, bg=self.panel_bg, fg=self.fg_main).pack(anchor="w")
        tk.Label(info_frame, text=f" > Mail: {email}", font=base_font, bg=self.panel_bg, fg=self.fg_main).pack(anchor="w", pady=(0, 15))

        tk.Label(content, text="Horas (Tabla de Horarios):", font=subtitle_font, fg=self.accent, bg=self.panel_bg).pack(anchor="w", pady=(0, 6))

        form_horario = tk.Frame(content, bg=self.panel_bg, pady=6)
        form_horario.pack(fill="x", pady=(0, 8))

        tk.Label(form_horario, text="Día:", font=(self.font_family, self.font_size, "bold"), bg=self.panel_bg, fg=self.fg_main).grid(row=0, column=0, sticky="w", padx=(0, 6), pady=(0, 4))
        entry_dia = tk.Entry(form_horario, width=14, font=base_font, bd=1, relief="solid")
        entry_dia.grid(row=0, column=1, padx=(0, 10), pady=(0, 4))

        tk.Label(form_horario, text="Horario:", font=(self.font_family, self.font_size, "bold"), bg=self.panel_bg, fg=self.fg_main).grid(row=0, column=2, sticky="w", padx=(0, 6), pady=(0, 4))
        entry_horario = tk.Entry(form_horario, width=18, font=base_font, bd=1, relief="solid")
        entry_horario.grid(row=0, column=3, padx=(0, 10), pady=(0, 4))

        tk.Label(form_horario, text="Actividad:", font=(self.font_family, self.font_size, "bold"), bg=self.panel_bg, fg=self.fg_main).grid(row=1, column=0, sticky="w", padx=(0, 6), pady=(0, 4))
        entry_actividad = tk.Entry(form_horario, width=26, font=base_font, bd=1, relief="solid")
        entry_actividad.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0, 10), pady=(0, 4))

        tk.Label(form_horario, text="Aula:", font=(self.font_family, self.font_size, "bold"), bg=self.panel_bg, fg=self.fg_main).grid(row=1, column=3, sticky="w", padx=(0, 6), pady=(0, 4))
        entry_aula = tk.Entry(form_horario, width=18, font=base_font, bd=1, relief="solid")
        entry_aula.grid(row=1, column=4, padx=(0, 8), pady=(0, 4))

        form_horario.columnconfigure(1, weight=1)
        form_horario.columnconfigure(3, weight=1)

        columns = ("Día", "Horario", "Materia / Actividad", "Aula / Modulo")
        style_name = "DocenteTable.Treeview"
        style = ttk.Style(self)
        style.configure(style_name, background=self.bg_main, foreground=self.fg_main, fieldbackground=self.bg_main, rowheight=max(26, self.font_size + 12), font=base_font)
        style.configure(f"{style_name}.Heading", background=self.panel_bg, foreground=self.fg_main, font=(self.font_family, self.font_size, "bold"))
        style.map(style_name, background=[("selected", self.accent)], foreground=[("selected", "#ffffff")])

        tree = ttk.Treeview(content, columns=columns, show="headings", height=6, style=style_name)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=max(120, 180 + self.font_size * 4), stretch=True)
        tree.pack(fill="both", expand=True, pady=(0, 8))

        def recargar_tabla(lista):
            tree.delete(*tree.get_children())
            for h in lista:
                tree.insert("", "end", values=(h.get("dia", ""), h.get("horario", ""), h.get("actividad", ""), h.get("aula", "")))

        tabla_horarios = doc.get("horarios_tabla", [{"dia": "Lunes", "horario": "07:45 - 09:15", "actividad": materia, "aula": "Aula 4B"}, {"dia": "Miércoles", "horario": "09:30 - 11:00", "actividad": materia, "aula": "Aula 4B"}, {"dia": "Viernes", "horario": "11:15 - 12:45", "actividad": "Consulta / Apoyo", "aula": "Taller Central"}])
        recargar_tabla(tabla_horarios)

        def _agregar_horario():
            dia = entry_dia.get().strip()
            horario = entry_horario.get().strip()
            actividad = entry_actividad.get().strip() or materia
            aula = entry_aula.get().strip() or "A confirmar"

            if not dia or not horario:
                messagebox.showwarning("Atención", "Completa al menos el día y el horario para agregar una fila.")
                return

            tabla_horarios.append({"dia": dia, "horario": horario, "actividad": actividad, "aula": aula})
            recargar_tabla(tabla_horarios)
            entry_dia.delete(0, "end")
            entry_horario.delete(0, "end")
            entry_actividad.delete(0, "end")
            entry_aula.delete(0, "end")

        def _guardar_horarios():
            doc_actual = self.manager.obtener_docente_materia(ciclo, anio, esp_div, materia)
            doc_actual["horarios_tabla"] = tabla_horarios
            self.manager.asignar_docente(ciclo, anio, esp_div, materia, doc_actual)
            messagebox.showinfo("Guardado", "La tabla de horarios del docente fue actualizada.")

        btn_agregar = tk.Button(form_horario, text="➕ Agregar horario", command=_agregar_horario, bg=self.accent, fg="white", font=(self.font_family, max(9, self.font_size - 1), "bold"), relief="groove", cursor="hand2")
        btn_agregar.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 4))

        btn_guardar = tk.Button(form_horario, text="💾 Guardar tabla", command=_guardar_horarios, bg="#28a745", fg="white", font=(self.font_family, max(9, self.font_size - 1), "bold"), relief="groove", cursor="hand2")
        btn_guardar.grid(row=2, column=2, columnspan=2, sticky="w", pady=(8, 4))

        btn_borrar = tk.Button(form_horario, text="🗑️ Borrar fila seleccionada", command=lambda: _borrar_fila_seleccionada(tree, tabla_horarios), bg="#dc3545", fg="white", font=(self.font_family, max(9, self.font_size - 1), "bold"), relief="groove", cursor="hand2")
        btn_borrar.grid(row=2, column=4, sticky="w", pady=(8, 4))

        def _borrar_fila_seleccionada(tree_widget, lista):
            selected = tree_widget.selection()
            if not selected:
                messagebox.showwarning("Atención", "Selecciona una fila de la tabla para borrar.")
                return
            item_id = selected[0]
            values = tree_widget.item(item_id, "values")
            for idx, fila in enumerate(lista):
                if (fila.get("dia", ""), fila.get("horario", ""), fila.get("actividad", ""), fila.get("aula", "")) == tuple(values):
                    del lista[idx]
                    break
            recargar_tabla(lista)

        _update_scrollregion()
    
    def _abrir_modal_edicion(self): 
            """Abre un diálogo flotante para editar la ficha del docente sin tocar el JSON.""" 
            ciclo, anio, esp_div, materia = self._obtener_contexto_curso()
            doc_actual = self.manager.obtener_docente_materia(ciclo, anio, esp_div, materia) 
            
            # Ventana Emergente Modal 
            top = tk.Toplevel(self)
            top.title(f"Editar Ficha: {doc_actual.get('nombre', 'Docente')}") 
            top.geometry("450x480") 
            top.configure(bg="#ffffff") 
            top.transient(self.winfo_toplevel())
            top.grab_set() 
            
            tk.Label( top, text="✏️ Actualizar Información Docente", font=("Arial", 12, "bold"), fg="#007acc", bg="#ffffff" ).pack(pady=12) 
            form = tk.Frame(top, bg="#ffffff", padx=20) 
            form.pack(fill="both", expand=True) 
            
            # Campos de Texto 
            tk.Label(form, text="Nombre del Docente:", font=("Arial", 9, "bold"), bg="#ffffff").pack(anchor="w") 
            ent_nombre = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid") 
            ent_nombre.pack(fill="x", pady=(0, 8)) 
            ent_nombre.insert(0, doc_actual.get("nombre", "")) 
            
            tk.Label(form, text="Cursos a cargo:", font=("Arial", 9, "bold"), bg="#ffffff").pack(anchor="w") 
            ent_cursos = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid") 
            ent_cursos.pack(fill="x", pady=(0, 8)) 
            ent_cursos.insert(0, doc_actual.get("cursos", f"{anio}º Año {esp_div}")) 
            
            tk.Label(form, text="Número telefónico:", font=("Arial", 9, "bold"), bg="#ffffff").pack(anchor="w") 
            ent_tel = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid") 
            ent_tel.pack(fill="x", pady=(0, 8)) 
            ent_tel.insert(0, doc_actual.get("telefono", "")) 
            
            tk.Label(form, text="Correo electrónico (Mail):", font=("Arial", 9, "bold"), bg="#ffffff").pack(anchor="w") 
            ent_email = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid") 
            ent_email.pack(fill="x", pady=(0, 8)) 
            ent_email.insert(0, doc_actual.get("email", "")) 
            
            # Horarios resumen rápido 
            tk.Label(form, text="Horario de atención / consulta:", font=("Arial", 9, "bold"), bg="#ffffff").pack(anchor="w") 
            ent_horario = tk.Entry(form, font=("Arial", 9), bd=1, relief="solid") 
            ent_horario.pack(fill="x", pady=(0, 15)) 
            ent_horario.insert(0, doc_actual.get("horario_consulta", "Martes 14:00 - 15:30")) 
            
            def _guardar(): 
                nuevos_datos = { "nombre": ent_nombre.get().strip() or "Docente a designar", "cursos": ent_cursos.get().strip() or f"{anio}º Año {esp_div}", "telefono": ent_tel.get().strip() or "Sin registrar", "email": ent_email.get().strip() or "consultas@escuelatecnica.edu.ar", "horario_consulta": ent_horario.get().strip(), "horarios_tabla": doc_actual.get("horarios_tabla", []) } 
                
                # Persistir cambios en el JSON 
                self.manager.asignar_docente(ciclo, anio, esp_div, materia, nuevos_datos) 
                messagebox.showinfo("Guardado", "Los datos del docente se actualizaron correctamente.") 
                top.destroy() 
                
                # Recargar la vista actual 
                for child in list(self.winfo_children()):
                    child.destroy()
                self._build_ui()
            
            tk.Button( top, text="💾 Guardar Cambios", command=_guardar, bg="#007acc", fg="white", font=("Arial", 10, "bold"), relief="groove", padx=15, pady=5, cursor="hand2" ).pack(pady=15)
