# theme.py
"""
Tema oscuro moderno para el sistema de análisis de algoritmos
Inspirado en GitHub Dark - Compartido por todos los módulos
"""
import tkinter as tk
from tkinter import ttk

class ModernDarkTheme:
    """Tema oscuro moderno para la aplicación"""
    
    # Paleta de colores GitHub Dark
    COLORS = {
        # Fondos
        'bg_primary': '#0d1117',      # Fondo principal
        'bg_secondary': '#161b22',    # Fondo secundario
        'bg_tertiary': '#1c2128',     # Fondo terciario
        'bg_hover': '#21262d',        # Hover
        'bg_active': '#30363d',       # Activo
        
        # Bordes
        'border': '#30363d',
        'border_hover': '#58a6ff',
        
        # Textos
        'text_primary': '#c9d1d9',    # Texto principal
        'text_secondary': '#8b949e',  # Texto secundario
        'text_link': '#58a6ff',       # Enlaces
        
        # Acentos y estados
        'accent': '#58a6ff',          # Azul
        'success': '#3fb950',         # Verde
        'warning': '#d29922',         # Amarillo
        'error': '#f85149',           # Rojo
        'purple': '#bc8cff',          # Morado
        
        # Gráficos
        'chart_1': '#58a6ff',
        'chart_2': '#bc8cff',
        'chart_3': '#3fb950',
        'chart_4': '#f78166',
        'chart_5': '#d29922',
        'chart_6': '#ff7b72',
        'chart_7': '#79c0ff',
        'chart_8': '#ffa657',
    }
    
    @staticmethod
    def apply_theme(root):
        """Aplica el tema oscuro a la aplicación"""
        style = ttk.Style(root)
        
        # Configurar tema base
        style.theme_use('clam')
        
        colors = ModernDarkTheme.COLORS
        
        # Configurar colores generales
        root.configure(bg=colors['bg_primary'])
        
        # Frame
        style.configure('TFrame',
                       background=colors['bg_primary'])
        
        style.configure('Card.TFrame',
                       background=colors['bg_secondary'],
                       relief='flat')
        
        # Label
        style.configure('TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 10))
        
        style.configure('Title.TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Heading.TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 11, 'bold'))
        
        style.configure('Secondary.TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_secondary'],
                       font=('Segoe UI', 9))
        
        # LabelFrame
        style.configure('TLabelframe',
                       background=colors['bg_secondary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('TLabelframe.Label',
                       background=colors['bg_secondary'],
                       foreground=colors['accent'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Button
        style.configure('TButton',
                       background=colors['bg_active'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       focuscolor='none',
                       font=('Segoe UI', 10),
                       padding=(15, 8))
        
        style.map('TButton',
                 background=[('active', colors['bg_hover']),
                           ('pressed', colors['bg_active'])],
                 foreground=[('active', colors['text_primary'])],
                 bordercolor=[('active', colors['border_hover'])])
        
        # Botón de acento (primary)
        style.configure('Accent.TButton',
                       background=colors['accent'],
                       foreground='#ffffff',
                       bordercolor=colors['accent'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 10))
        
        style.map('Accent.TButton',
                 background=[('active', '#4493f8'),
                           ('pressed', '#388bfd')],
                 foreground=[('active', '#ffffff')])
        
        # Radiobutton
        style.configure('TRadiobutton',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 10),
                       focuscolor='none')
        
        style.map('TRadiobutton',
                 background=[('active', colors['bg_primary'])],
                 foreground=[('active', colors['accent'])])
        
        # Checkbutton
        style.configure('TCheckbutton',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 10),
                       focuscolor='none')
        
        style.map('TCheckbutton',
                 background=[('active', colors['bg_primary'])],
                 foreground=[('active', colors['accent'])])
        
        # Entry
        style.configure('TEntry',
                       fieldbackground=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       insertcolor=colors['text_primary'],
                       font=('Segoe UI', 10))
        
        style.map('TEntry',
                 fieldbackground=[('readonly', colors['bg_tertiary'])],
                 bordercolor=[('focus', colors['accent'])])
        
        # Combobox
        style.configure('TCombobox',
                       fieldbackground=colors['bg_tertiary'],
                       background=colors['bg_active'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       arrowcolor=colors['text_primary'],
                       font=('Segoe UI', 10))
        
        style.map('TCombobox',
                 fieldbackground=[('readonly', colors['bg_tertiary'])],
                 bordercolor=[('focus', colors['accent'])])
        
        # Treeview
        style.configure('Treeview',
                       background=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       fieldbackground=colors['bg_tertiary'],
                       bordercolor=colors['border'],
                       font=('Segoe UI', 9))
        
        style.configure('Treeview.Heading',
                       background=colors['bg_active'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Treeview',
                 background=[('selected', colors['accent'])],
                 foreground=[('selected', '#ffffff')])
        
        style.map('Treeview.Heading',
                 background=[('active', colors['bg_hover'])])
        
        # Progressbar
        style.configure('TProgressbar',
                       background=colors['accent'],
                       troughcolor=colors['bg_tertiary'],
                       bordercolor=colors['border'],
                       lightcolor=colors['accent'],
                       darkcolor=colors['accent'])
        
        # Scrollbar
        style.configure('TScrollbar',
                       background=colors['bg_active'],
                       troughcolor=colors['bg_tertiary'],
                       bordercolor=colors['border'],
                       arrowcolor=colors['text_primary'])
        
        style.map('TScrollbar',
                 background=[('active', colors['bg_hover'])])
        
        # Separator
        style.configure('TSeparator',
                       background=colors['border'])
        
        # Configurar colores de selección para widgets de texto
        root.option_add('*TCombobox*Listbox.background', colors['bg_tertiary'])
        root.option_add('*TCombobox*Listbox.foreground', colors['text_primary'])
        root.option_add('*TCombobox*Listbox.selectBackground', colors['accent'])
        root.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')
        root.option_add('*TCombobox*Listbox.font', 'SegoeUI 10')
    
    @staticmethod
    def configure_matplotlib_dark():
        """Configura matplotlib para tema oscuro"""
        import matplotlib.pyplot as plt
        
        colors = ModernDarkTheme.COLORS
        
        plt.style.use('dark_background')
        plt.rcParams.update({
            'figure.facecolor': colors['bg_secondary'],
            'axes.facecolor': colors['bg_tertiary'],
            'axes.edgecolor': colors['border'],
            'axes.labelcolor': colors['text_primary'],
            'text.color': colors['text_primary'],
            'xtick.color': colors['text_secondary'],
            'ytick.color': colors['text_secondary'],
            'grid.color': colors['border'],
            'legend.facecolor': colors['bg_tertiary'],
            'legend.edgecolor': colors['border'],
            'font.family': 'Segoe UI',
            'font.size': 10,
        })
    
    @staticmethod
    def get_chart_colors():
        """Retorna lista de colores para gráficos"""
        colors = ModernDarkTheme.COLORS
        return [
            colors['chart_1'],
            colors['chart_2'],
            colors['chart_3'],
            colors['chart_4'],
            colors['chart_5'],
            colors['chart_6'],
            colors['chart_7'],
            colors['chart_8'],
        ]