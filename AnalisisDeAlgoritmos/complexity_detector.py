# complexity_detector.py
import ast
import numpy as np
from typing import List, Dict, Any


class ComplexityDetector:
    """Detecta la complejidad temporal mediante análisis estático del código"""
    
    def __init__(self, code: str):  
        self.code = code
        self.tree = None
        self.has_recursion = False
        self.recursive_functions = set()
        self.max_loop_depth = 0
        self.has_divide_conquer = False
        
    def analyze(self) -> Dict[str, Any]:
        """Analiza el código y determina su complejidad"""
        try:
            self.tree = ast.parse(self.code)
        except SyntaxError:
            return {'complexity': 'Error', 'notation': 'Sintaxis inválida', 'confidence': 0}
        
        # Detectar recursión
        self.detect_recursion()
        
        # Analizar estructura de loops
        loop_analysis = self.analyze_loops()
        
        # Detectar patrones específicos
        patterns = self.detect_patterns()
        
        # Determinar complejidad
        if self.has_recursion:
            return self.analyze_recursive_complexity(patterns)
        else:
            return self.analyze_iterative_complexity(loop_analysis, patterns)
    
    def detect_recursion(self):
        """Detecta si hay funciones recursivas"""
        class RecursionDetector(ast.NodeVisitor):
            def __init__(self):
                self.functions = {}
                self.current_function = None
                self.recursive_calls = set()
                
            def visit_FunctionDef(self, node):
                old_function = self.current_function
                self.current_function = node.name
                self.functions[node.name] = node
                self.generic_visit(node)
                self.current_function = old_function
                
            def visit_Call(self, node):
                if self.current_function and isinstance(node.func, ast.Name):
                    if node.func.id == self.current_function:
                        self.recursive_calls.add(self.current_function)
                self.generic_visit(node)
        
        detector = RecursionDetector()
        detector.visit(self.tree) # type: ignore
        self.has_recursion = len(detector.recursive_calls) > 0
        self.recursive_functions = detector.recursive_calls
        
        return self.has_recursion
    
    def analyze_loops(self) -> Dict[str, Any]:
        """Analiza la estructura de loops anidados"""
        class LoopAnalyzer(ast.NodeVisitor):
            def __init__(self):
                self.max_depth = 0
                self.current_depth = 0
                self.loop_structures = []
                self.has_dependent_loops = False
                
            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                
                loop_var = node.target.id if isinstance(node.target, ast.Name) else None
                iter_info = self.analyze_iterator(node.iter)
                
                self.loop_structures.append({
                    'depth': self.current_depth,
                    'variable': loop_var,
                    'iterator': iter_info
                })
                
                if self.current_depth > 1 and iter_info.get('depends_on_outer'):
                    self.has_dependent_loops = True
                
                self.generic_visit(node)
                self.current_depth -= 1
                
            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
            
            def analyze_iterator(self, node):
                """Analiza el iterador del loop"""
                info = {'type': 'unknown', 'depends_on_outer': False}
                
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id == 'range':
                            info['type'] = 'range'
                            if node.args:
                                arg = node.args[0]
                                if isinstance(arg, ast.BinOp):
                                    info['depends_on_outer'] = True
                                elif isinstance(arg, ast.Name):
                                    info['depends_on_outer'] = True
                        elif node.func.id == 'len':
                            info['type'] = 'len'
                elif isinstance(node, ast.Name):
                    info['type'] = 'variable'
                    info['depends_on_outer'] = False
                    
                return info
        
        analyzer = LoopAnalyzer()
        analyzer.visit(self.tree) # type: ignore
        
        return {
            'max_depth': analyzer.max_depth,
            'structures': analyzer.loop_structures,
            'has_dependent': analyzer.has_dependent_loops
        }
    
    def detect_patterns(self) -> Dict[str, bool]:
        """Detecta patrones algorítmicos comunes"""
        code_lower = self.code.lower()
        
        patterns = {
            'sorting': any(word in code_lower for word in ['sort', 'bubble', 'quick', 'merge', 'heap']),
            'binary_search': 'binary' in code_lower or ('while' in code_lower and '//' in self.code),
            'divide_conquer': any(pattern in self.code for pattern in ['//2', '/ 2', 'mid', 'split']),
            'dynamic_programming': 'dp' in code_lower or 'memo' in code_lower,
            'logarithmic': '//' in self.code or 'log' in code_lower,
        }
        
        if self.has_recursion:
            class DivisionDetector(ast.NodeVisitor):
                def __init__(self):
                    self.has_division = False
                    
                def visit_BinOp(self, node):
                    if isinstance(node.op, (ast.FloorDiv, ast.Div)):
                        self.has_division = True
                    self.generic_visit(node)
            
            detector = DivisionDetector()
            detector.visit(self.tree) # type: ignore
            patterns['divide_conquer'] = detector.has_division
        
        return patterns
    
    def analyze_recursive_complexity(self, patterns: Dict[str, bool]) -> Dict[str, Any]:
        """Analiza la complejidad de algoritmos recursivos"""
        
        class RecursiveAnalyzer(ast.NodeVisitor):
            def __init__(self, recursive_funcs):
                self.recursive_funcs = recursive_funcs
                self.recursive_calls_per_invocation = 0
                self.has_linear_work = False
                self.has_loop_in_recursion = False
                self.current_in_recursive = False
                
            def visit_FunctionDef(self, node):
                if node.name in self.recursive_funcs:
                    old_state = self.current_in_recursive
                    self.current_in_recursive = True
                    
                    calls = 0
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                            if child.func.id == node.name:
                                calls += 1
                    
                    self.recursive_calls_per_invocation = max(self.recursive_calls_per_invocation, calls)
                    
                    for child in ast.walk(node):
                        if isinstance(child, (ast.For, ast.While)):
                            self.has_loop_in_recursion = True
                            self.has_linear_work = True
                    
                    self.generic_visit(node)
                    self.current_in_recursive = old_state
                else:
                    self.generic_visit(node)
        
        analyzer = RecursiveAnalyzer(self.recursive_functions)
        analyzer.visit(self.tree) # type: ignore
        
        if patterns['divide_conquer'] or patterns['binary_search']:
            if analyzer.recursive_calls_per_invocation == 1:
                if analyzer.has_linear_work:
                    complexity = 'O(n)'
                    recurrence = 'T(n) = T(n/2) + O(n)'
                else:
                    complexity = 'O(log n)'
                    recurrence = 'T(n) = T(n/2) + O(1)'
            elif analyzer.recursive_calls_per_invocation == 2:
                if analyzer.has_linear_work:
                    complexity = 'O(n log n)'
                    recurrence = 'T(n) = 2T(n/2) + O(n)'
                else:
                    complexity = 'O(n)'
                    recurrence = 'T(n) = 2T(n/2) + O(1)'
            else:
                complexity = 'O(n log n)'
                recurrence = f'T(n) = {analyzer.recursive_calls_per_invocation}T(n/2) + O(n)'
        else:
            if analyzer.has_loop_in_recursion:
                complexity = 'O(n²)'
                recurrence = 'T(n) = T(n-1) + O(n)'
            else:
                complexity = 'O(n)'
                recurrence = 'T(n) = T(n-1) + O(1)'
        
        return {
            'complexity': complexity,
            'notation': recurrence,
            'is_recursive': True,
            'confidence': 0.85
        }
    
    def analyze_iterative_complexity(self, loop_analysis: Dict, patterns: Dict[str, bool]) -> Dict[str, Any]:
        """Analiza la complejidad de algoritmos iterativos"""
        
        max_depth = loop_analysis['max_depth']
        has_dependent = loop_analysis['has_dependent']
        
        if max_depth == 0:
            return {
                'complexity': 'O(1)',
                'notation': 'O(1)',
                'is_recursive': False,
                'confidence': 0.95
            }
        
        elif max_depth == 1:
            if patterns['binary_search'] or patterns['logarithmic']:
                complexity = 'O(log n)'
            else:
                complexity = 'O(n)'
            
            return {
                'complexity': complexity,
                'notation': complexity,
                'is_recursive': False,
                'confidence': 0.90
            }
        
        elif max_depth == 2:
            complexity = 'O(n²)'
            
            return {
                'complexity': complexity,
                'notation': complexity,
                'is_recursive': False,
                'confidence': 0.85
            }
        
        elif max_depth == 3:
            return {
                'complexity': 'O(n³)',
                'notation': 'O(n³)',
                'is_recursive': False,
                'confidence': 0.80
            }
        
        else:
            return {
                'complexity': f'O(n^{max_depth})',
                'notation': f'O(n^{max_depth})',
                'is_recursive': False,
                'confidence': 0.75
            }
    
    @staticmethod
    def estimate_complexity_from_data(sizes: List[int], times: List[float]) -> str:
        """Estima la complejidad analizando los datos empíricos"""
        if len(sizes) < 3:
            return "Datos insuficientes"
        
        ratios = []
        for i in range(1, len(sizes)):
            size_ratio = sizes[i] / sizes[i-1]
            time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 0
            if time_ratio > 0:
                ratios.append(time_ratio / size_ratio)
        
        if not ratios:
            return "O(1)"
        
        avg_ratio = np.mean(ratios)
        
        if avg_ratio < 1.5:
            return "O(n) o O(log n)"
        elif avg_ratio < 3:
            return "O(n log n)"
        elif avg_ratio < 10:
            return "O(n²)"
        else:
            return "O(n³) o mayor"