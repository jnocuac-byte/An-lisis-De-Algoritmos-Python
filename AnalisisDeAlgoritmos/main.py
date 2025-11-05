# main.py - Archivo principal
import tkinter as tk
from gui import TemporalAnalyzerGUI


def main():
    root = tk.Tk()
    app = TemporalAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()