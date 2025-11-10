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


class TemporalAnalyzerGUI:
    """Interfaz gráfica principal"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Complejidad Temporal")
        self.root.geometry("1400x850")
        
        self.current_results = None
        self.detected_complexity = None
        self.is_analyzing = False
        
        # Configuraciones de ejecución
        self.predefined_configs = [700, 1500, 3000]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # ===== Panel Izquierdo =====
        editor_label = ttk.Label(left_frame, text="Código Python:", font=("Arial", 10, "bold"))
        editor_label.pack(pady=(5, 2))
        
        self.code_editor = scrolledtext.ScrolledText(
            left_frame, 
            height=15, 
            font=("Courier", 10),
            wrap=tk.WORD
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
        
        control_frame = ttk.LabelFrame(left_frame, text="Configuración", padding=10)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Configuración de ejecuciones
        exec_frame = ttk.LabelFrame(control_frame, text="Número de Ejecuciones", padding=10)
        exec_frame.pack(fill=tk.X, pady=5)
        
        self.exec_mode_var = tk.StringVar(value="predefined")
        
        ttk.Radiobutton(
            exec_frame,
            text="Estándar (700, 1500, 3000)",
            variable=self.exec_mode_var,
            value="predefined",
            command=self.on_exec_mode_change
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            exec_frame,
            text="Personalizado",
            variable=self.exec_mode_var,
            value="custom",
            command=self.on_exec_mode_change
        ).pack(anchor=tk.W, pady=2)
        
        # Frame para ejecuciones personalizadas
        self.custom_exec_frame = ttk.Frame(exec_frame)
        
        custom_grid = ttk.Frame(self.custom_exec_frame)
        custom_grid.pack(fill=tk.X, pady=5)
        
        ttk.Label(custom_grid, text="Config 1:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.custom_exec1 = ttk.Entry(custom_grid, width=10)
        self.custom_exec1.grid(row=0, column=1, padx=5, pady=2)
        self.custom_exec1.insert(0, "3000")
        
        ttk.Label(custom_grid, text="Config 2:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.custom_exec2 = ttk.Entry(custom_grid, width=10)
        self.custom_exec2.grid(row=1, column=1, padx=5, pady=2)
        self.custom_exec2.insert(0, "7000")
        
        ttk.Label(custom_grid, text="Config 3:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.custom_exec3 = ttk.Entry(custom_grid, width=10)
        self.custom_exec3.grid(row=2, column=1, padx=5, pady=2)
        self.custom_exec3.insert(0, "15000")
        
        ttk.Label(
            self.custom_exec_frame,
            text="Límite máximo: 1,000,000 ejecuciones",
            foreground="gray",
            font=("Arial", 8)
        ).pack(pady=5)
        
        ttk.Label(
            exec_frame,
            text="Se tomarán 20 puntos muestreados de cada configuración",
            foreground="#555",
            font=("Arial", 8)
        ).pack(pady=5)
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame, 
            text="▶ Analizar", 
            command=self.analyze_code
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="🔍 Detectar Complejidad", 
            command=self.detect_complexity_only
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="✓ Verificar Sintaxis", 
            command=self.check_syntax
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="🗑 Limpiar", 
            command=self.clear_editor
        ).pack(side=tk.LEFT, padx=5)
        
        # Barra de progreso
        self.progress_frame = ttk.Frame(control_frame)
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="",
            font=("Arial", 8)
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        results_label = ttk.Label(left_frame, text="Resultados:", font=("Arial", 10, "bold"))
        results_label.pack(pady=(5, 2))
        
        self.results_text = scrolledtext.ScrolledText(
            left_frame, 
            height=8, 
            font=("Courier", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ===== Panel Derecho =====
        complexity_frame = ttk.LabelFrame(right_frame, text="Complejidad Detectada", padding=10)
        complexity_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.complexity_label = ttk.Label(
            complexity_frame, 
            text="Ejecuta un análisis primero", 
            font=("Arial", 14, "bold"),
            foreground="#2E86AB"
        )
        self.complexity_label.pack(pady=5)
        
        self.notation_label = ttk.Label(
            complexity_frame, 
            text="", 
            font=("Courier", 11),
            foreground="#555"
        )
        self.notation_label.pack(pady=5)
        
        self.confidence_label = ttk.Label(
            complexity_frame, 
            text="", 
            font=("Arial", 9),
            foreground="#888"
        )
        self.confidence_label.pack()
        
        graph_label = ttk.Label(right_frame, text="Visualización Temporal", font=("Arial", 12, "bold"))
        graph_label.pack(pady=10)
        
        # Crear figura con 3 subplots
        self.figure, self.axes = plt.subplots(1, 3, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        export_btn = ttk.Button(
            right_frame, 
            text="💾 Exportar Gráfico", 
            command=self.export_graph
        )
        export_btn.pack(pady=5)
        
        self.show_empty_graph()
        self.on_exec_mode_change()
    
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
        # Limpiar axes
        for ax in self.axes:
            ax.clear()
        
        colors = ['#2E86AB', '#A23B72', '#F18F01']
        
        for idx, config in enumerate(configs):
            data = results[config]
            ax = self.axes[idx]
            
            # Graficar línea constante de tiempos muestreados
            ax.plot(
                data['sampled_indices'],
                data['sampled_times'],
                'o-',
                linewidth=2,
                markersize=6,
                color=colors[idx],
                label=f"{config:,} ejecuciones"
            )
            
            # Línea promedio
            avg_line = np.mean(data['sampled_times'])
            ax.axhline(
                y=avg_line,
                color=colors[idx],
                linestyle='--',
                linewidth=1,
                alpha=0.5
            )
            
            ax.set_xlabel('Ejecución #', fontsize=9, fontweight='bold')
            ax.set_ylabel('Tiempo (s)', fontsize=9, fontweight='bold')
            ax.set_title(f'{config:,} ejecuciones', fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
            
            # Agregar texto con tiempo promedio
            ax.text(
                0.95, 0.95,
                f'Promedio:\n{ComplexityAnalyzer.format_time(data["avg_time"])}',
                transform=ax.transAxes,
                fontsize=8,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def show_empty_graph(self):
        """Muestra gráficos vacíos iniciales"""
        for ax in self.axes:
            ax.clear()
            ax.text(
                0.5, 0.5,
                'Ejecuta un\nanálisis primero',
                ha='center',
                va='center',
                fontsize=10,
                color='gray',
                transform=ax.transAxes
            )
            ax.set_xticks([])
            ax.set_yticks([])
        self.canvas.draw()
    
    def export_graph(self):
        """Exporta el gráfico actual"""
        if self.current_results is None:
            messagebox.showinfo("Info", "No hay gráfico para exportar")
            return
        
        filename = f"temporal_analysis_{int(time.time())}.png"
        self.figure.savefig(filename, dpi=300, bbox_inches='tight')
        messagebox.showinfo("Éxito", f"Gráfico exportado como:\n{filename}")
        self.log_result(f"\n💾 Gráfico guardado: {filename}")
    
    def clear_editor(self):
        """Limpia el editor de código"""
        self.code_editor.delete('1.0', tk.END)
        self.log_result("", clear=True)
        self.complexity_label.config(text="Ejecuta un análisis primero")
        self.notation_label.config(text="")
        self.confidence_label.config(text="")
        self.show_empty_graph()