# sorting_analyzer.py
import time
from typing import List, Dict, Tuple, Callable
from sorting_algorithms import SortingAlgorithms


class SortingAnalyzer:
    """Analiza el rendimiento de algoritmos de ordenamiento"""
    
    @staticmethod
    def measure_sorting_time(
        algorithm_func: Callable,
        dataset: List[int],
        timeout: float = 300.0
    ) -> Tuple[float, bool, str]:
        """
        Mide el tiempo de ejecución de un algoritmo
        
        Args:
            algorithm_func: Función del algoritmo
            dataset: Datos a ordenar
            timeout: Tiempo máximo en segundos (por defecto 5 minutos)
        
        Returns:
            Tupla (tiempo, éxito, mensaje_error)
        """
        try:
            start_time = time.perf_counter()
            result = algorithm_func(dataset)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            
            # Verificar timeout
            if execution_time > timeout:
                return execution_time, False, "Tiempo de ejecución excedido"
            
            # Verificar que el resultado esté ordenado
            if not SortingAnalyzer.is_sorted(result):
                return execution_time, False, "El algoritmo no ordenó correctamente"
            
            return execution_time, True, ""
            
        except RecursionError:
            return 0.0, False, "Error: Límite de recursión excedido"
        except MemoryError:
            return 0.0, False, "Error: Memoria insuficiente"
        except ValueError as e:
            return 0.0, False, f"Error: {str(e)}"
        except Exception as e:
            return 0.0, False, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def is_sorted(arr: List[int]) -> bool:
        """Verifica si un arreglo está ordenado"""
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True
    
    @staticmethod
    def analyze_multiple_algorithms(
        algorithm_names: List[str],
        datasets: List[List[int]],
        progress_callback: Callable = None # type: ignore
    ) -> Dict[str, Dict]:
        """
        Analiza múltiples algoritmos sobre múltiples datasets
        
        Args:
            algorithm_names: Lista de nombres de algoritmos
            datasets: Lista de datasets a probar
            progress_callback: Función callback para reportar progreso
        
        Returns:
            Diccionario con resultados por algoritmo
        """
        results = {}
        total_tests = len(algorithm_names) * len(datasets)
        current_test = 0
        
        for algo_name in algorithm_names:
            algo_func = SortingAlgorithms.get_sorting_function(algo_name) # type: ignore
            algo_info = SortingAlgorithms.get_algorithm_info()[algo_name] # type: ignore
            
            times = []
            sizes = []
            errors = []
            
            for i, dataset in enumerate(datasets):
                current_test += 1
                
                if progress_callback:
                    progress = (current_test / total_tests) * 100
                    progress_callback(progress, algo_name, len(dataset))
                
                exec_time, success, error_msg = SortingAnalyzer.measure_sorting_time(
                    algo_func, dataset
                )
                
                if success:
                    times.append(exec_time)
                    sizes.append(len(dataset))
                else:
                    errors.append({
                        'dataset_index': i,
                        'size': len(dataset),
                        'error': error_msg
                    })
                    # Si hay error, continuar con el siguiente algoritmo
                    break
            
            results[algo_name] = {
                'times': times,
                'sizes': sizes,
                'errors': errors,
                'complexity': algo_info,
                'success': len(errors) == 0
            }
        
        return results
    
    @staticmethod
    def analyze_single_dataset(
        algorithm_names: List[str],
        dataset: List[int],
        progress_callback: Callable = None # type: ignore
    ) -> Dict[str, Dict]:
        """
        Analiza múltiples algoritmos sobre un único dataset
        
        Args:
            algorithm_names: Lista de nombres de algoritmos
            dataset: Dataset único a probar
            progress_callback: Función callback para reportar progreso
        
        Returns:
            Diccionario con resultados por algoritmo
        """
        results = {}
        total_tests = len(algorithm_names)
        
        for i, algo_name in enumerate(algorithm_names):
            if progress_callback:
                progress = ((i + 1) / total_tests) * 100
                progress_callback(progress, algo_name, len(dataset))
            
            algo_func = SortingAlgorithms.get_sorting_function(algo_name) # type: ignore
            algo_info = SortingAlgorithms.get_algorithm_info()[algo_name] # type: ignore
            
            exec_time, success, error_msg = SortingAnalyzer.measure_sorting_time(
                algo_func, dataset
            )
            
            results[algo_name] = {
                'time': exec_time,
                'size': len(dataset),
                'error': error_msg if not success else None,
                'complexity': algo_info,
                'success': success
            }
        
        return results
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Formatea el tiempo de ejecución de manera legible"""
        if seconds < 0.001:
            return f"{seconds * 1000000:.2f} µs"
        elif seconds < 1:
            return f"{seconds * 1000:.2f} ms"
        else:
            return f"{seconds:.4f} s"