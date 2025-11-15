# gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import threading
from typing import List, Dict, Any

from complexity_detector import ComplexityDetector
from code_executor import CodeExecutor
from complexity_analyzer import ComplexityAnalyzer
from AnalisisDeAlgoritmos.tutorial_helperAdG import TutorialWindow, HelpDialog
from ejemplos_python import EjemplosWindow
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import ModernDarkTheme


class TemporalAnalyzerGUI:
    """Interfaz gráfica principal"""
    
    def __init__(self, root, return_callback=None):
        self.root = root
        self.return_callback = return_callback
        self.root.title("🚀 Analizador de Complejidad Temporal")
        self.root.geometry("1500x900")
        
        self.current_results = None
        self.detected_complexity = None
        self.is_analyzing = False
        
        # Configuraciones de ejecución
        self.predefined_configs = [700, 1500, 3000]

        self.root.protocol("WM_DELETE_WINDOW", self.on_Closing)
        
        self.setup_ui()

    def on_Closing(self):
        """Maneja el cierre de la ventana"""
        if self.is_analyzing:
            if not messagebox.askokcancel(
                "Salir",
                "Un análisis está en curso. ¿Seguro que deseas salir?"
            ):
                return
        # Ejecutar callback para volver al menú
        if self.return_callback:
            self.return_callback()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Panel principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ===== PANEL IZQUIERDO CON SCROLL =====
        left_panel = ttk.Frame(main_frame, width=550)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Canvas para scroll
        canvas = tk.Canvas(left_panel, highlightthickness=0, width=530)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_scroll_region)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido del panel izquierdo
        self.setup_left_panel(scrollable_frame)
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # ===== PANEL DERECHO =====
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.setup_right_panel(right_panel)
    
    def setup_left_panel(self, parent):
        """Configura el panel izquierdo"""
        colors = ModernDarkTheme.COLORS

        back_btn = ttk.Button(
            parent,
            text="◀️ Volver al Menú Principal",
            command=self.return_to_menu
        )
        back_btn.pack(fill=tk.X, padx=5, pady=(5, 5))
        
        # Botón de tutorial
        tutorial_btn = ttk.Button(
            parent,
            text="📖 Ver Tutorial Interactivo",
            command=lambda: TutorialWindow(self.root)
        )
        tutorial_btn.pack(fill=tk.X, padx=5, pady=(5, 10))
        
        # Botón de ejemplos
        examples_btn = ttk.Button(
            parent,
            text="📝 Cargar Ejemplos de Código",
            command=self.show_examples
        )
        examples_btn.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        # Editor de código
        editor_header = ttk.Frame(parent)
        editor_header.pack(fill=tk.X, padx=5, pady=(5, 2))
        
        ttk.Label(editor_header, text="Código Python:", style='Heading.TLabel').pack(side=tk.LEFT)
        ttk.Button(
            editor_header,
            text="?",
            width=3,
            command=lambda: HelpDialog.show(self.root, "editor")
        ).pack(side=tk.RIGHT)
        
        # Configurar colores del editor
        self.code_editor = scrolledtext.ScrolledText(
            parent, 
            height=15, 
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=colors['bg_tertiary'],
            fg=colors['text_primary'],
            insertbackground=colors['accent'],
            selectbackground=colors['accent'],
            selectforeground='#ffffff'
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        example_code = """# Ejemplo de función o código:
def suma(a, b):
    return a + b

# O código directo:
# resultado = x ** 2 + y * 3

# O algoritmo más complejo:
# def fibonacci(n):
#     if n <= 1:
#         return n
#     return fibonacci(n-1) + fibonacci(n-2)"""
        self.code_editor.insert('1.0', example_code)
        
        # Frame de configuración
        control_frame = ttk.LabelFrame(parent, text="⚙️  Configuración de Análisis", padding=15)
        control_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Configuración de ejecuciones
        exec_header = ttk.Frame(control_frame)
        exec_header.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(exec_header, text="Número de Ejecuciones", style='Heading.TLabel').pack(side=tk.LEFT)
        ttk.Button(
            exec_header,
            text="?",
            width=3,
            command=lambda: HelpDialog.show(self.root, "ejecuciones")
        ).pack(side=tk.RIGHT)
        
        exec_frame = ttk.Frame(control_frame)
        exec_frame.pack(fill=tk.X, pady=5)
        
        self.exec_mode_var = tk.StringVar(value="predefined")
        
        ttk.Radiobutton(
            exec_frame,
            text="📊 Estándar (700, 1500, 3000)",
            variable=self.exec_mode_var,
            value="predefined",
            command=self.on_exec_mode_change
        ).pack(anchor=tk.W, pady=3)
        
        ttk.Radiobutton(
            exec_frame,
            text="✏️ Personalizado",
            variable=self.exec_mode_var,
            value="custom",
            command=self.on_exec_mode_change
        ).pack(anchor=tk.W, pady=3)
        
        # Frame para ejecuciones personalizadas
        self.custom_exec_frame = ttk.Frame(control_frame)
        
        custom_grid = ttk.Frame(self.custom_exec_frame)
        custom_grid.pack(fill=tk.X, pady=5)
        
        ttk.Label(custom_grid, text="Config 1:").grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self.custom_exec1 = ttk.Entry(custom_grid, width=12)
        self.custom_exec1.grid(row=0, column=1, padx=5, pady=3)
        self.custom_exec1.insert(0, "3000")
        
        ttk.Label(custom_grid, text="Config 2:").grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
        self.custom_exec2 = ttk.Entry(custom_grid, width=12)
        self.custom_exec2.grid(row=1, column=1, padx=5, pady=3)
        self.custom_exec2.insert(0, "7000")
        
        ttk.Label(custom_grid, text="Config 3:").grid(row=2, column=0, padx=5, pady=3, sticky=tk.W)
        self.custom_exec3 = ttk.Entry(custom_grid, width=12)
        self.custom_exec3.grid(row=2, column=1, padx=5, pady=3)
        self.custom_exec3.insert(0, "15000")
        
        ttk.Label(
            self.custom_exec_frame,
            text="ℹ️  Límite máximo: 1,000,000 ejecuciones",
            style='Secondary.TLabel'
        ).pack(pady=5)
        
        ttk.Label(
            control_frame,
            text="ℹ️  Se tomarán 20 puntos muestreados de cada configuración",
            style='Secondary.TLabel'
        ).pack(pady=5)
        
        # Separator
        separator1 = ttk.Frame(control_frame, height=1)
        separator1.pack(fill=tk.X, pady=10)
        
        # Botones de acción
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Grid para botones
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Button(
            button_frame, 
            text="▶  ANALIZAR", 
            command=self.analyze_code,
            style="Accent.TButton"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        ttk.Button(
            button_frame, 
            text="🔍 Detectar", 
            command=self.detect_complexity_only
        ).grid(row=1, column=0, sticky=tk.EW, padx=(0, 3), pady=2)
        
        ttk.Button(
            button_frame, 
            text="✓ Sintaxis", 
            command=self.check_syntax
        ).grid(row=1, column=1, sticky=tk.EW, padx=(3, 0), pady=2)
        
        ttk.Button(
            button_frame, 
            text="🗑 Limpiar", 
            command=self.clear_editor
        ).grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=2)
        
        # Barra de progreso
        self.progress_frame = ttk.Frame(control_frame)
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="",
            style='Secondary.TLabel'
        )
        self.progress_label.pack(pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Resultados
        results_header = ttk.Frame(parent)
        results_header.pack(fill=tk.X, padx=5, pady=(10, 2))
        
        ttk.Label(results_header, text="Resultados:", style='Heading.TLabel').pack(side=tk.LEFT)
        
        self.results_text = scrolledtext.ScrolledText(
            parent, 
            height=10, 
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=colors['bg_tertiary'],
            fg=colors['text_primary']
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.on_exec_mode_change()
    
    def setup_right_panel(self, parent):
        """Configura el panel derecho"""
        colors = ModernDarkTheme.COLORS
        
        # Complejidad detectada
        complexity_frame = ttk.LabelFrame(parent, text="🎯  Complejidad Detectada", padding=15)
        complexity_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.complexity_label = ttk.Label(
            complexity_frame, 
            text="Ejecuta un análisis primero", 
            font=("Segoe UI", 14, "bold"),
            foreground=colors['accent']
        )
        self.complexity_label.pack(pady=5)
        
        self.notation_label = ttk.Label(
            complexity_frame, 
            text="", 
            font=("Consolas", 11),
            foreground=colors['text_secondary']
        )
        self.notation_label.pack(pady=5)
        
        self.confidence_label = ttk.Label(
            complexity_frame, 
            text="", 
            font=("Segoe UI", 9),
            foreground=colors['text_secondary']
        )
        self.confidence_label.pack()
        
        # Visualización
        viz_frame = ttk.LabelFrame(parent, text="📈  Visualización Temporal", padding=10)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear figura con 3 subplots
        self.figure, self.axes = plt.subplots(1, 3, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        export_btn = ttk.Button(
            viz_frame, 
            text="💾 Exportar Gráfico PNG", 
            command=self.export_graph
        )
        export_btn.pack(pady=10)
        
        self.show_empty_graph()
    
    def on_exec_mode_change(self):
        """Maneja el cambio de modo de ejecución"""
        if self.exec_mode_var.get() == "custom":
            self.custom_exec_frame.pack(fill=tk.X, pady=5)
        else:
            self.custom_exec_frame.pack_forget()
    
    def log_result(self, message: str, clear: bool = False):
        """Escribe en el área de resultados"""
        self.results_text.config(state=tk.NORMAL)
        if clear:
            self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def detect_complexity_only(self):
        """Detecta solo la complejidad sin ejecutar el código"""
        code = self.code_editor.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "Por favor ingresa código para analizar")
            return
        
        self.log_result("🔍 Analizando estructura del código...", clear=True)
        
        detector = ComplexityDetector(code)
        result = detector.analyze()
        
        self.detected_complexity = result
        self.update_complexity_display(result)
        
        self.log_result(f"\n📊 Análisis estático completado:")
        self.log_result(f"  • Complejidad detectada: {result['complexity']}")
        self.log_result(f"  • Notación: {result['notation']}")
        self.log_result(f"  • Es recursivo: {'Sí' if result.get('is_recursive', False) else 'No'}")
        self.log_result(f"  • Confianza: {result['confidence']*100:.1f}%")
    
    def update_complexity_display(self, complexity_info: Dict[str, Any]):
        """Actualiza la visualización de complejidad"""
        self.complexity_label.config(text=f"Complejidad: {complexity_info['complexity']}")
        
        notation = complexity_info['notation']
        if complexity_info.get('is_recursive', False):
            self.notation_label.config(text=f"Recurrencia: {notation}")
        else:
            self.notation_label.config(text=f"Notación: {notation}")
        
        confidence = complexity_info.get('confidence', 0) * 100
        self.confidence_label.config(text=f"Confianza: {confidence:.1f}%")
    
    def check_syntax(self):
        """Verifica la sintaxis del código"""
        code = self.code_editor.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "Por favor ingresa código para verificar")
            return
        
        result = CodeExecutor.test_code_syntax(code)
        
        if result['valid']:
            messagebox.showinfo("Sintaxis", "✓ La sintaxis del código es correcta")
            self.log_result("✓ Sintaxis correcta", clear=True)
        else:
            messagebox.showerror("Error de Sintaxis", f"✗ Error:\n{result['error']}")
            self.log_result(f"✗ Error de sintaxis:\n{result['error']}", clear=True)
    
    def get_execution_configs(self) -> List[int]:
        """Obtiene las configuraciones de ejecución"""
        if self.exec_mode_var.get() == "predefined":
            return self.predefined_configs
        else:
            try:
                config1 = int(self.custom_exec1.get())
                config2 = int(self.custom_exec2.get())
                config3 = int(self.custom_exec3.get())
                
                # Validar límites
                max_limit = 1000000
                if any(c <= 0 or c > max_limit for c in [config1, config2, config3]):
                    messagebox.showerror(
                        "Error",
                        f"Las configuraciones deben estar entre 1 y {max_limit:,}"
                    )
                    return None # type: ignore
                
                # Ordenar de menor a mayor
                configs = sorted([config1, config2, config3])
                return configs
                
            except ValueError:
                messagebox.showerror("Error", "Los valores deben ser números enteros")
                return None # type: ignore
    
    def analyze_code(self):
        """Inicia el análisis del código"""
        if self.is_analyzing:
            messagebox.showwarning("Advertencia", "Ya hay un análisis en curso")
            return
        
        code = self.code_editor.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "Por favor ingresa código para analizar")
            return
        
        # Verificar sintaxis
        syntax_result = CodeExecutor.test_code_syntax(code)
        if not syntax_result['valid']:
            messagebox.showerror("Error de Sintaxis", f"✗ Error:\n{syntax_result['error']}")
            self.log_result(f"✗ Error de sintaxis:\n{syntax_result['error']}", clear=True)
            return
        
        # Obtener configuraciones
        configs = self.get_execution_configs()
        if configs is None:
            return
        
        # Detectar complejidad
        detector = ComplexityDetector(code)
        complexity_result = detector.analyze()
        self.detected_complexity = complexity_result
        self.update_complexity_display(complexity_result)
        
        # Iniciar análisis en thread
        self.is_analyzing = True
        self.progress_frame.pack(fill=tk.X, pady=10)
        self.log_result("🔄 Iniciando análisis...", clear=True)
        
        thread = threading.Thread(
            target=self.run_analysis,
            args=(code, configs),
            daemon=True
        )
        thread.start()
    
    def update_progress(self, overall: float, config: int, config_progress: float):
        """Actualiza la barra de progreso"""
        self.progress_bar['value'] = overall
        self.progress_label.config(
            text=f"Analizando con {config:,} ejecuciones... {config_progress:.1f}%"
        )
        self.root.update_idletasks()
    
    def run_analysis(self, code: str, configs: List[int]):
        """Ejecuta el análisis en thread separado"""
        try:
            results = ComplexityAnalyzer.analyze_multiple_executions(
                code,
                configs,
                lambda o, c, p: self.root.after(0, lambda: self.update_progress(o, c, p))
            )
            
            if not results['success']: # type: ignore
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Error en configuración {results['failed_config']}:\n{results['error']}" # type: ignore
                ))
                self.root.after(0, lambda: self.log_result(f"✗ Error: {results['error']}")) # type: ignore
            else:
                self.current_results = results['results'] # type: ignore
                self.root.after(0, lambda: self.display_results(results['results'], configs)) # type: ignore
                self.root.after(0, lambda: messagebox.showinfo("Éxito", "Análisis completado"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error",
                f"Error durante el análisis:\n{str(e)}"
            ))
        finally:
            self.is_analyzing = False
            self.root.after(0, self.progress_frame.pack_forget)
    
    def display_results(self, results: Dict[int, Dict], configs: List[int]):
        """Muestra los resultados en el log y gráficos"""
        self.log_result("\n✓ Análisis completado:", clear=False)
        
        for config in configs:
            data = results[config]
            self.log_result(f"\n📊 Configuración: {config:,} ejecuciones")
            self.log_result(f"  • Tiempo promedio: {ComplexityAnalyzer.format_time(data['avg_time'])}")
            self.log_result(f"  • Desviación estándar: {ComplexityAnalyzer.format_time(data['std_time'])}")
            self.log_result(f"  • Tiempo mínimo: {ComplexityAnalyzer.format_time(data['min_time'])}")
            self.log_result(f"  • Tiempo máximo: {ComplexityAnalyzer.format_time(data['max_time'])}")
        
        # Graficar resultados
        self.plot_results(results, configs)
    
    def plot_results(self, results: Dict[int, Dict], configs: List[int]):
        """Genera los 3 subplots con los resultados"""
        colors = ModernDarkTheme.get_chart_colors()
        
        # Limpiar axes
        for ax in self.axes:
            ax.clear()
        
        for idx, config in enumerate(configs):
            data = results[config]
            ax = self.axes[idx]
            
            color = colors[idx]
            
            # Graficar línea de tiempos muestreados
            ax.plot(
                data['sampled_indices'],
                data['sampled_times'],
                'o-',
                linewidth=2.5,
                markersize=7,
                color=color,
                label=f"{config:,} ejecuciones",
                markeredgewidth=0,
                alpha=0.9
            )
            
            # Línea promedio
            avg_line = np.mean(data['sampled_times'])
            ax.axhline(
                y=avg_line,
                color=color,
                linestyle='--',
                linewidth=1.5,
                alpha=0.6
            )
            
            ax.set_xlabel('Ejecución #', fontsize=10, fontweight='600')
            ax.set_ylabel('Tiempo (s)', fontsize=10, fontweight='600')
            ax.set_title(f'{config:,} ejecuciones', fontsize=11, fontweight='bold', pad=15)
            ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
            ax.set_axisbelow(True)
            ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
            
            # Mejorar apariencia
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Agregar texto con tiempo promedio
            ax.text(
                0.95, 0.95,
                f'Promedio:\n{ComplexityAnalyzer.format_time(data["avg_time"])}',
                transform=ax.transAxes,
                fontsize=9,
                verticalalignment='top',
                horizontalalignment='right',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.6', 
                         facecolor=ModernDarkTheme.COLORS['bg_secondary'], 
                         alpha=0.9,
                         edgecolor=ModernDarkTheme.COLORS['border'])
            )
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def show_empty_graph(self):
        """Muestra gráficos vacíos iniciales"""
        colors = ModernDarkTheme.COLORS
        
        for ax in self.axes:
            ax.clear()
            ax.text(
                0.5, 0.5,
                'Ejecuta un\nanálisis primero',
                ha='center',
                va='center',
                fontsize=12,
                color=colors['text_secondary'],
                transform=ax.transAxes,
                fontweight='500'
            )
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor(colors['bg_tertiary'])
        self.canvas.draw()
    
    def export_graph(self):
        """Exporta el gráfico actual"""
        if self.current_results is None:
            messagebox.showinfo("Info", "No hay gráfico para exportar")
            return
        
        from tkinter import filedialog
        import time
        
        # Diálogo para guardar archivo
        default_name = f"temporal_analysis_{int(time.time())}.png"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=default_name,
            title="Guardar gráfico como"
        )
    
        if not filepath:  # Usuario canceló
            return
        
        self.figure.savefig(filepath, dpi=300, bbox_inches='tight')
        messagebox.showinfo("Éxito", f"Gráfico exportado como:\n{filepath}")
        self.log_result(f"\n💾 Gráfico guardado: {filepath}")
    
    def clear_editor(self):
        """Limpia el editor de código"""
        self.code_editor.delete('1.0', tk.END)
        self.log_result("", clear=True)
        self.complexity_label.config(text="Ejecuta un análisis primero")
        self.notation_label.config(text="")
        self.confidence_label.config(text="")
        self.show_empty_graph()

    def show_examples(self):
        """Muestra la ventana de ejemplos"""
        EjemplosWindow(self.root, self.load_example_code)

    def load_example_code(self, codigo):
        """Carga un ejemplo en el editor"""
        self.code_editor.delete('1.0', tk.END)
        self.code_editor.insert('1.0', codigo)
        self.log_result("📝 Ejemplo cargado. ¡Listo para analizar!", clear=True)

    def return_to_menu(self):
        """Vuelve al menú principal"""
        if self.is_analyzing:
            if not messagebox.askokcancel(
                "Volver",
                "Un análisis está en curso. ¿Seguro que deseas volver?"
            ):
                return
        # Ejecutar callback para volver al menú
        if self.return_callback:
            self.return_callback()
