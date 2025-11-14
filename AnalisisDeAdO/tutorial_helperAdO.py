"""
Módulo de ayuda y tutoriales para el analizador de algoritmos de ordenamiento
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Importar tema desde la raíz
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import ModernDarkTheme


class TutorialWindow:
    """Ventana de tutorial principal"""
    
    def __init__(self, parent):
        self.colors = ModernDarkTheme.COLORS
        
        self.window = tk.Toplevel(parent)
        self.window.title("📚 Tutorial - Analizador de Algoritmos de Ordenamiento")
        self.window.geometry("750x600")
        self.window.resizable(True, True)
        self.window.configure(bg=self.colors['bg_primary'])
        self.window.configure(bg=self.colors['bg_primary'])
        
        # Centrar ventana
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crea los widgets del tutorial"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title = ttk.Label(
            scrollable_frame,
            text="🚀 Bienvenido al Analizador de Algoritmos de Ordenamiento",
            style='Title.TLabel'
        )
        title.pack(pady=(0, 20))
        
        # Secciones
        sections = [
            {
                "title": "📋 ¿Qué hace este programa?",
                "content": "Analiza y compara el rendimiento de diferentes algoritmos de ordenamiento. "
                          "Puedes generar conjuntos de datos automáticamente o cargar tus propios datos "
                          "para ver cuál algoritmo es más eficiente."
            },
            {
                "title": "🎯 Modo de Operación",
                "content": "• Generar conjuntos internamente: El programa crea 15 subconjuntos balanceados "
                          "desde tamaños pequeños hasta el máximo que especifiques.\n"
                          "• Cargar desde archivo .txt: Ingresa tu propio conjunto de datos en formato CSV.\n"
                          "Ejemplo: 42,17,93,8,56,31,205"
            },
            {
                "title": "📊 Tamaño Máximo",
                "content": "Define cuántos elementos tendrá tu conjunto de datos (1 a 1,000,000).\n"
                          "Recomendaciones:\n"
                          "• 1,000-10,000: Análisis rápido, todos los algoritmos\n"
                          "• 10,000-50,000: Evitar algoritmos O(n²)\n"
                          "• 50,000-100,000: Solo algoritmos eficientes (Merge, Quick, Radix)\n"
                          "• 100,000+: Análisis exhaustivo con algoritmos O(n log n)"
            },
            {
                "title": "🔄 Estado Inicial",
                "content": "• Ordenado: Datos ya ordenados (mejor caso para algunos algoritmos)\n"
                          "• Desordenado: Datos aleatorios (caso promedio)"
            },
            {
                "title": "⚙️ Algoritmos Disponibles",
                "content": "🌳 Tree Sort: O(n log n) promedio - Usa árboles binarios de búsqueda\n"
                          "🫧 Bubble Sort: O(n²) - Simple pero lento\n"
                          "🎯 Selection Sort: O(n²) - Menos intercambios\n"
                          "📌 Insertion Sort: O(n²) - Eficiente con datos casi ordenados\n"
                          "🔀 Merge Sort: O(n log n) - Consistente, usa memoria extra\n"
                          "⚡ Quick Sort: O(n log n) - Muy rápido en la práctica\n"
                          "🔢 Counting Sort: O(n+k) - Rápido para rangos pequeños\n"
                          "📊 Radix Sort: O(d(n+k)) - Excelente para números enteros"
            },
            {
                "title": "📈 Resultados",
                "content": "• Tabla comparativa: Muestra tiempos de ejecución por algoritmo\n"
                          "• Gráfico de líneas: Visualiza crecimiento temporal (modo generar)\n"
                          "• Gráfico de barras: Compara tiempos directamente (modo cargar)\n"
                          "• Gráficos individuales: Análisis detallado por algoritmo\n"
                          "• Exportación: Guarda resultados en CSV o gráficos en PNG"
            },
            {
                "title": "💡 Consejos",
                "content": "• Usa tamaños pequeños para pruebas rápidas\n"
                          "• Para conjuntos grandes (>10,000), evita Bubble, Selection e Insertion Sort\n"
                          "• El gráfico de líneas muestra claramente la complejidad temporal\n"
                          "• Usa botones '?' en cada sección para ayuda específica\n"
                          "• Exporta resultados para análisis posteriores o reportes"
            }
        ]
        
        for section in sections:
            self.create_section(scrollable_frame, section["title"], section["content"])
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        ttk.Button(
            self.window,
            text="Entendido",
            command=self.window.destroy
        ).pack(pady=10)
    
    def create_section(self, parent, title, content):
        """Crea una sección del tutorial"""
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        label = ttk.Label(
            frame,
            text=content,
            wraplength=650,
            justify=tk.LEFT
        )
        label.pack()


class HelpDialog:
    """Diálogos de ayuda contextual"""
    
    HELP_TEXTS = {
        "modo": {
            "title": "Modo de Operación",
            "content": "Selecciona cómo proporcionar los datos:\n\n"
                      "🔸 Generar conjuntos internamente:\n"
                      "El programa creará automáticamente 15 subconjuntos balanceados "
                      "desde tamaños pequeños hasta el máximo especificado. "
                      "Esto permite analizar cómo crece el tiempo de ejecución.\n\n"
                      "🔸 Cargar desde archivo .txt:\n"
                      "Carga tu propio conjunto de datos desde un archivo.\n"
                      "Formato: números separados por comas\n"
                      "Ejemplo: 42, 17, 93, 8, 56, 31\n\n"
                      "⚠️ Nota: Al cargar datos, el tamaño se determina por el archivo."
        },
        "tamano": {
            "title": "Tamaño Máximo",
            "content": "Define la cantidad de elementos en tu conjunto de datos.\n\n"
                      "🔹 Rango: 1 a 1,000,000 elementos\n\n"
                      "🔹 Tamaños predefinidos:\n"
                      "  • 1,000: Pruebas rápidas\n"
                      "  • 5,000: Análisis estándar\n"
                      "  • 10,000: Análisis detallado\n"
                      "  • 50,000: Análisis avanzado\n"
                      "  • 100,000: Análisis exhaustivo\n"
                      "  • Personalizado: Define tu propio tamaño\n\n"
                      "⏱️ A mayor tamaño, más tiempo de ejecución.\n\n"
                      "⚠️ Para tamaños >10,000, evita algoritmos O(n²)."
        },
        "estado": {
            "title": "Estado Inicial",
            "content": "Determina cómo se organizan los datos generados:\n\n"
                      "🔸 Ordenado:\n"
                      "Números ya ordenados de menor a mayor.\n"
                      "Representa el MEJOR CASO para algunos algoritmos.\n"
                      "Insertion Sort es muy rápido con datos ordenados.\n\n"
                      "🔸 Desordenado:\n"
                      "Números en orden completamente aleatorio.\n"
                      "Representa el CASO PROMEDIO.\n"
                      "Más realista para la mayoría de aplicaciones.\n\n"
                      "💡 Prueba ambos para ver la diferencia de rendimiento."
        },
        "algoritmos": {
            "title": "Selección de Algoritmos",
            "content": "Elige qué algoritmos analizar:\n\n"
                      "🌳 Tree Sort - O(n log n) promedio\n"
                      "   Usa árboles binarios de búsqueda\n\n"
                      "🫧 Bubble Sort - O(n²)\n"
                      "   Simple pero lento para conjuntos grandes\n\n"
                      "🎯 Selection Sort - O(n²)\n"
                      "   Realiza menos intercambios que Bubble\n\n"
                      "📌 Insertion Sort - O(n²)\n"
                      "   Muy eficiente con datos casi ordenados\n\n"
                      "🔀 Merge Sort - O(n log n)\n"
                      "   Consistente, requiere memoria extra\n\n"
                      "⚡ Quick Sort - O(n log n) promedio\n"
                      "   Muy rápido en la práctica\n\n"
                      "🔢 Counting Sort - O(n+k)\n"
                      "   Excelente para números con rango limitado\n\n"
                      "📊 Radix Sort - O(d(n+k))\n"
                      "   Muy eficiente para números enteros\n\n"
                      "💡 Puedes seleccionar varios para comparar."
        }
    }
    
    @staticmethod
    def show(parent, help_key):
        """Muestra diálogo de ayuda"""
        colors = ModernDarkTheme.COLORS
        
        if help_key not in HelpDialog.HELP_TEXTS:
            return
        
        help_data = HelpDialog.HELP_TEXTS[help_key]
        
        dialog = tk.Toplevel(parent)
        dialog.title(f"Ayuda - {help_data['title']}")
        dialog.geometry("550x450")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.configure(bg=colors['bg_primary'])
        
        # Centrar
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(
            main_frame,
            text=f"❓ {help_data['title']}",
            style='Title.TLabel'
        )
        title.pack(pady=(0, 15))
        
        # Texto con scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            padx=10,
            pady=10,
            bg=colors['bg_tertiary'],
            fg=colors['text_primary'],
            relief='flat'
        )
        scrollbar = ttk.Scrollbar(text_frame, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.insert('1.0', help_data['content'])
        text.configure(state='disabled')
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón cerrar
        ttk.Button(
            main_frame,
            text="Cerrar",
            command=dialog.destroy
        ).pack(pady=(10, 0))