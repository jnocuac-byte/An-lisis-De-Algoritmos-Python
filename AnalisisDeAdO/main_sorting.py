# main_sorting.py - Archivo principal para el analizador de ordenamiento
import tkinter as tk
from sorting_gui import SortingAnalyzerGUI


def main():
    """Función principal"""
    root = tk.Tk()
    
    # Configurar estilos
    style = tk.ttk.Style() # type: ignore
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    
    app = SortingAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()