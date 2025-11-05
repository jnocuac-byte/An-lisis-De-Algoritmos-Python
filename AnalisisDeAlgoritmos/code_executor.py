# code_executor.py
import sys
import time
import traceback
from io import StringIO
from typing import Dict, Any


class CodeExecutor:
    """Ejecuta código y mide su tiempo de ejecución"""
    
    @staticmethod
    def execute_code(code: str, dataset_value: Any = None) -> Dict[str, Any]:
        """Ejecuta el código proporcionado y retorna el tiempo y resultado"""
        global_vars = {
            'arr': dataset_value,
            'conjunto': dataset_value,
            'data': dataset_value,
            '__builtins__': __builtins__
        }
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            start_time = time.perf_counter()
            exec(code, global_vars)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            output = captured_output.getvalue()
            
            return {
                'success': True,
                'time': execution_time,
                'output': output,
                'error': None
            }
        
        except Exception as e:
            error_msg = traceback.format_exc()
            return {
                'success': False,
                'time': 0,
                'output': captured_output.getvalue(),
                'error': error_msg
            }
        
        finally:
            sys.stdout = old_stdout
    
    @staticmethod
    def test_code_syntax(code: str) -> Dict[str, Any]:
        """Verifica la sintaxis del código sin ejecutarlo"""
        try:
            compile(code, '<string>', 'exec')
            return {'valid': True, 'error': None}
        except SyntaxError as e:
            return {'valid': False, 'error': str(e)}