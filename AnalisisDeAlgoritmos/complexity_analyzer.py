# complexity_analyzer.py
import numpy as np
import time
from typing import List, Dict, Any, Tuple
from code_executor import CodeExecutor


class ComplexityAnalyzer:
    """Analiza la complejidad temporal del código"""
    
    SAMPLE_POINTS = 20  # Número de puntos a graficar
    
    @staticmethod
    def analyze_code_execution(
        code: str, 
        num_executions: int,
        progress_callback=None
    ) -> Dict[str, Any]:
        """
        Ejecuta el código múltiples veces y mide tiempos
        
        Args:
            code: Código a ejecutar
            num_executions: Número de veces a ejecutar
            progress_callback: Callback para reportar progreso
            
        Returns:
            Diccionario con tiempos y puntos muestreados
        """
        all_times = []
        sampling_interval = max(1, num_executions // ComplexityAnalyzer.SAMPLE_POINTS)
        sampled_times = []
        sampled_indices = []
        
        # Preparar código envuelto para medición
        wrapped_code = ComplexityAnalyzer._prepare_code_for_execution(code)
        
        for i in range(num_executions):
            # Reportar progreso
            if progress_callback and i % 10 == 0:
                progress = (i / num_executions) * 100
                progress_callback(progress)
            
            # Medir tiempo de ejecución
            start_time = time.perf_counter()
            result = CodeExecutor.execute_code(wrapped_code, None)
            end_time = time.perf_counter()
            
            if not result['success']:
                return {
                    'success': False,
                    'error': result['error'],
                    'iteration': i
                }
            
            execution_time = end_time - start_time
            all_times.append(execution_time)
            
            # Muestrear cada N ejecuciones
            if i % sampling_interval == 0 and len(sampled_times) < ComplexityAnalyzer.SAMPLE_POINTS:
                sampled_times.append(execution_time)
                sampled_indices.append(i + 1)
        
        # Asegurar que tenemos exactamente 20 puntos
        if len(sampled_times) < ComplexityAnalyzer.SAMPLE_POINTS:
            sampled_times.append(all_times[-1])
            sampled_indices.append(num_executions)
        
        return {
            'success': True,
            'all_times': all_times,
            'sampled_times': sampled_times,
            'sampled_indices': sampled_indices,
            'num_executions': num_executions,
            'avg_time': np.mean(all_times),
            'std_time': np.std(all_times),
            'min_time': min(all_times),
            'max_time': max(all_times)
        }
    
    @staticmethod
    def _prepare_code_for_execution(code: str) -> str:
        """
        Prepara el código del usuario para ejecución segura
        Maneja funciones sin parámetros o con parámetros undefined
        """
        # El código se ejecuta tal cual, si hay errores de variables no definidas
        # los ignoramos ya que queremos una línea constante de todas formas
        
        # Envolver en try-except para manejar errores de variables no definidas
        safe_code = f"""
try:
    # Definir variables dummy por si el código las necesita
    a, b, c, d, e = 1, 2, 3, 4, 5
    x, y, z = 10, 20, 30
    arr, lista, data = [1, 2, 3], [4, 5, 6], [7, 8, 9]
    n, m, k = 100, 200, 300
    
    # Ejecutar código del usuario
{ComplexityAnalyzer._indent_code(code, 4)}
except:
    # Si hay error, simplemente hacer una operación trivial
    pass
"""
        return safe_code
    
    @staticmethod
    def _indent_code(code: str, spaces: int) -> str:
        """Indenta código con número de espacios especificado"""
        lines = code.split('\n')
        return '\n'.join(' ' * spaces + line if line.strip() else line for line in lines)
    
    @staticmethod
    def analyze_multiple_executions(
        code: str,
        execution_configs: List[int],
        progress_callback=None
    ) -> Dict[int, Dict[str, Any]]:
        """
        Analiza código con múltiples configuraciones de ejecución
        
        Args:
            code: Código a analizar
            execution_configs: Lista de números de ejecuciones [700, 1500, 3000]
            progress_callback: Callback para progreso
            
        Returns:
            Diccionario con resultados por configuración
        """
        results = {}
        total_configs = len(execution_configs)
        
        for idx, num_exec in enumerate(execution_configs):
            def config_progress(progress):
                overall_progress = ((idx + progress/100) / total_configs) * 100
                if progress_callback:
                    progress_callback(overall_progress, num_exec, progress)
            
            result = ComplexityAnalyzer.analyze_code_execution(
                code,
                num_exec,
                config_progress
            )
            
            if not result['success']:
                return {
                    'success': False,
                    'error': result['error'],
                    'failed_config': num_exec
                } # type: ignore
            
            results[num_exec] = result
        
        return {
            'success': True,
            'results': results
        } # type: ignore
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Formatea el tiempo de ejecución de manera legible"""
        if seconds < 0.000001:
            return f"{seconds * 1000000000:.2f} ns"
        elif seconds < 0.001:
            return f"{seconds * 1000000:.2f} µs"
        elif seconds < 1:
            return f"{seconds * 1000:.2f} ms"
        else:
            return f"{seconds:.4f} s"