# tutorial_helper.py
"""
Módulo de ayuda y tutoriales para el analizador de complejidad temporal
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
        self.window.title("📚 Tutorial - Analizador de Complejidad Temporal")
        self.window.geometry("750x600")
        self.window.resizable(True, True)
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

        # Función para manejar el scroll de la rueda del mouse
        def on_mouse_wheel(event):
            # Forzamos el scroll en el canvas.
            if event.delta: # Windows/macOS
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif event.num == 4: # Linux (Scroll Up)
                canvas.yview_scroll(-1, "units")
            elif event.num == 5: # Linux (Scroll Down)
                canvas.yview_scroll(1, "units")
            return "break" # Detiene la propagación del evento

        # Función que vincula el evento a todos los widgets hijos
        def bind_all_children(widget):
            # Vincula la función de scroll a todos los widgets contenidos en el frame
            widget.bind("<MouseWheel>", on_mouse_wheel)
            widget.bind("<Button-4>", on_mouse_wheel)
            widget.bind("<Button-5>", on_mouse_wheel)
            for child in widget.winfo_children():
                bind_all_children(child)
        
        # Vinculamos la función al scrollable_frame y a todos sus hijos
        bind_all_children(scrollable_frame)
        
        # También vinculamos al canvas y la ventana principal por si acaso
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        self.window.bind("<MouseWheel>", on_mouse_wheel)
        self.window.bind("<Button-4>", on_mouse_wheel)
        self.window.bind("<Button-5>", on_mouse_wheel)
        
        # Título
        title = ttk.Label(
            scrollable_frame,
            text="🚀 Bienvenido al Analizador de Complejidad Temporal",
            style='Title.TLabel'
        )
        title.pack(pady=(0, 20))
        
        # Secciones
        sections = [
            {
                "title": "📋 ¿Qué hace este programa?",
                "content": "Analiza el comportamiento temporal de tu código Python. "
                          "Ejecuta tu código múltiples veces y mide cuánto tiempo tarda, "
                          "ayudándote a entender su complejidad temporal (O(1), O(n), O(n²), etc.)."
            },
            {
                "title": "✍️ Editor de Código",
                "content": "Escribe o pega tu código Python aquí.\n\n"
                          "Puede ser:\n"
                          "• Una función simple\n"
                          "• Un algoritmo complejo\n"
                          "• Código con loops anidados\n"
                          "• Funciones recursivas\n\n"
                          "El código se ejecutará múltiples veces para medir su rendimiento."
            },
            {
                "title": "🔢 Configuración de Ejecuciones",
                "content": "Determina cuántas veces se ejecutará tu código:\n\n"
                          "📊 Modo Estándar:\n"
                          "Ejecuta 700, 1500 y 3000 veces. Ideal para la mayoría de casos.\n\n"
                          "✏️ Modo Personalizado:\n"
                          "Define tus propias configuraciones (hasta 1,000,000 ejecuciones).\n\n"
                          "💡 El programa toma 20 puntos muestreados de cada configuración "
                          "para crear gráficos más claros."
            },
            {
                "title": "🎯 Análisis de Complejidad",
                "content": "El programa detecta automáticamente la complejidad:\n\n"
                          "• O(1): Tiempo constante\n"
                          "• O(log n): Logarítmica (búsqueda binaria)\n"
                          "• O(n): Lineal (un loop simple)\n"
                          "• O(n log n): Divide y conquista (merge sort)\n"
                          "• O(n²): Cuadrática (loops anidados)\n"
                          "• O(n³) o superior: Cúbica o mayor\n\n"
                          "Para funciones recursivas, muestra la relación de recurrencia."
            },
            {
                "title": "📈 Visualización",
                "content": "Muestra 3 gráficos correspondientes a cada configuración:\n\n"
                          "• Línea principal: Muestra los tiempos muestreados\n"
                          "• Línea punteada: Tiempo promedio\n"
                          "• Etiqueta: Tiempo promedio formateado\n\n"
                          "Los gráficos te ayudan a ver si el tiempo se mantiene constante "
                          "o varía durante las ejecuciones."
            },
            {
                "title": "🔍 Botones Disponibles",
                "content": "▶ ANALIZAR: Ejecuta el análisis completo\n"
                          "🔍 Detectar: Solo detecta la complejidad sin ejecutar\n"
                          "✓ Sintaxis: Verifica que tu código sea válido\n"
                          "🗑 Limpiar: Borra todo y reinicia\n"
                          "📝 Ejemplos: Carga ejemplos de código\n"
                          "💾 Exportar: Guarda los gráficos como PNG"
            },
            {
                "title": "💡 Consejos de Uso",
                "content": "• Empieza con configuraciones pequeñas para código complejo\n"
                          "• Usa 🔍 Detectar primero para ver la complejidad estimada\n"
                          "• Verifica la sintaxis antes de analizar\n"
                          "• Los códigos con O(n²) o mayor pueden tardar más\n"
                          "• Usa los ejemplos para aprender sobre cada complejidad\n"
                          "• Exporta los gráficos para reportes o presentaciones"
            },
            {
                "title": "⚠️ Limitaciones",
                "content": "• Máximo: 1,000,000 ejecuciones por configuración\n"
                          "• El código debe ser Python válido\n"
                          "• No se pueden usar imports externos\n"
                          "• Funciones muy complejas pueden tardar bastante\n"
                          "• La detección de complejidad es una estimación"
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
        "editor": {
            "title": "Editor de Código",
            "content": "Escribe o pega tu código Python aquí.\n\n"
                      "📝 Tipos de código soportados:\n"
                      "• Funciones definidas con 'def'\n"
                      "• Código directo (asignaciones, operaciones)\n"
                      "• Algoritmos con loops\n"
                      "• Funciones recursivas\n\n"
                      "💡 Ejemplos:\n"
                      "def suma(a, b):\n"
                      "    return a + b\n\n"
                      "resultado = x ** 2 + y\n\n"
                      "⚠️ Nota: No uses 'import' de librerías externas.\n"
                      "Variables básicas (a, b, x, y, arr, n, m, k) están predefinidas."
        },
        "ejecuciones": {
            "title": "Número de Ejecuciones",
            "content": "Configura cuántas veces se ejecutará tu código.\n\n"
                      "📊 Modo Estándar:\n"
                      "• Configuración 1: 700 ejecuciones\n"
                      "• Configuración 2: 1,500 ejecuciones\n"
                      "• Configuración 3: 3,000 ejecuciones\n\n"
                      "Ideal para la mayoría de análisis. Balance entre "
                      "precisión y tiempo de espera.\n\n"
                      "✏️ Modo Personalizado:\n"
                      "Define tus propias configuraciones según tus necesidades.\n"
                      "• Mínimo: 1 ejecución\n"
                      "• Máximo: 1,000,000 ejecuciones\n\n"
                      "📈 Puntos Muestreados:\n"
                      "Se toman 20 puntos distribuidos uniformemente de cada "
                      "configuración para crear gráficos claros y legibles.\n\n"
                      "⏱️ Recomendaciones:\n"
                      "• Código simple (O(1), O(n)): Usar configuraciones altas\n"
                      "• Código complejo (O(n²), O(n³)): Usar configuraciones bajas\n"
                      "• Para pruebas rápidas: 100, 500, 1000"
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
        dialog.geometry("550x500")
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