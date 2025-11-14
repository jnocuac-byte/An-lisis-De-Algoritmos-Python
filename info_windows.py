# info_windows.py - Ventanas de información del programa y autor
import tkinter as tk
from tkinter import ttk
from theme import ModernDarkTheme


class ProgramInfoWindow:
    """Ventana con información sobre el programa"""
    
    def __init__(self, parent):
        self.colors = ModernDarkTheme.COLORS
        
        self.window = tk.Toplevel(parent)
        self.window.title("📖 Sobre el Programa")
        self.window.geometry("700x600")
        self.window.resizable(False, False)
        self.window.configure(bg=self.colors['bg_primary'])
        
        # Centrar ventana
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        ttk.Label(
            scrollable_frame,
            text="📚 Sistema de Análisis de Algoritmos",
            style='Title.TLabel'
        ).pack(pady=(0, 20))
        
        # Contenido
        content = """
🎯 Objetivo del Programa

Este sistema educativo fue desarrollado como proyecto para la clase de Análisis de Algoritmos, 
con el propósito de facilitar el estudio y comprensión de la complejidad temporal y los algoritmos 
de ordenamiento.

📦 Componentes del Sistema

1️⃣ Analizador de Complejidad Temporal
   • Analiza cualquier código Python y determina su complejidad
   • Detecta: O(1), O(log n), O(n), O(n log n), O(n²), O(n³) y O(2ⁿ)
   • Mide tiempos de ejecución reales
   • Proporciona visualizaciones gráficas
   • Incluye ejemplos de código predefinidos

2️⃣ Analizador de Algoritmos de Ordenamiento
   • Compara 8 algoritmos de ordenamiento clásicos
   • Soporta dos modos: generación interna o carga desde archivo
   • Muestra complejidades teóricas (mejor, promedio, peor caso)
   • Visualizaciones comparativas entre algoritmos
   • Exportación de resultados en CSV

🎓 Contexto Académico

Clase: Análisis de Algoritmos
Institución: Universidad Central
Semestre: 2025-1
Profesor: Giovanny Alexander Briceño Riveros

💡 Propósito Educativo

El sistema está diseñado para:
   • Ayudar a estudiantes a comprender la complejidad algorítmica
   • Proporcionar herramientas visuales de análisis
   • Facilitar la comparación práctica de algoritmos
   • Reforzar conceptos teóricos con ejemplos prácticos

🛠️ Tecnologías Utilizadas

   • Python 3.10+
   • Tkinter (Interfaz gráfica)
   • Matplotlib (Visualizaciones)
   • NumPy (Análisis numérico)
   • Threading (Procesamiento asíncrono)

📖 Licencia y Uso

Este programa es de uso educativo libre. Puede ser utilizado y modificado con 
fines académicos, dando el crédito correspondiente al autor.
        """
        
        text_widget = tk.Text(
            scrollable_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            padx=15,
            pady=15,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            relief='flat',
            height=20
        )
        text_widget.insert('1.0', content)
        text_widget.configure(state='disabled')
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        ttk.Button(
            self.window,
            text="Cerrar",
            command=self.window.destroy
        ).pack(pady=15)


class AboutMeWindow:
    """Ventana con información sobre el autor"""
    
    def __init__(self, parent):
        self.colors = ModernDarkTheme.COLORS
        
        self.window = tk.Toplevel(parent)
        self.window.title("👤 Sobre el Autor")
        self.window.geometry("700x650")
        self.window.resizable(False, False)
        self.window.configure(bg=self.colors['bg_primary'])
        
        # Centrar ventana
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        ttk.Label(
            scrollable_frame,
            text="👋 Juan Esteban Nocua Camacho",
            style='Title.TLabel'
        ).pack(pady=(0, 20))
        
        # Contenido
        content = """
💻 Estudiante de Ingeniería de Sistemas
🎓 Universidad Central | Bogotá, Colombia

🧐 Sobre Mí

Estudiante apasionado por el desarrollo de software y la programación, con enfoque en:
   • Desarrollo Backend
   • Arquitectura de Sistemas
   • Diseño de Bases de Datos
   • Optimización de Algoritmos

Busco establecer bases sólidas y colaborar en proyectos desafiantes para expandir 
mis habilidades de desarrollo.

🚀 Proyecto Destacado

Portal Web Completo - Desplegado en Google Cloud Platform
   • Backend: Spring Framework + Java
   • Frontend: HTML, CSS, JavaScript
   • Cloud: Google Cloud Platform (GCP)
   • Arquitectura: Microservicios
   • Contenerización: Docker

✨ Stack Tecnológico

🏗️ Arquitectura
   • Docker
   • Microservicios
   • Kubernetes

☁️ Cloud Computing
   • Google Cloud Platform (GCP)
   • Servicios de infraestructura cloud

💼 Backend & Core
   • Spring Framework
   • Java
   • Bases de Datos (SQL/NoSQL)
   • Análisis y Optimización de Algoritmos

⚽ Intereses Personales

🎮 Videojuegos
   Entusiasta de los nuevos lanzamientos y tecnologías gaming

🚗 Automóviles Clásicos
   Admirador de autos retro: japoneses, americanos y alemanes

⚽ Fútbol
   Fan del FC Barcelona y Lionel Messi

🤝 Contacto

📧 Email Institucional:  jnocuac@ucentral.edu.co
📧 Email Personal:       juesnoca@hotmail.com
💼 LinkedIn:             linkedin.com/in/juan-esteban-nocua-camacho-bb2663269

🔭 Actualmente trabajando en:
   Expandiendo funcionalidades del portal web en GCP
   Profundizando en Kubernetes y microservicios avanzados

🌱 Estoy aprendiendo:
   Servicios avanzados de Google Cloud
   Patrones de diseño para arquitecturas distribuidas
   Optimización y escalabilidad de sistemas

💬 Pregúntame sobre:
   • Desarrollo backend con Spring
   • Arquitectura de Microservicios
   • Despliegue en Google Cloud Platform
   • Análisis de Algoritmos
        """
        
        text_widget = tk.Text(
            scrollable_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            padx=15,
            pady=15,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            relief='flat',
            height=22
        )
        text_widget.insert('1.0', content)
        text_widget.configure(state='disabled')
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        ttk.Button(
            self.window,
            text="Cerrar",
            command=self.window.destroy
        ).pack(pady=15)