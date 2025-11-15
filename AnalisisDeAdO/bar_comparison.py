# bar_comparison.py
"""
Módulo para gráfico de barras comparativo general
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict

class BarComparisonWindow:
    """Ventana para mostrar gráfico de barras comparativo"""
    
    def __init__(self, parent, results: Dict):
        from theme import ModernDarkTheme
        
        self.window = tk.Toplevel(parent)
        self.window.title("📊 Comparación General - Gráfico de Barras")
        self.window.geometry("1100x750")  # Aumentado de 1000x650 a 1100x750
        
        # Aplicar tema
        self.colors = ModernDarkTheme.COLORS
        self.window.configure(bg=self.colors['bg_primary'])
        
        self.results = results
        
        # Centrar ventana
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crea los widgets de la ventana"""
        # Frame principal con scrollbar
        main_container = ttk.Frame(self.window)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar para contenido scrolleable
        canvas = tk.Canvas(main_container, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame superior
        header = ttk.Frame(scrollable_frame, padding=15)
        header.pack(fill=tk.X)
        
        ttk.Label(
            header,
            text="📊  Comparación de Rendimiento - Todos los Algoritmos",
            style='Title.TLabel'
        ).pack()
        
        # Frame para gráfico
        chart_frame = ttk.Frame(scrollable_frame, padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_bar_chart(chart_frame)
        
        # Frame de estadísticas con padding adicional
        stats_frame = ttk.LabelFrame(scrollable_frame, text="📈  Estadísticas", padding=20)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_statistics(stats_frame)
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel para scroll
        def _on_mousewheel(event):
            scroll_units = int(-1 * (event.delta / 120)) 
            canvas.yview_scroll(scroll_units, "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        self.window.bind("<MouseWheel>", _on_mousewheel)

        canvas.bind('<Button-4>', lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind('<Button-5>', lambda e: canvas.yview_scroll(1, "units"))
        self.window.bind('<Button-4>', lambda e: canvas.yview_scroll(-1, "units"))
        self.window.bind('<Button-5>', lambda e: canvas.yview_scroll(1, "units"))

        canvas.bind('<Enter>', lambda e: canvas.focus_set())
        
        # Frame para botón cerrar (fuera del scroll)
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="✕ Cerrar",
            command=self.window.destroy
        ).pack()
    
    def create_bar_chart(self, parent):
        """Crea el gráfico de barras"""
        from theme import ModernDarkTheme
        
        fig, ax = plt.subplots(figsize=(10, 5.5))  # Aumentado altura de 5 a 5.5
        
        # Preparar datos
        algorithms = []
        avg_times = []
        colors = ModernDarkTheme.get_chart_colors()
        
        for algo_name, data in self.results.items():
            if data['success']:
                algorithms.append(algo_name)
                
                # Calcular tiempo promedio
                if 'times' in data and data['times']:
                    avg_time = sum(data['times']) / len(data['times'])
                elif 'time' in data:
                    avg_time = data['time']
                else:
                    continue
                
                avg_times.append(avg_time)
        
        # Crear barras
        bar_colors = colors[:len(algorithms)]
        bars = ax.bar(range(len(algorithms)), avg_times, color=bar_colors, 
                     alpha=0.85, edgecolor='none', width=0.7)
        
        # Configurar ejes
        ax.set_xlabel('Algoritmos', fontsize=12, fontweight='600')
        ax.set_ylabel('Tiempo Promedio (s)', fontsize=12, fontweight='600')
        ax.set_title('Comparación de Rendimiento de Algoritmos', 
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.set_xticks(range(len(algorithms)))
        ax.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=10)
        
        ax.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Mejorar apariencia
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Añadir valores sobre barras
        for bar, time in zip(bars, avg_times):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                self.format_time(time),
                ha='center',
                va='bottom',
                fontsize=9,
                fontweight='bold'
            )
        
        fig.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_statistics(self, parent):
        """Crea panel de estadísticas"""
        # Calcular tiempos promedio
        algo_times = {}
        for algo_name, data in self.results.items():
            if data['success']:
                if 'times' in data and data['times']:
                    algo_times[algo_name] = sum(data['times']) / len(data['times'])
                elif 'time' in data:
                    algo_times[algo_name] = data['time']
        
        if not algo_times:
            ttk.Label(parent, text="No hay datos para estadísticas").pack()
            return
        
        fastest = min(algo_times, key=algo_times.get) # type: ignore
        slowest = max(algo_times, key=algo_times.get) # type: ignore
        avg_all = sum(algo_times.values()) / len(algo_times)
        
        # Grid de estadísticas con colores del tema
        stats_grid = ttk.Frame(parent)
        stats_grid.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Crear labels con colores y más espacio
        stats_data = [
            ("🏆 Más Rápido:", f"{fastest} ({self.format_time(algo_times[fastest])})", self.colors['success']),
            ("🐌 Más Lento:", f"{slowest} ({self.format_time(algo_times[slowest])})", self.colors['error']),
            ("⏱️  Promedio General:", f"{self.format_time(avg_all)}", self.colors['accent']),
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            frame = ttk.Frame(stats_grid)
            frame.grid(row=i, column=0, sticky=tk.W, pady=8)  # Aumentado pady de 5 a 8
            
            ttk.Label(frame, text=label, font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)  # Aumentado de 10 a 11
            
            value_label = tk.Label(frame, text=value, 
                                  font=('Segoe UI', 11),  # Aumentado de 10 a 11
                                  fg=color, bg=self.colors['bg_secondary'])
            value_label.pack(side=tk.LEFT, padx=15)  # Aumentado de 10 a 15
        
        # Diferencia
        diff = algo_times[slowest] - algo_times[fastest]
        if algo_times[fastest] > 0:
            factor = algo_times[slowest] / algo_times[fastest]
            diff_frame = ttk.Frame(stats_grid)
            diff_frame.grid(row=3, column=0, sticky=tk.W, pady=8)  # Aumentado pady de 5 a 8
            
            ttk.Label(diff_frame, text="📊 Diferencia:", 
                     font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)  # Aumentado de 10 a 11
            
            diff_label = tk.Label(diff_frame, 
                                 text=f"{self.format_time(diff)} ({factor:.1f}x más lento)",
                                 font=('Segoe UI', 11),  # Aumentado de 10 a 11
                                 fg=self.colors['warning'], 
                                 bg=self.colors['bg_secondary'])
            diff_label.pack(side=tk.LEFT, padx=15)  # Aumentado de 10 a 15
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Formatea el tiempo"""
        if seconds < 0.001:
            return f"{seconds * 1000000:.2f} µs"
        elif seconds < 1:
            return f"{seconds * 1000:.2f} ms"
        else:
            return f"{seconds:.4f} s"