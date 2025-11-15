# ejemplos_python.py
"""
Módulo con ejemplos de código para diferentes complejidades temporales
"""
import tkinter as tk
from tkinter import ttk

class EjemplosWindow:
    """Ventana para seleccionar ejemplos de código"""
    
    EJEMPLOS = {
        "O(1) - Constante": {
            "descripcion": "Operaciones que siempre tardan lo mismo",
            "codigo": """# Complejidad O(1) - Tiempo Constante
# Las operaciones se ejecutan en tiempo fijo

def operacion_constante():
    resultado = 5 + 10
    x = resultado * 2
    return x

# Ejecutar
valor = operacion_constante()"""
        },
        
        "O(n) - Lineal": {
            "descripcion": "Un solo loop que recorre n elementos",
            "codigo": """# Complejidad O(n) - Lineal
# El tiempo crece proporcionalmente con n

def suma_elementos(arr):
    total = 0
    for num in arr:
        total += num
    return total

# Ejecutar
resultado = suma_elementos([1, 2, 3, 4, 5])"""
        },
        
        "O(n²) - Cuadrática": {
            "descripcion": "Loops anidados que recorren n×n elementos",
            "codigo": """# Complejidad O(n²) - Cuadrática
# Dos loops anidados

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Ejecutar
ordenado = bubble_sort([5, 2, 8, 1, 9])"""
        },
        
        "O(log n) - Logarítmica": {
            "descripcion": "Divide el problema a la mitad en cada paso",
            "codigo": """# Complejidad O(log n) - Logarítmica
# Búsqueda binaria

def busqueda_binaria(arr, target):
    izq, der = 0, len(arr) - 1
    
    while izq <= der:
        mid = (izq + der) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            izq = mid + 1
        else:
            der = mid - 1
    return -1

# Ejecutar
resultado = busqueda_binaria([1,3,5,7,9], 5)"""
        },
        
        "O(n log n) - Linearítmica": {
            "descripcion": "Divide y conquista (ej: merge sort)",
            "codigo": """# Complejidad O(n log n) - Linearítmica
# Merge Sort

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    izq = merge_sort(arr[:mid])
    der = merge_sort(arr[mid:])
    
    return merge(izq, der)

def merge(izq, der):
    resultado = []
    i = j = 0
    
    while i < len(izq) and j < len(der):
        if izq[i] < der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

# Ejecutar
ordenado = merge_sort([5,2,8,1,9,3])"""
        },
        
        "O(2^n) - Exponencial": {
            "descripcion": "Crece exponencialmente (ej: Fibonacci recursivo)",
            "codigo": """# Complejidad O(2^n) - Exponencial
# Fibonacci recursivo (LENTO para n > 30)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Ejecutar (usa n pequeño: 5-15)
resultado = fibonacci(10)"""
        },
        
        "O(n³) - Cúbica": {
            "descripcion": "Tres loops anidados",
            "codigo": """# Complejidad O(n³) - Cúbica
# Multiplicación de matrices

def multiplicar_matrices(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

# Ejecutar
A = [[1,2], [3,4]]
B = [[5,6], [7,8]]
resultado = multiplicar_matrices(A, B)"""
        },
        
        "Counting Sort O(n+k)": {
            "descripcion": "Ordenamiento por conteo (del archivo Algoritmos.txt)",
            "codigo": """# Counting Sort - O(n + k)
# Ordena números enteros eficientemente

def counting_sort(arr):
    if not arr:
        return []
    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    for i in range(1, len(count)):
        count[i] += count[i-1]

    output = [0] * len(arr)

    for num in reversed(arr):
        output_index = count[num] - 1
        output[output_index] = num
        count[num] -= 1

    return output

# Ejecutar
arreglo = [4, 2, 2, 8, 3, 3, 1]
ordenado = counting_sort(arreglo)
print(ordenado)"""
        },
        
        "Merge Sort O(n log n)": {
            "descripcion": "Merge Sort (del archivo Algoritmos.txt)",
            "codigo": """# Merge Sort - O(n log n)
# Ordenamiento por mezcla

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            
    return arr

# Ejecutar
arreglo = [38, 27, 43, 3, 9, 82, 10]
ordenado = merge_sort(arreglo)
print(ordenado)"""
        },
        
        "Bubble Sort O(n²)": {
            "descripcion": "Bubble Sort (del archivo Algoritmos.txt)",
            "codigo": """# Bubble Sort - O(n²)
# Ordenamiento de burbuja

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Ejecutar
arreglo = [64, 34, 25, 12, 22, 11, 90]
ordenado = bubble_sort(arreglo)
print(ordenado)"""
        }
    }
    
    def __init__(self, parent, callback):
        """
        Args:
            parent: Ventana padre
            callback: Función que se llama con el código seleccionado
        """
        from theme import ModernDarkTheme
        
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title("📝 Ejemplos de Código Python")
        self.window.geometry("920x670")
        
        # Aplicar tema
        self.colors = ModernDarkTheme.COLORS
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
        """Crea los widgets de la ventana"""
        # Header
        header = ttk.Frame(self.window, padding=15)
        header.pack(fill=tk.X)
        
        ttk.Label(
            header,
            text="📝  Ejemplos de Código por Complejidad",
            style='Title.TLabel'
        ).pack()
        
        ttk.Label(
            header,
            text="Selecciona un ejemplo para cargarlo en el editor",
            style='Secondary.TLabel'
        ).pack(pady=5)
        
        # Frame principal con dos paneles
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Lista de ejemplos
        left_panel = ttk.LabelFrame(main_frame, text="Categorías", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        
        # Crear listbox con scrollbar
        list_frame = ttk.Frame(left_panel)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 10),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground='#ffffff',
            activestyle='none',
            highlightthickness=0,
            width=25
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Agregar ejemplos a la lista
        for nombre in self.EJEMPLOS.keys():
            self.listbox.insert(tk.END, nombre)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Panel derecho - Detalles y código
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Descripción
        self.desc_label = ttk.Label(
            right_panel,
            text="Selecciona un ejemplo de la lista",
            style='Heading.TLabel',
            wraplength=500
        )
        self.desc_label.pack(pady=10)
        
        # Área de código
        code_label = ttk.Label(right_panel, text="Vista Previa:", style='Heading.TLabel')
        code_label.pack(anchor=tk.W, padx=5, pady=(10, 5))
        
        code_frame = ttk.Frame(right_panel)
        code_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        code_scrollbar = ttk.Scrollbar(code_frame)
        code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.code_text = tk.Text(
            code_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            yscrollcommand=code_scrollbar.set,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            state=tk.DISABLED
        )
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        code_scrollbar.config(command=self.code_text.yview)
        
        # Botones
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="✓ Cargar en Editor",
            command=self.load_code,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="✕ Cerrar",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Seleccionar primer elemento por defecto
        self.listbox.selection_set(0)
        self.on_select(None)
    
    def on_select(self, event):
        """Maneja la selección de un ejemplo"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        nombre = self.listbox.get(index)
        ejemplo = self.EJEMPLOS[nombre]
        
        # Actualizar descripción
        self.desc_label.config(text=f"{nombre}\n{ejemplo['descripcion']}")
        
        # Mostrar código
        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete('1.0', tk.END)
        self.code_text.insert('1.0', ejemplo['codigo'])
        self.code_text.config(state=tk.DISABLED)
    
    def load_code(self):
        """Carga el código seleccionado en el editor"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        nombre = self.listbox.get(index)
        codigo = self.EJEMPLOS[nombre]['codigo']
        
        # Llamar al callback con el código
        self.callback(codigo)
        self.window.destroy()