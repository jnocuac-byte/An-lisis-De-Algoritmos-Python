# main_menu.py - Interfaz del menú principal
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from theme import ModernDarkTheme
from info_windows import ProgramInfoWindow, AboutMeWindow


class MainMenuGUI:
    """Interfaz principal del sistema de análisis de algoritmos"""
    
    def __init__(self, root):
        self.root = root
        self.colors = ModernDarkTheme.COLORS
        
        # Configurar ventana
        self.root.configure(bg=self.colors['bg_primary'])
        self.root.protocol("WM_DELETE_WINDOW", self.quit_application)
        
        self.setup_ui()

    def on_close(self):
        """Maneja el cierre de la ventana principal"""
        self.quit_application()
    
    def setup_ui(self):
        """Configura la interfaz del menú"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === HEADER ===
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Título principal
        title_label = ttk.Label(
            header_frame,
            text="🎓 Sistema de Análisis de Algoritmos",
            font=("Segoe UI", 24, "bold"),
            foreground=self.colors['accent']
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Herramienta educativa para análisis de complejidad temporal y algoritmos de ordenamiento",
            style='Secondary.TLabel',
            font=("Segoe UI", 11)
        )
        subtitle_label.pack()
        
        # Separator
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.pack(fill=tk.X, pady=20)
        
        # === SECCIÓN DE PROGRAMAS ===
        programs_frame = ttk.LabelFrame(
            main_frame,
            text="📚  Programas Disponibles",
            padding=25
        )
        programs_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Grid para centrar los botones
        programs_frame.grid_columnconfigure(0, weight=1)
        programs_frame.grid_columnconfigure(1, weight=1)
        
        # Programa 1: Análisis de Complejidad Temporal
        prog1_frame = self.create_program_card(
            programs_frame,
            "🕒 Análisis de Complejidad Temporal",
            "Analiza la complejidad temporal de cualquier código Python.\n"
            "Detecta O(1), O(n), O(n²), O(log n) y más.",
            self.launch_temporal_analyzer
        )
        prog1_frame.grid(row=0, column=0, padx=15, pady=10, sticky=tk.NSEW)
        
        # Programa 2: Análisis de Ordenamiento
        prog2_frame = self.create_program_card(
            programs_frame,
            "📊 Análisis de Algoritmos de Ordenamiento",
            "Compara 8 algoritmos de ordenamiento diferentes.\n"
            "Visualiza rendimiento y complejidad temporal.",
            self.launch_sorting_analyzer
        )
        prog2_frame.grid(row=0, column=1, padx=15, pady=10, sticky=tk.NSEW)
        
        # Separator
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=20)
        
        # === SECCIÓN DE INFORMACIÓN ===
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Botón información del programa
        ttk.Button(
            info_frame,
            text="📖 Sobre el Programa",
            command=self.show_program_info,
            width=30
        ).grid(row=0, column=0, padx=10, pady=5)
        
        # Botón sobre mí
        ttk.Button(
            info_frame,
            text="👤 Sobre el Autor",
            command=self.show_about_me,
            width=30
        ).grid(row=0, column=1, padx=10, pady=5)
        
        # === FOOTER ===
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botón salir
        ttk.Button(
            footer_frame,
            text="❌ Salir de la Aplicación",
            command=self.quit_application,
            style="Accent.TButton"
        ).pack(pady=10)
        
        # Créditos
        credits_label = ttk.Label(
            footer_frame,
            text="Desarrollado por Juan Esteban Nocua | Universidad Central | 2025",
            style='Secondary.TLabel',
            font=("Segoe UI", 9)
        )
        credits_label.pack(pady=(10, 0))
    
    def create_program_card(self, parent, title, description, command):
        """Crea una tarjeta para un programa"""
        # Frame contenedor
        card_frame = ttk.Frame(parent, relief='flat', borderwidth=2)
        
        # Título
        title_label = ttk.Label(
            card_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            foreground=self.colors['accent']
        )
        title_label.pack(pady=(10, 15))
        
        # Descripción
        desc_label = ttk.Label(
            card_frame,
            text=description,
            wraplength=280,
            justify=tk.CENTER,
            style='Secondary.TLabel'
        )
        desc_label.pack(pady=(0, 20), padx=15)
        
        # Botón de lanzamiento
        ttk.Button(
            card_frame,
            text="▶ Iniciar Programa",
            command=command,
            style="Accent.TButton"
        ).pack(pady=(0, 15), padx=20, fill=tk.X)
        
        return card_frame
    
    def launch_temporal_analyzer(self):
        """Lanza el analizador de complejidad temporal"""
        try:
            # Agregar directorio al path
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AnalisisDeAlgoritmos'))
            
            from AnalisisDeAlgoritmos.gui import TemporalAnalyzerGUI
            
            # Crear nueva ventana
            analyzer_window = tk.Toplevel(self.root)
            ModernDarkTheme.apply_theme(analyzer_window)
            ModernDarkTheme.configure_matplotlib_dark()
            
            # Configurar cierre
            def on_close():
                analyzer_window.destroy()
                self.root.deiconify()  # Mostrar menú principal
            
            analyzer_window.protocol("WM_DELETE_WINDOW", on_close)
            
            # Ocultar menú principal
            self.root.withdraw()
            
            # Lanzar aplicación y pasar callback para volver
            app = TemporalAnalyzerGUI(analyzer_window, on_close)
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo iniciar el analizador de complejidad:\n{str(e)}"
            )

    def launch_sorting_analyzer(self):
        """Lanza el analizador de algoritmos de ordenamiento"""
        try:
            # Agregar directorio al path
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AnalisisDeAdO'))
            
            from AnalisisDeAdO.sorting_gui import SortingAnalyzerGUI
            
            # Crear nueva ventana
            sorting_window = tk.Toplevel(self.root)
            ModernDarkTheme.apply_theme(sorting_window)
            ModernDarkTheme.configure_matplotlib_dark()
            
            # Configurar cierre
            def on_close():
                sorting_window.destroy()
                self.root.deiconify()  # Mostrar menú principal
            
            sorting_window.protocol("WM_DELETE_WINDOW", on_close)
            
            # Ocultar menú principal
            self.root.withdraw()
            
            # Lanzar aplicación y pasar callback para volver
            app = SortingAnalyzerGUI(sorting_window, on_close)
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo iniciar el analizador de ordenamiento:\n{str(e)}"
            )
    
    def show_program_info(self):
        """Muestra información sobre el programa"""
        ProgramInfoWindow(self.root)
    
    def show_about_me(self):
        """Muestra información sobre el autor"""
        AboutMeWindow(self.root)
    
    def quit_application(self):
        """Cierra la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.root.quit()
            self.root.destroy()
            sys.exit(0)