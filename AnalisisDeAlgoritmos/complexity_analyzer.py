# complexity_analyzer.py
import numpy as np
from typing import List, Dict, Any
from code_executor import CodeExecutor


class ComplexityAnalyzer:
    """Analiza la complejidad temporal del código"""
    
    @staticmethod
    def analyze_with_dataset(code: str, datasets: List[List[Any]]) -> Dict[str, Any]:
        """Ejecuta el código con múltiples tamaños de entrada y mide tiempos"""
        sizes = []
        times = []
        errors = []
        
        for i, dataset in enumerate(datasets):
            result = CodeExecutor.execute_code(code, dataset)
            
            if result['success']:
                sizes.append(len(dataset))
                times.append(result['time'])
            else:
                errors.append({
                    'dataset_index': i,
                    'size': len(dataset),
                    'error': result['error']
                })
                break
        
        return {
            'sizes': sizes,
            'times': times,
            'errors': errors
        }
    
    @staticmethod
    def analyze_without_dataset(code: str, iterations: int = 10) -> Dict[str, Any]:
        """Ejecuta código sin datasets múltiples veces para obtener tiempo promedio"""
        times = []
        
        for _ in range(iterations):
            result = CodeExecutor.execute_code(code, None)
            if result['success']:
                times.append(result['time'])
            else:
                return {
                    'success': False,
                    'error': result['error']
                }
        
        avg_time = np.mean(times) if times else 0
        std_time = np.std(times) if times else 0
        
        return {
            'success': True,
            'avg_time': avg_time,
            'std_time': std_time,
            'times': times
        }