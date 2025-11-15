# dataset_manager.py
import random
from typing import List, Tuple


class DatasetManager:
    """Gestiona la generación y carga de datasets para ordenamiento"""
    
    MAX_SIZE = 1000000  # Límite máximo de elementos
    PREDEFINED_SIZES = [1000, 5000, 10000, 50000, 100000]
    NUM_SUBSETS = 15
    
    @staticmethod
    def validate_size(size: int) -> Tuple[bool, str]:
        """Valida que el tamaño esté dentro de límites razonables"""
        if size <= 0:
            return False, "El tamaño debe ser mayor a 0"
        if size > DatasetManager.MAX_SIZE:
            return False, f"El tamaño máximo permitido es {DatasetManager.MAX_SIZE:,}"
        return True, ""
    
    @staticmethod
    def generate_subsets(max_size: int, ordered: bool = False) -> List[List[int]]:
        """
        Genera 15 subconjuntos balanceados desde tamaño proporcional hasta max_size
        
        Args:
            max_size: Tamaño máximo del conjunto
            ordered: Si True, genera conjuntos ordenados, sino desordenados
        
        Returns:
            Lista de 15 subconjuntos
        """
        subsets = []
        step = max_size // DatasetManager.NUM_SUBSETS
        
        for i in range(1, DatasetManager.NUM_SUBSETS + 1):
            size = step * i
            if i == DatasetManager.NUM_SUBSETS:
                size = max_size  # Asegurar que el último sea exactamente max_size
            
            if ordered:
                # Generar conjunto ordenado
                subset = list(range(size))
            else:
                # Generar conjunto desordenado
                subset = list(range(size))
                random.shuffle(subset)
            
            subsets.append(subset)
        
        return subsets
    
    @staticmethod
    def load_from_file(filepath: str) -> Tuple[List[int], str]:
        """
        Carga un conjunto de datos desde un archivo .txt
        
        Args:
            filepath: Ruta al archivo
        
        Returns:
            Tupla (datos, mensaje_error). Si hay error, datos es None
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
            
            # Parsear números separados por comas
            numbers = []
            for item in content.split(','):
                item = item.strip()
                if item:
                    try:
                        numbers.append(int(item))
                    except ValueError:
                        return None, f"Valor inválido encontrado: '{item}'" # type: ignore
            
            if not numbers:
                return None, "El archivo está vacío o no contiene números válidos" # type: ignore
            
            # Validar tamaño
            valid, msg = DatasetManager.validate_size(len(numbers))
            if not valid:
                return None, msg # type: ignore
            
            return numbers, ""
            
        except FileNotFoundError:
            return None, "Archivo no encontrado" # type: ignore
        except Exception as e:
            return None, f"Error al leer archivo: {str(e)}" # type: ignore
    
    @staticmethod
    def get_subset_sizes(max_size: int) -> List[int]:
        """Retorna los tamaños de los subconjuntos que se generarán"""
        sizes = []
        step = max_size // DatasetManager.NUM_SUBSETS
        
        for i in range(1, DatasetManager.NUM_SUBSETS + 1):
            size = step * i
            if i == DatasetManager.NUM_SUBSETS:
                size = max_size
            sizes.append(size)
        
        return sizes
    
    @staticmethod
    def validate_file_path(filepath: str) -> Tuple[bool, str]:
        """Valida que el archivo tenga la extensión correcta"""
        if not filepath:
            return False, "Debe seleccionar un archivo"
        if not filepath.endswith('.txt'):
            return False, "Solo se permiten archivos .txt"
        return True, ""