# gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
from typing import List, Dict, Any

from complexity_detector import ComplexityDetector
from dataset_generator import DatasetGenerator
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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_ui()

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            self.root.quit()
            self.root.destroy()
    
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
        
        example_code = """# Ejemplo Merge Sort con dataset:
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            
    return arr

arreglo_ejemplo = arr
arreglo_ordenado = merge_sort(arreglo_ejemplo)

print(arreglo_ordenado)"""
        self.code_editor.insert('1.0', example_code)
        
        control_frame = ttk.LabelFrame(left_frame, text="Configuración", padding=10)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        mode_frame = ttk.Frame(control_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="Modo:").pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="with_dataset")
        ttk.Radiobutton(
            mode_frame, 
            text="Con Dataset", 
            variable=self.mode_var, 
            value="with_dataset",
            command=self.on_mode_change
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            mode_frame, 
            text="Sin Dataset", 
            variable=self.mode_var, 
            value="without_dataset",
            command=self.on_mode_change
        ).pack(side=tk.LEFT, padx=5)
        
        self.dataset_frame = ttk.Frame(control_frame)
        self.dataset_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.dataset_frame, text="Tipo de dato:").pack(side=tk.LEFT, padx=5)
        self.data_type_var = tk.StringVar(value="int")
        ttk.Combobox(
            self.dataset_frame, 
            textvariable=self.data_type_var,
            values=["int", "float", "string"],
            state="readonly",
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.dataset_frame, text="Variable: arr, conjunto, data").pack(side=tk.LEFT, padx=10)
        
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
        
        self.figure, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        export_btn = ttk.Button(
            right_frame, 
            text="💾 Exportar Gráfico", 
            command=self.export_graph
        )
        export_btn.pack(pady=5)
        
        self.show_empty_graph()
    
    def on_mode_change(self):
        """Maneja el cambio de modo"""
        if self.mode_var.get() == "with_dataset":
            self.dataset_frame.pack(fill=tk.X, pady=5)
        else:
            self.dataset_frame.pack_forget()
    
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
    
    def analyze_code(self):
        """Analiza el código según el modo seleccionado"""
        code = self.code_editor.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "Por favor ingresa código para analizar")
            return
        
        syntax_result = CodeExecutor.test_code_syntax(code)
        if not syntax_result['valid']:
            messagebox.showerror("Error de Sintaxis", f"✗ Error:\n{syntax_result['error']}")
            self.log_result(f"✗ Error de sintaxis:\n{syntax_result['error']}", clear=True)
            return
        
        self.log_result("🔄 Analizando código...", clear=True)
        
        # Detectar complejidad primero
        detector = ComplexityDetector(code)
        complexity_result = detector.analyze()
        self.detected_complexity = complexity_result
        self.update_complexity_display(complexity_result)
        
        self.root.update()
        
        mode = self.mode_var.get()
        
        try:
            if mode == "with_dataset":
                self.analyze_with_dataset(code)
            else:
                self.analyze_without_dataset(code)
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis:\n{str(e)}")
            self.log_result(f"✗ Error: {str(e)}")
    
    def analyze_with_dataset(self, code: str):
        """Analiza código con datasets escalables"""
        data_type = self.data_type_var.get()
        
        self.log_result(f"📊 Tipo de dato: {data_type}")
        self.log_result("📦 Cargando/generando datasets...")
        
        datasets = DatasetGenerator.get_or_create_dataset(data_type)
        self.log_result(f"✓ {len(datasets)} datasets listos")
        
        self.log_result("⏱ Midiendo tiempos de ejecución...")
        results = ComplexityAnalyzer.analyze_with_dataset(code, datasets)
        
        if results['errors']:
            error_info = results['errors'][0]
            self.log_result(f"\n✗ Error en dataset #{error_info['dataset_index']} (tamaño {error_info['size']}):")
            self.log_result(error_info['error'])
            messagebox.showerror("Error de Ejecución", f"Error al ejecutar el código:\n{error_info['error']}")
            return
        
        if not results['sizes']:
            self.log_result("✗ No se pudieron obtener resultados")
            return
        
        self.current_results = results
        
        self.log_result(f"\n✓ Análisis completado:")
        self.log_result(f"  • Datasets procesados: {len(results['sizes'])}")
        self.log_result(f"  • Tamaño mínimo: {min(results['sizes'])}")
        self.log_result(f"  • Tamaño máximo: {max(results['sizes'])}")
        self.log_result(f"  • Tiempo mínimo: {min(results['times']):.6f}s")
        self.log_result(f"  • Tiempo máximo: {max(results['times']):.6f}s")
        
        self.plot_complexity_graph(results['sizes'], results['times'])
    
    def analyze_without_dataset(self, code: str):
        """Analiza código sin datasets (tiempo promedio)"""
        self.log_result("⏱ Ejecutando código 10 veces...")
        
        results = ComplexityAnalyzer.analyze_without_dataset(code, iterations=10)
        
        if not results['success']:
            self.log_result(f"\n✗ Error al ejecutar el código:")
            self.log_result(results['error'])
            messagebox.showerror("Error de Ejecución", f"Error:\n{results['error']}")
            return
        
        self.log_result(f"\n✓ Análisis completado:")
        self.log_result(f"  • Tiempo promedio: {results['avg_time']:.6f}s")
        self.log_result(f"  • Desviación estándar: {results['std_time']:.6f}s")
        self.log_result(f"  • Tiempo mínimo: {min(results['times']):.6f}s")
        self.log_result(f"  • Tiempo máximo: {max(results['times']):.6f}s")
        
        self.plot_execution_times(results['times'])
    
    def plot_complexity_graph(self, sizes: List[int], times: List[float]):
        """Grafica la complejidad temporal"""
        self.ax.clear()
        
        self.ax.plot(sizes, times, 'o-', linewidth=2, markersize=8, color='#2E86AB', label='Tiempo medido')
        self.ax.fill_between(sizes, times, alpha=0.3, color='#2E86AB')
        
        self.ax.set_xlabel('Tamaño de entrada (n)', fontsize=11, fontweight='bold')
        self.ax.set_ylabel('Tiempo de ejecución (s)', fontsize=11, fontweight='bold')
        
        title = 'Análisis de Complejidad Temporal'
        if self.detected_complexity:
            title += f"\n{self.detected_complexity['complexity']}"
        self.ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
        
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.legend(loc='upper left')
        self.ax.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_execution_times(self, times: List[float]):
        """Grafica los tiempos de ejecución múltiples"""
        self.ax.clear()
        
        iterations = list(range(1, len(times) + 1))
        avg_time = np.mean(times)
        
        self.ax.plot(iterations, times, 'o-', linewidth=2, markersize=8, color='#A23B72', label='Tiempo medido')
        self.ax.axhline(y=avg_time, color='#F18F01', linestyle='--', linewidth=2, label=f'Promedio: {avg_time:.6f}s') # type: ignore
        
        self.ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
        self.ax.set_ylabel('Tiempo de ejecución (s)', fontsize=11, fontweight='bold')
        
        title = 'Tiempos de Ejecución (10 iteraciones)'
        if self.detected_complexity:
            title += f"\n{self.detected_complexity['complexity']}"
        self.ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
        
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.legend(loc='upper right')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def show_empty_graph(self):
        """Muestra un gráfico vacío inicial"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Ejecuta un análisis para ver resultados', 
                    ha='center', va='center', fontsize=12, color='gray',
                    transform=self.ax.transAxes)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
    
    def export_graph(self):
        """Exporta el gráfico actual"""
        if self.current_results is None and self.detected_complexity is None:
            messagebox.showinfo("Info", "No hay gráfico para exportar. Ejecuta un análisis primero.")
            return
        
        filename = f"complexity_graph_{int(time.time())}.png"
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