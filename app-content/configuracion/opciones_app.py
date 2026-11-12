import tkinter as tk 
from tkinter import ttk, messagebox
import tkinter.colorchooser as colorchooser
from tkinter import font as tkfont
import sys
from pathlib import Path

if __package__ in (None, ""):
    BASE_DIR = Path(__file__).resolve().parent.parent
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))
    from configuracion.config_manager import ( cargar_configuracion, guardar_configuracion, aplicar_estilos_ttk, TEMAS_PREDEFINIDOS )
else:
    from .config_manager import ( cargar_configuracion, guardar_configuracion, aplicar_estilos_ttk, TEMAS_PREDEFINIDOS )

def build_opciones_app_ui(parent_frame, root=None): 
    """Construye la interfaz de personalización con selectores interactivos de color.""" 
    config = cargar_configuracion() 
    main_frame = ttk.Frame(parent_frame) 
    main_frame.pack(fill="both", expand=True) 
    canvas = tk.Canvas(main_frame, highlightthickness=0, bd=0) 
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview) 
    container = ttk.Frame(canvas, padding=15) 
    canvas_window = canvas.create_window((0, 0), window=container, anchor="nw") 

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _update_scroll_region(event=None): 
        canvas.update_idletasks() 
        req_h = container.winfo_reqheight() 
        canvas_w = max(canvas.winfo_width(), 1)
        canvas.configure(scrollregion=(0, 0, canvas_w, req_h)) 

    def _on_canvas_configure(event): 
        canvas.itemconfig(canvas_window, width=event.width) 
        _update_scroll_region() 

    canvas.bind("<Configure>", _on_canvas_configure)
    container.bind("<Configure>", _update_scroll_region)

    def _on_mousewheel(event): 
        if event.num == 4: 
            canvas.yview_scroll(-2, "units") 
        elif event.num == 5: 
            canvas.yview_scroll(2, "units") 
        elif event.delta: 
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") 
            
    def _bind_mousewheel_recursive(widget): 
        widget.bind("<MouseWheel>", _on_mousewheel) 
        widget.bind("<Button-4>", _on_mousewheel) 
        widget.bind("<Button-5>", _on_mousewheel) 
        for child in widget.winfo_children(): 
            _bind_mousewheel_recursive(child)

    ttk.Label( container, text="⚙️ Personalización Visual Detallada", style="Header.TLabel", font=("Arial", 12, "bold") ).pack(anchor="w", pady=(0, 10)) 
    
    # 1. TEMAS & TIPOGRAFÍA 
    frame_general = ttk.LabelFrame(container, text=" Presets & Tipografía ", padding=10) 
    frame_general.pack(fill="x", pady=(0, 10)) 
    frame_general.columnconfigure(1, weight=1) 
    
    ttk.Label(frame_general, text="Tema Rápido:").grid(row=0, column=0, sticky="w", pady=4) 
    combo_presets = ttk.Combobox( frame_general, values=list(TEMAS_PREDEFINIDOS.keys()) + ["Custom"], state="readonly", width=24 ) 
    
    combo_presets.set(config.get("tema", "Custom")) 
    combo_presets.grid(row=0, column=1, sticky="w", pady=4, padx=8) 
    
    ttk.Label(frame_general, text="Tipografía:").grid(row=1, column=0, sticky="w", pady=4) 
    available_fonts = sorted([f for f in tkfont.families() if not f.startswith("@")]) 
    combo_font = ttk.Combobox(frame_general, values=available_fonts, state="readonly", width=24) 
    combo_font.set(config.get("font_family", "Arial")) 
    combo_font.grid(row=1, column=1, sticky="w", pady=4, padx=8) 
    
    ttk.Label(frame_general, text="Tamaño de Letra:").grid(row=2, column=0, sticky="w", pady=4) 
    spin_size = ttk.Spinbox(frame_general, from_=8, to=22, width=8) 
    spin_size.set(config.get("font_size", 10)) 
    spin_size.grid(row=2, column=1, sticky="w", pady=4, padx=8)

    # 2. SELECCIÓN INDIVIDUAL DE COLORES 
    frame_colors = ttk.LabelFrame(container, text=" Personalización Individual de Colores ", padding=10) 
    frame_colors.pack(fill="x", pady=(0, 10)) 
    frame_colors.columnconfigure(1, weight=1) 
    
    colors = { "bg_color": config.get("bg_color", "#ffffff"), "fg_color": config.get("fg_color", "#212529"), "panel_bg": config.get("panel_bg", "#f8f9fa"), "accent_color": config.get("accent_color", "#007acc") } 
    
    color_buttons = {} 
    
    def pick_color(key, button_widget): 
        chosen = colorchooser.askcolor(initialcolor=colors[key], title=f"Seleccionar {key}") 
        if chosen[1]: 
            colors[key] = chosen[1] 
            button_widget.config(bg=colors[key], text=colors[key]) 
            combo_presets.set("Custom") 
            update_preview() 
    
    color_items = [ ("Color Fondo Principal:", "bg_color", 0), ("Color Texto del Cuerpo:", "fg_color", 1), ("Color Fondo Paneles/Tarjetas:", "panel_bg", 2), ("Color Acento (Títulos/Destacados):", "accent_color", 3) ] 
    
    for label_text, key, row_idx in color_items: 
        ttk.Label(frame_colors, text=label_text).grid(row=row_idx, column=0, sticky="w", pady=4) 
        btn = tk.Button( frame_colors, text=colors[key], bg=colors[key], fg="#ffffff" if colors[key] in ["#1e1e1e", "#0f172a", "#007acc", "#212529"] else "#000000", width=12, relief="solid", bd=1, cursor="hand2" ) 
        btn.config(command=lambda k=key, b=btn: pick_color(k, b)) 
        btn.grid(row=row_idx, column=1, sticky="w", pady=4, padx=8) 
        color_buttons[key] = btn 
        
    def apply_preset(event=None): 
        preset_name = combo_presets.get() 
        if preset_name in TEMAS_PREDEFINIDOS: 
            preset_data = TEMAS_PREDEFINIDOS[preset_name] 
            for k, val in preset_data.items(): 
                colors[k] = val 
                if k in color_buttons: 
                    color_buttons[k].config(bg=val, text=val) 
            update_preview() 
            
    combo_presets.bind("<<ComboboxSelected>>", apply_preset)

    # 3. VISTA PREVIA EN TIEMPO REAL 
    frame_preview = ttk.LabelFrame(container, text=" Vista Previa en Tiempo Real ", padding=10) 
    frame_preview.pack(fill="both", expand=True, pady=(0, 10)) 
    
    preview_card = tk.Frame(frame_preview, bd=1, relief="solid", padx=10, pady=10) 
    preview_card.pack(fill="both", expand=True) 
    
    lbl_preview_title = tk.Label(preview_card, text="Título de Ejemplo / Acento", font=("Arial", 11, "bold")) 
    lbl_preview_title.pack(anchor="w", pady=(0, 4)) 
    
    txt_preview = tk.Text(preview_card, height=4, wrap="word", padx=6, pady=6, bd=1, relief="solid") 
    txt_preview.pack(fill="both", expand=True) 
    txt_preview.insert("1.0", "Este texto refleja el color de fondo, texto de cuerpo y tipografía en tiempo real.") 
    
    def update_preview(*args): 
        font_name = combo_font.get() or "Arial" 
        try: 
            font_sz = int(spin_size.get()) 
        except ValueError: 
            font_sz = 10 
            
        preview_card.config(bg=colors["panel_bg"]) 
        lbl_preview_title.config( font=(font_name, font_sz + 1, "bold"), bg=colors["panel_bg"], fg=colors["accent_color"] ) 
        txt_preview.config( font=(font_name, font_sz), bg=colors["bg_color"], fg=colors["fg_color"] ) 
        
    combo_font.bind("<<ComboboxSelected>>", update_preview)
    spin_size.bind("<KeyRelease>", update_preview)

    update_preview() 

    # 4. BARRAS DE ACCIÓN 
    def save_and_apply(): 
        try: 
            font_sz = int(spin_size.get()) 
        except ValueError: 
            font_sz = 10 
            
        config["font_family"] = combo_font.get() 
        config["font_size"] = font_sz 
        config["tema"] = combo_presets.get() 
        config.update(colors) 
        
        if guardar_configuracion(config): 
            if root: 
                if __package__ in (None, ""):
                    from configuracion.config_manager import aplicar_estilos_globales
                else:
                    from .config_manager import aplicar_estilos_globales
                aplicar_estilos_globales(root, config)
            messagebox.showinfo("Éxito", "¡Configuración visual guardada y aplicada!") 
            
    btn_save = ttk.Button(container, text="💾 Guardar Ajustes Individuales", command=save_and_apply) 
    btn_save.pack(anchor="e", pady=(5, 15)) 
    
    _bind_mousewheel_recursive(container) 
    return parent_frame