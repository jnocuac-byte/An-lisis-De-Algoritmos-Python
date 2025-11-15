# sorting_gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from typing import List, Dict

from sorting_algorithms import SortingAlgorithms
from dataset_manager import DatasetManager
from sorting_analyzer import SortingAnalyzer
from tutorial_helperAdO import TutorialWindow, HelpDialog
from bar_comparison import BarComparisonWindow


class SortingAnalyzerGUI:
    """Interfaz gráfica para análisis de algoritmos de ordenamiento"""
    
    def __init__(self, root, return_callback=None):
        self.root = root
        self.return_callback = return_callback
        self.root.title("Analizador de Algoritmos de Ordenamiento")
        self.root.geometry("1500x900")
        
        self.results = None
        self.current_mode = "generate"  # "generate" o "load"
        self.is_analyzing = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if self.is_analyzing:
            if not messagebox.askokcancel("Salir", "Un análisis está en curso. ¿Seguro que desea salir?"):
                return
        # Ejecutar callback para volver al menú
        if self.return_callback:
            self.return_callback()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Panel principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ===== PANEL IZQUIERDO CON SCROLL Y ANCHO FIJO =====
        left_panel = ttk.Frame(main_frame, width=520)  # Ancho fijo
        left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(0, 5))
        left_panel.pack_propagate(False)  # Evitar que se redimensione
        
        # Canvas para scroll
        canvas = tk.Canvas(left_panel, highlightthickness=0, width=500)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Ajustar el ancho del contenido al canvas
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Asegurar que el contenido tenga el ancho del canvas
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_scroll_region)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido del panel izquierdo
        self.setup_control_panel(scrollable_frame)
        self.setup_results_panel(scrollable_frame) # type: ignore
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel para scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # ===== PANEL DERECHO (Visualización) =====
        right_panel = ttk.Frame(main_frame) 
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True) 
        self.setup_visualization_panel(right_panel) # type: ignore
    
    def setup_control_panel(self, parent):
        """Configura el panel de controles"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from theme import ModernDarkTheme
        colors = ModernDarkTheme.COLORS
        
        control_frame = ttk.LabelFrame(parent, text="⚙️  Configuración de Análisis", padding=15)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        back_btn = ttk.Button(
            control_frame,
            text="◀️ Volver al Menú Principal",
            command=self.return_to_menu,
            style='Back.TButton'
        )
        back_btn.pack(fill=tk.X, pady=(0, 10))

        # Botón de tutorial con estilo
        tutorial_btn = ttk.Button(
            control_frame,
            text="📖 Ver Tutorial Interactivo",
            command=lambda: TutorialWindow(self.root)
        )
        tutorial_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Modo de operación
        mode_header = ttk.Frame(control_frame)
        mode_header.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(mode_header, text="Modo de Operación", style='Heading.TLabel').pack(side=tk.LEFT, padx=5)
        help_btn = ttk.Button(
            mode_header,
            text="?",
            width=3,
            command=lambda: HelpDialog.show(self.root, "modo")
        )
        help_btn.pack(side=tk.RIGHT, padx=5)

        mode_frame = ttk.Frame(control_frame)       
        mode_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        self.mode_var = tk.StringVar(value="generate")
        
        ttk.Radiobutton(
            mode_frame,
            text="🔄 Generar conjuntos internamente",
            variable=self.mode_var,
            value="generate",
            command=self.on_mode_change # type: ignore
        ).pack(anchor=tk.W, pady=3)
        
        ttk.Radiobutton(
            mode_frame,
            text="📁 Cargar desde archivo .txt",
            variable=self.mode_var,
            value="load",
            command=self.on_mode_change # type: ignore
        ).pack(anchor=tk.W, pady=3)
        
        # Separator
        separator1 = ttk.Frame(control_frame, height=1)
        separator1.pack(fill=tk.X, pady=10)
        
        # Frame para generación de conjuntos
        self.generate_frame = ttk.Frame(control_frame)
        self.generate_frame.pack(fill=tk.X, pady=5)
        
        # Tamaño del conjunto
        size_frame = ttk.Frame(self.generate_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Tamaño máximo:", style='Heading.TLabel').pack(side=tk.LEFT, padx=5)
        ttk.Button(
            size_frame,
            text="?",
            width=3,
            command=lambda: HelpDialog.show(self.root, "tamano")
        ).pack(side=tk.LEFT, padx=2)

        self.size_var = tk.StringVar(value="1000")
        size_combo = ttk.Combobox(
            size_frame,
            textvariable=self.size_var,
            values=[str(s) for s in DatasetManager.PREDEFINED_SIZES] + ["Personalizado"],
            state="readonly",
            width=15
        )
        size_combo.pack(side=tk.LEFT, padx=5)
        size_combo.bind('<<ComboboxSelected>>', self.on_size_change) # type: ignore
        
        self.custom_size_frame = ttk.Frame(self.generate_frame)
        ttk.Label(self.custom_size_frame, text="Tamaño:").pack(side=tk.LEFT, padx=5)
        self.custom_size_entry = ttk.Entry(self.custom_size_frame, width=10)
        self.custom_size_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(
            self.custom_size_frame,
            text=f"(Máx: {DatasetManager.MAX_SIZE:,})",
            style='Secondary.TLabel'
        ).pack(side=tk.LEFT, padx=5)
        
        # Estado inicial
        order_frame = ttk.Frame(self.generate_frame)
        order_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(order_frame, text="Estado inicial:", style='Heading.TLabel').pack(side=tk.LEFT, padx=5)
        ttk.Button(
            order_frame,
            text="?",
            width=3,
            command=lambda: HelpDialog.show(self.root, "estado")
        ).pack(side=tk.LEFT, padx=2)

        self.order_var = tk.StringVar(value="desordenado")
        ttk.Radiobutton(
            order_frame,
            text="⬆️ Ordenado",
            variable=self.order_var,
            value="ordenado"
        ).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(
            order_frame,
            text="🔀 Desordenado",
            variable=self.order_var,
            value="desordenado"
        ).pack(side=tk.LEFT, padx=10)
        
        # Info de subconjuntos
        self.subset_info_label = ttk.Label(
            self.generate_frame,
            text="ℹ️  Se generarán 15 subconjuntos balanceados",
            style='Secondary.TLabel'
        )
        self.subset_info_label.pack(pady=5)
        
        # Frame para carga de archivo
        self.load_frame = ttk.Frame(control_frame)
        
        file_frame = ttk.Frame(self.load_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Archivo:", style='Heading.TLabel').pack(side=tk.LEFT, padx=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly", width=28).pack(
            side=tk.LEFT, padx=5, fill=tk.X, expand=True
        )
        ttk.Button(
            file_frame,
            text="📂 Examinar...",
            command=self.browse_file # type: ignore
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            self.load_frame,
            text="ℹ️  Formato: números separados por comas (ej: 5,3,8,1,9)",
            style='Secondary.TLabel'
        ).pack(pady=5)
        
        # Separator
        separator2 = ttk.Frame(control_frame, height=1)
        separator2.pack(fill=tk.X, pady=15)
        
        # Selección de algoritmos
        algo_header = ttk.Frame(control_frame)
        algo_header.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(algo_header, text="Algoritmos a Analizar", style='Heading.TLabel').pack(side=tk.LEFT, padx=5)
        ttk.Button(
            algo_header,
            text="?",
            width=3,
            command=lambda: HelpDialog.show(self.root, "algoritmos")
        ).pack(side=tk.RIGHT, padx=5)

        algo_frame = ttk.Frame(control_frame)
        algo_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10), padx=10)
        
        # Crear checkboxes en dos columnas
        self.algorithm_vars = {}
        algorithms = SortingAlgorithms.get_available_algorithms()
        
        col1 = ttk.Frame(algo_frame)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        col2 = ttk.Frame(algo_frame)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        algo_icons = {
            'Tree Sort': '🌳',
            'Bubble Sort': '🫧',
            'Selection Sort': '🎯',
            'Insertion Sort': '📌',
            'Merge Sort': '🔀',
            'Quick Sort': '⚡',
            'Counting Sort': '🔢',
            'Radix Sort': '📊'
        }
        
        for i, algo in enumerate(algorithms):
            var = tk.BooleanVar(value=False)
            self.algorithm_vars[algo] = var
            
            parent_col = col1 if i < 4 else col2
            icon = algo_icons.get(algo, '•')
            cb = ttk.Checkbutton(parent_col, text=f"{icon} {algo}", variable=var)
            cb.pack(anchor=tk.W, pady=3)
        
        # Botones de selección rápida
        select_frame = ttk.Frame(algo_frame)
        select_frame.pack(fill=tk.X, pady=(15, 0))

        # Usar grid en lugar de pack para mejor control
        select_frame.grid_columnconfigure(0, weight=1)
        select_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(
            select_frame,
            text="✓ Todos",
            command=self.select_all_algorithms
        ).grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))

        ttk.Button(
            select_frame,
            text="✗ Ninguno",
            command=self.deselect_all_algorithms
        ).grid(row=1, column=0, columnspan=2, sticky=tk.EW, padx=0, pady=(5, 0))
        
        # Separator
        separator3 = ttk.Frame(control_frame, height=1)
        separator3.pack(fill=tk.X, pady=15)
        
        # Botón de análisis con estilo de acento
        analyze_button = ttk.Button(
            control_frame,
            text="▶  INICIAR ANÁLISIS",
            command=self.start_analysis, # type: ignore
            style="Accent.TButton"
        )
        analyze_button.pack(fill=tk.X, pady=5)
        
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
        
        # Mostrar frame apropiado según el modo
        self.on_mode_change() # type: ignore
    
    def setup_results_panel(self, parent):
        """Configura el panel de resultados"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from theme import ModernDarkTheme
        colors = ModernDarkTheme.COLORS
        
        results_frame = ttk.LabelFrame(parent, text="📊  [TABLA] Resultados del Análisis", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Crear tabla con scrollbar
        table_frame = ttk.Frame(results_frame)
        table_frame.pack(fill=tk.BOTH, expand=False)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview para tabla con altura fija
        self.results_tree = ttk.Treeview(
            table_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode='browse',
            height=8
        )
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        vsb.config(command=self.results_tree.yview)
        hsb.config(command=self.results_tree.xview)
        
        # Botones de exportación
        export_frame = ttk.Frame(results_frame)
        export_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(
            export_frame,
            text="📈 Gráfica Individual",
            command=self.show_individual_graph
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            export_frame,
            text="💾 Exportar CSV",
            command=self.export_results
        ).pack(side=tk.LEFT, padx=5)

        # Botón de comparación de barras (se mostrará/ocultará según el modo)
        self.bar_comparison_button = ttk.Button(
            export_frame,
            text="📊 Comparar Barras",
            command=self.show_bar_comparison
        )
        self.bar_comparison_button.pack(side=tk.LEFT, padx=5)

    def setup_visualization_panel(self, parent):
        """Configura el panel de visualización"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from theme import ModernDarkTheme
        colors = ModernDarkTheme.COLORS
        
        viz_frame = ttk.LabelFrame(parent, text="📈  Visualización Comparativa", padding=10)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas para matplotlib
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Mostrar gráfico vacío inicial
        self.show_empty_graph()
        
        # Botón exportar gráfico
        export_btn = ttk.Button(
            viz_frame,
            text="💾 Exportar Gráfico PNG",
            command=self.export_graph
        )
        export_btn.pack(pady=10)
    
    def on_mode_change(self):
        """Maneja el cambio de modo de operación"""
        if self.mode_var.get() == "generate":
            self.generate_frame.pack(fill=tk.X, pady=5)
            self.load_frame.pack_forget()
        else:
            self.generate_frame.pack_forget()
            self.load_frame.pack(fill=tk.X, pady=5)
    
    def on_size_change(self, event=None):
        """Maneja el cambio de tamaño"""
        if self.size_var.get() == "Personalizado":
            self.custom_size_frame.pack(fill=tk.X, pady=5)
        else:
            self.custom_size_frame.pack_forget()
    
    def browse_file(self):
        """Abre diálogo para seleccionar archivo"""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de datos",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self.file_path_var.set(filepath)
    
    def select_all_algorithms(self):
        """Selecciona todos los algoritmos"""
        for var in self.algorithm_vars.values():
            var.set(True)
    
    def deselect_all_algorithms(self):
        """Deselecciona todos los algoritmos"""
        for var in self.algorithm_vars.values():
            var.set(False)
    
    def get_selected_algorithms(self) -> List[str]:
        """Retorna lista de algoritmos seleccionados"""
        return [algo for algo, var in self.algorithm_vars.items() if var.get()]
    
    def update_progress(self, percent: float, algorithm: str, size: int):
        """Actualiza la barra de progreso"""
        self.progress_bar['value'] = percent
        self.progress_label.config(
            text=f"Analizando {algorithm} con {size:,} elementos... {percent:.1f}%"
        )
        self.root.update_idletasks()
    
    def start_analysis(self):
        """Inicia el análisis en un thread separado"""
        if self.is_analyzing:
            messagebox.showwarning("Advertencia", "Ya hay un análisis en curso")
            return
        
        # Validar selección de algoritmos
        selected_algos = self.get_selected_algorithms()
        if not selected_algos:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar al menos un algoritmo"
            )
            return
        
        # Validar según el modo
        if self.mode_var.get() == "generate":
            if not self.validate_generate_mode():
                return
        else:
            if not self.validate_load_mode():
                return
        
        # Iniciar análisis en thread
        self.is_analyzing = True
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()
    
    def validate_generate_mode(self) -> bool:
        """Valida configuración del modo generación"""
        if self.size_var.get() == "Personalizado":
            try:
                size = int(self.custom_size_entry.get())
                valid, msg = DatasetManager.validate_size(size)
                if not valid:
                    messagebox.showerror("Error", msg)
                    return False
            except ValueError:
                messagebox.showerror("Error", "Tamaño inválido")
                return False
        return True
    
    def validate_load_mode(self) -> bool:
        """Valida configuración del modo carga"""
        filepath = self.file_path_var.get()
        valid, msg = DatasetManager.validate_file_path(filepath)
        if not valid:
            messagebox.showerror("Error", msg)
            return False
        return True
    
    def run_analysis(self):
        """Ejecuta el análisis (corre en thread separado)"""
        try:
            selected_algos = self.get_selected_algorithms()
            
            if self.mode_var.get() == "generate":
                self.run_generate_analysis(selected_algos)
            else:
                self.run_load_analysis(selected_algos)
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error",
                f"Error durante el análisis:\n{str(e)}"
            ))
        finally:
            self.is_analyzing = False
            self.root.after(0, self.progress_frame.pack_forget)
    
    def run_generate_analysis(self, algorithms: List[str]):
        """Ejecuta análisis con conjuntos generados"""
        # Obtener tamaño
        if self.size_var.get() == "Personalizado":
            max_size = int(self.custom_size_entry.get())
        else:
            max_size = int(self.size_var.get())
        
        # Generar datasets
        ordered = self.order_var.get() == "ordenado"
        datasets = DatasetManager.generate_subsets(max_size, ordered)
        
        # Analizar
        results = SortingAnalyzer.analyze_multiple_algorithms(
            algorithms,
            datasets,
            lambda p, a, s: self.root.after(0, lambda: self.update_progress(p, a, s))
        )
        
        self.results = results
        self.root.after(0, lambda: self.display_results(results, "multiple"))
    
    def run_load_analysis(self, algorithms: List[str]):
        """Ejecuta análisis con conjunto cargado"""
        filepath = self.file_path_var.get()
        dataset, error = DatasetManager.load_from_file(filepath)
        
        if dataset is None:
            self.root.after(0, lambda: messagebox.showerror("Error", error))
            return
        
        # Analizar
        results = SortingAnalyzer.analyze_single_dataset(
            algorithms,
            dataset,
            lambda p, a, s: self.root.after(0, lambda: self.update_progress(p, a, s))
        )
        
        self.results = results
        self.root.after(0, lambda: self.display_results(results, "single"))
    
    def display_results(self, results: Dict, mode: str):
        """Muestra los resultados en la tabla y gráfico"""
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        if mode == "multiple":
            self.display_multiple_results(results)
        else:
            self.display_single_results(results)
        
        # Mostrar gráfico comparativo
        self.plot_comparative_graph(results, mode)
        
        # Actualizar visibilidad del botón de comparación de barras
        self.update_bar_comparison_button_visibility()
        
        messagebox.showinfo("Éxito", "Análisis completado correctamente")
    
    def display_multiple_results(self, results: Dict):
        """Muestra resultados de análisis con múltiples conjuntos"""
        # Configurar columnas
        if not results:
            return
        
        # Obtener número de conjuntos
        first_algo = list(results.keys())[0]
        num_subsets = len(results[first_algo]['times']) if results[first_algo]['success'] else 0
        
        columns = ['Algoritmo', 'Complejidad'] + [f'Conj{i+1}' for i in range(num_subsets)]
        self.results_tree['columns'] = columns
        self.results_tree['show'] = 'headings'
        
        # Configurar encabezados
        self.results_tree.heading('Algoritmo', text='Algoritmo')
        self.results_tree.column('Algoritmo', width=120, minwidth=100, anchor=tk.W)
        
        self.results_tree.heading('Complejidad', text='Complejidad')
        self.results_tree.column('Complejidad', width=100, minwidth=80, anchor=tk.CENTER)

        for i in range(num_subsets):
            col_name = f'Conj{i+1}'
            self.results_tree.heading(col_name, text=col_name)
            self.results_tree.column(col_name, width=80, minwidth=70, anchor=tk.CENTER)

        # Insertar datos
        for algo_name, data in results.items():
            if data['success']:
                row = [algo_name, data['complexity']['average']]
                for time_val in data['times']:
                    row.append(SortingAnalyzer.format_time(time_val))
                self.results_tree.insert('', tk.END, values=row)
            else:
                row = [algo_name, data['complexity']['average'], "Error: " + data['errors'][0]['error']]
                self.results_tree.insert('', tk.END, values=row)
    
    def display_single_results(self, results: Dict):
        """Muestra resultados de análisis con conjunto único"""
        # Configurar columnas
        columns = ['Algoritmo', 'Complejidad', 'Tamaño', 'Tiempo']
        self.results_tree['columns'] = columns
        self.results_tree['show'] = 'headings'
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120, anchor=tk.CENTER)
        
        # Insertar datos
        for algo_name, data in results.items():
            if data['success']:
                row = [
                    algo_name,
                    data['complexity']['average'],
                    f"{data['size']:,}",
                    SortingAnalyzer.format_time(data['time'])
                ]
            else:
                row = [
                    algo_name,
                    data['complexity']['average'],
                    f"{data['size']:,}",
                    f"Error: {data['error']}"
                ]
            self.results_tree.insert('', tk.END, values=row)
    
    def plot_comparative_graph(self, results: Dict, mode: str):
        """Genera gráfico comparativo"""
        self.ax.clear()
        
        if mode == "multiple":
            self.plot_multiple_comparative(results)
        else:
            self.plot_single_comparative(results)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_multiple_comparative(self, results: Dict):
        """Gráfico comparativo para múltiples conjuntos"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from theme import ModernDarkTheme
        colors = ModernDarkTheme.get_chart_colors()
        
        for i, (algo_name, data) in enumerate(results.items()):
            if data['success'] and data['times']:
                color = colors[i % len(colors)]
                self.ax.plot(
                    data['sizes'],
                    data['times'],
                    'o-',
                    label=f"{algo_name} ({data['complexity']['average']})",
                    linewidth=2.5,
                    markersize=7,
                    color=color,
                    markeredgewidth=0,
                    alpha=0.9
                )
        
        self.ax.set_xlabel('Tamaño del conjunto (n)', fontsize=12, fontweight='600')
        self.ax.set_ylabel('Tiempo de ejecución (s)', fontsize=12, fontweight='600')
        self.ax.set_title('Comparación de Algoritmos de Ordenamiento', 
                        fontsize=14, fontweight='bold', pad=20)
        self.ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        self.ax.legend(loc='best', fontsize=9, framealpha=0.9)
        self.ax.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))
        
        # Mejorar apariencia
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def plot_single_comparative(self, results: Dict):
        """Gráfico comparativo para conjunto único"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from theme import ModernDarkTheme
        colors = ModernDarkTheme.get_chart_colors()
        
        algos = []
        times = []
        colors_list = []
        
        for i, (algo_name, data) in enumerate(results.items()):
            if data['success']:
                algos.append(f"{algo_name}\n{data['complexity']['average']}")
                times.append(data['time'])
                colors_list.append(colors[i % len(colors)])
        
        if not algos:
            self.ax.text(0.5, 0.5, 'No hay datos para mostrar', 
                        ha='center', va='center', fontsize=12,
                        transform=self.ax.transAxes)
            return
        
        bars = self.ax.bar(range(len(algos)), times, color=colors_list, 
                        alpha=0.85, edgecolor='none', width=0.7)
        
        self.ax.set_xticks(range(len(algos)))
        self.ax.set_xticklabels(algos, rotation=45, ha='right', fontsize=10)
        self.ax.set_ylabel('Tiempo de ejecución (s)', fontsize=12, fontweight='600')
        self.ax.set_title('Comparación de Tiempos de Ejecución', 
                        fontsize=14, fontweight='bold', pad=20)
        self.ax.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.5)
        
        # Agregar valores sobre las barras
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            self.ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                SortingAnalyzer.format_time(time_val),
                ha='center',
                va='bottom',
                fontsize=9,
                fontweight='bold'
            )
        
        # Mejorar apariencia
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def show_empty_graph(self):
        """Muestra gráfico vacío inicial"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from theme import ModernDarkTheme
        colors = ModernDarkTheme.COLORS
        
        self.ax.clear()
        self.ax.text(
            0.5, 0.5,
            'Ejecuta un análisis para visualizar resultados',
            ha='center',
            va='center',
            fontsize=13,
            color=colors['text_secondary'],
            transform=self.ax.transAxes,
            fontweight='500'
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor(colors['bg_tertiary'])
        self.canvas.draw()
    
    def show_individual_graph(self):
        """Muestra gráfica individual del algoritmo seleccionado"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un algoritmo de la tabla")
            return
        
        item = self.results_tree.item(selection[0])
        algo_name = item['values'][0]
        
        if algo_name not in self.results: # type: ignore
            return
        
        # Crear ventana nueva para gráfica individual
        IndividualGraphWindow(self.root, algo_name, self.results[algo_name], self.mode_var.get()) # type: ignore
        
    def export_graph(self):
        """Exporta el gráfico actual"""
        if self.results is None:
            messagebox.showinfo("Info", "No hay gráfico para exportar")
            return
        
        import time as time_module
        
        # Diálogo para guardar archivo
        default_name = f"sorting_comparison_{int(time_module.time())}.png"
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
    
    def export_results(self):
        """Exporta los resultados a archivo CSV"""
        if self.results is None:
            messagebox.showinfo("Info", "No hay resultados para exportar")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w') as f:
                mode = "multiple" if 'times' in list(self.results.values())[0] else "single"
                
                if mode == "multiple":
                    # Exportar resultados múltiples
                    first_algo = list(self.results.keys())[0]
                    num_subsets = len(self.results[first_algo]['times']) if self.results[first_algo]['success'] else 0
                    
                    header = "Algoritmo,Complejidad," + ",".join([f"Conjunto{i+1}" for i in range(num_subsets)])
                    f.write(header + "\n")
                    
                    for algo_name, data in self.results.items():
                        if data['success']:
                            times_str = ",".join([str(t) for t in data['times']])
                            f.write(f"{algo_name},{data['complexity']['average']},{times_str}\n")
                else:
                    # Exportar resultados únicos
                    f.write("Algoritmo,Complejidad,Tamaño,Tiempo(s)\n")
                    for algo_name, data in self.results.items():
                        if data['success']:
                            f.write(f"{algo_name},{data['complexity']['average']},{data['size']},{data['time']}\n")
            
            messagebox.showinfo("Éxito", f"Resultados exportados a:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")

    def show_bar_comparison(self):
        """Muestra gráfico de barras comparativo general"""
        if self.results is None:
            messagebox.showinfo("Info", "No hay resultados para mostrar")
            return
        
        BarComparisonWindow(self.root, self.results) # type: ignore

    def update_bar_comparison_button_visibility(self):
        """Actualiza la visibilidad del botón de comparación de barras"""
        if self.results is None:
            return
        
        # Ocultar el botón si estamos en modo "single" (carga desde archivo)
        # porque el gráfico principal ya es de barras
        mode = "multiple" if 'times' in list(self.results.values())[0] else "single"
        
        if mode == "single":
            self.bar_comparison_button.pack_forget()
        else:
            self.bar_comparison_button.pack(side=tk.LEFT, padx=5)

    def return_to_menu(self):
        """Vuelve al menú principal"""
        if self.is_analyzing:
            if not messagebox.askokcancel(
                "Volver",
                "Un análisis está en curso. ¿Seguro que desea volver?"
            ):
                return
        # Ejecutar callback para volver al menú
        if self.return_callback:
            self.return_callback()


class IndividualGraphWindow:
    """Ventana para mostrar gráfica individual de un algoritmo"""
    
    def __init__(self, parent, algo_name: str, data: Dict, mode: str):
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from theme import ModernDarkTheme
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"📈 Gráfica Individual - {algo_name}")
        self.window.geometry("850x650")
        
        # Aplicar tema
        self.colors = ModernDarkTheme.COLORS
        self.window.configure(bg=self.colors['bg_primary'])
        
        self.algo_name = algo_name
        self.data = data
        self.mode = mode
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Información del algoritmo
        info_frame = ttk.Frame(self.window, padding=15)
        info_frame.pack(fill=tk.X)
        
        ttk.Label(
            info_frame,
            text=f"Algoritmo: {self.algo_name}",
            style='Title.TLabel'
        ).pack(anchor=tk.W)
        
        complexity_info = self.data['complexity']
        
        # Frame para complejidades con colores
        complexity_frame = tk.Frame(info_frame, bg=self.colors['bg_primary'])
        complexity_frame.pack(anchor=tk.W, pady=8)
        
        complexities = [
            ("Mejor caso:", complexity_info['best'], self.colors['success']),
            ("Caso promedio:", complexity_info['average'], self.colors['accent']),
            ("Peor caso:", complexity_info['worst'], self.colors['error'])
        ]
        
        for label, value, color in complexities:
            frame = tk.Frame(complexity_frame, bg=self.colors['bg_primary'])
            frame.pack(side=tk.LEFT, padx=10)
            
            tk.Label(frame, text=label, 
                    font=('Segoe UI', 9),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['bg_primary']).pack(side=tk.LEFT)
            
            tk.Label(frame, text=value,
                    font=('Segoe UI', 9, 'bold'),
                    fg=color,
                    bg=self.colors['bg_primary']).pack(side=tk.LEFT, padx=5)
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        canvas = FigureCanvasTkAgg(fig, self.window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        chart_colors = self.colors['chart_2']  # Color morado
        
        if self.mode == "generate" and self.data['success']:
            # Gráfico de líneas para múltiples conjuntos
            ax.plot(
                self.data['sizes'],
                self.data['times'],
                'o-',
                linewidth=2.5,
                markersize=8,
                color=chart_colors,
                markeredgewidth=0,
                alpha=0.9,
                label=f"{self.algo_name}"
            )
            ax.fill_between(self.data['sizes'], self.data['times'], 
                           alpha=0.2, color=chart_colors)
            ax.set_xlabel('Tamaño del conjunto (n)', fontsize=12, fontweight='600')
            ax.set_ylabel('Tiempo de ejecución (s)', fontsize=12, fontweight='600')
            ax.set_title(f'{self.algo_name} - Análisis de Rendimiento', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
            ax.legend(fontsize=10)
            ax.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))
            
        elif self.mode == "load" and self.data['success']:
            # Gráfico de barras para conjunto único
            bar = ax.bar(
                [0],
                [self.data['time']],
                color=chart_colors,
                alpha=0.85,
                edgecolor='none',
                width=0.6
            )
            
            ax.set_xticks([0])
            ax.set_xticklabels([self.algo_name], fontsize=11, fontweight='600')
            ax.set_ylabel('Tiempo de ejecución (s)', fontsize=12, fontweight='600')
            ax.set_title(f'{self.algo_name} - Resultado Individual', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.5)
            ax.set_axisbelow(True)
            
            # Valor sobre la barra
            height = bar[0].get_height()
            ax.text(
                0,
                height,
                SortingAnalyzer.format_time(self.data['time']),
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold'
            )
            
            # Información adicional
            info_text = f"Tamaño: {self.data['size']:,} elementos\nComplejidad: {complexity_info['average']}"
            ax.text(
                0,
                height * 0.5,
                info_text,
                ha='center',
                va='center',
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.8', 
                         facecolor=self.colors['bg_secondary'], 
                         alpha=0.9, 
                         edgecolor=self.colors['border'])
            )
            
        else:
            # Manejo de errores
            if self.data.get('error'):
                ax.text(0.5, 0.5,
                    f"❌ Error: {self.data['error']}",
                    ha='center', va='center', fontsize=12, 
                    color=self.colors['error'],
                    transform=ax.transAxes,
                    fontweight='500')
            else:
                ax.text(0.5, 0.5,
                    "⚠️ No hay datos disponibles",
                    ha='center', va='center', fontsize=12, 
                    color=self.colors['text_secondary'],
                    transform=ax.transAxes,
                    fontweight='500')
            
            ax.set_xticks([])
            ax.set_yticks([])
        
        # Mejorar apariencia
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout()
        canvas.draw()
        
        # Botón cerrar
        close_btn = ttk.Button(
            self.window,
            text="✕ Cerrar",
            command=self.window.destroy
        )
        close_btn.pack(pady=15)

        # Frame de botones
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=15)
        
        # Botón exportar
        ttk.Button(
            button_frame,
            text="💾 Exportar PNG",
            command=self.export_graph
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón cerrar
        ttk.Button(
            button_frame,
            text="✕ Cerrar",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def export_graph(self):
        """Exporta el gráfico individual"""
        from tkinter import filedialog
        import time
        
        default_name = f"{self.algo_name.replace(' ', '_')}_{int(time.time())}.png"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=default_name,
            title="Guardar gráfico como"
        )
        
        if not filepath:
            return
        
        # Obtener la figura del gráfico
        canvas_widget = self.window.winfo_children()[1]  # El canvas está en índice 1
        fig = canvas_widget.figure # type: ignore
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        messagebox.showinfo("Éxito", f"Gráfico exportado como:\n{filepath}")