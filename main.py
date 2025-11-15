# main.py - Punto de entrada principal de la aplicación
import tkinter as tk
from main_menu import MainMenuGUI
from theme import ModernDarkTheme


def main():
    """Función principal de la aplicación"""
    root = tk.Tk()
    
    # Aplicar tema oscuro moderno
    ModernDarkTheme.apply_theme(root)
    
    # Configurar ventana principal
    root.title("🚀 Análisis de Algoritmos - Sistema Completo")
    root.geometry("1200x900")
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Iniciar menú principal
    app = MainMenuGUI(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()