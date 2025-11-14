# sorting_algorithms.py
import sys
from typing import List, Dict, Callable

# Aumentar límite de recursión para algoritmos recursivos
sys.setrecursionlimit(100000)


class SortingAlgorithms:
    """Implementación de algoritmos de ordenamiento con información de complejidad"""
    
    @staticmethod
    def get_algorithm_info() -> Dict[str, Dict[str, str]]:
        """Retorna información de complejidad de cada algoritmo"""
        return {
            'Tree Sort': {
                'best': 'O(n log n)',
                'average': 'O(n log n)',
                'worst': 'O(n²)',
                'space': 'O(n)'
            },
            'Bubble Sort': {
                'best': 'O(n)',
                'average': 'O(n²)',
                'worst': 'O(n²)',
                'space': 'O(1)'
            },
            'Selection Sort': {
                'best': 'O(n²)',
                'average': 'O(n²)',
                'worst': 'O(n²)',
                'space': 'O(1)'
            },
            'Insertion Sort': {
                'best': 'O(n)',
                'average': 'O(n²)',
                'worst': 'O(n²)',
                'space': 'O(1)'
            },
            'Merge Sort': {
                'best': 'O(n log n)',
                'average': 'O(n log n)',
                'worst': 'O(n log n)',
                'space': 'O(n)'
            },
            'Quick Sort': {
                'best': 'O(n log n)',
                'average': 'O(n log n)',
                'worst': 'O(n²)',
                'space': 'O(log n)'
            },
            'Counting Sort': {
                'best': 'O(n + k)',
                'average': 'O(n + k)',
                'worst': 'O(n + k)',
                'space': 'O(k)'
            },
            'Radix Sort': {
                'best': 'O(d(n + k))',
                'average': 'O(d(n + k))',
                'worst': 'O(d(n + k))',
                'space': 'O(n + k)'
            }
        }
    
    @staticmethod
    def tree_sort(arr: List[int]) -> List[int]:
        """Tree Sort - O(n log n) average, O(n²) worst"""
        if not arr:
            return []
        
        class TreeNode:
            def __init__(self, value):
                self.value = value
                self.left = None
                self.right = None
        
        def insert(root, value):
            if root is None:
                return TreeNode(value)
            if value < root.value:
                root.left = insert(root.left, value)
            else:
                root.right = insert(root.right, value)
            return root
        
        def inorder(root, result):
            if root:
                inorder(root.left, result)
                result.append(root.value)
                inorder(root.right, result)
        
        root = None
        for value in arr:
            root = insert(root, value)
        
        result = []
        inorder(root, result)
        return result
    
    @staticmethod
    def bubble_sort(arr: List[int]) -> List[int]:
        """Bubble Sort - O(n²)"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n - 1):
            swapped = False
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr
    
    @staticmethod
    def selection_sort(arr: List[int]) -> List[int]:
        """Selection Sort - O(n²)"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    @staticmethod
    def insertion_sort(arr: List[int]) -> List[int]:
        """Insertion Sort - O(n²) average, O(n) best"""
        arr = arr.copy()
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    
    @staticmethod
    def merge_sort(arr: List[int]) -> List[int]:
        """Merge Sort - O(n log n)"""
        if len(arr) <= 1:
            return arr.copy()
        
        def merge(left: List[int], right: List[int]) -> List[int]:
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def merge_sort_recursive(arr: List[int]) -> List[int]:
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort_recursive(arr[:mid])
            right = merge_sort_recursive(arr[mid:])
            return merge(left, right)
        
        return merge_sort_recursive(arr)
    
    @staticmethod
    def quick_sort(arr: List[int]) -> List[int]:
        """Quick Sort - O(n log n) average, O(n²) worst"""
        def quick_sort_recursive(arr: List[int], low: int, high: int):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_recursive(arr, low, pi - 1)
                quick_sort_recursive(arr, pi + 1, high)
        
        def partition(arr: List[int], low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        arr = arr.copy()
        quick_sort_recursive(arr, 0, len(arr) - 1)
        return arr
    
    @staticmethod
    def counting_sort(arr: List[int]) -> List[int]:
        """Counting Sort - O(n + k) donde k es el rango de valores"""
        if not arr:
            return []
        
        arr = arr.copy()
        min_val = min(arr)
        max_val = max(arr)
        range_size = max_val - min_val + 1
        
        # Limitar el rango para evitar consumo excesivo de memoria
        if range_size > 1000000:
            raise ValueError("Rango de valores muy grande para Counting Sort")
        
        count = [0] * range_size
        output = [0] * len(arr)
        
        for num in arr:
            count[num - min_val] += 1
        
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        
        for i in range(len(arr) - 1, -1, -1):
            output[count[arr[i] - min_val] - 1] = arr[i]
            count[arr[i] - min_val] -= 1
        
        return output
    
    @staticmethod
    def radix_sort(arr: List[int]) -> List[int]:
        """Radix Sort - O(d(n + k)) donde d es número de dígitos"""
        if not arr:
            return []
        
        arr = arr.copy()
        
        # Manejar números negativos
        min_val = min(arr)
        if min_val < 0:
            arr = [x - min_val for x in arr]
        
        def counting_sort_for_radix(arr: List[int], exp: int):
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            
            for i in range(n):
                index = arr[i] // exp
                count[index % 10] += 1
            
            for i in range(1, 10):
                count[i] += count[i - 1]
            
            i = n - 1
            while i >= 0:
                index = arr[i] // exp
                output[count[index % 10] - 1] = arr[i]
                count[index % 10] -= 1
                i -= 1
            
            for i in range(n):
                arr[i] = output[i]
        
        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            counting_sort_for_radix(arr, exp)
            exp *= 10
        
        # Restaurar valores originales si había negativos
        if min_val < 0:
            arr = [x + min_val for x in arr]
        
        return arr
    
    @staticmethod
    def get_sorting_function(algorithm_name: str) -> Callable:
        """Retorna la función de ordenamiento correspondiente"""
        algorithms = {
            'Tree Sort': SortingAlgorithms.tree_sort,
            'Bubble Sort': SortingAlgorithms.bubble_sort,
            'Selection Sort': SortingAlgorithms.selection_sort,
            'Insertion Sort': SortingAlgorithms.insertion_sort,
            'Merge Sort': SortingAlgorithms.merge_sort,
            'Quick Sort': SortingAlgorithms.quick_sort,
            'Counting Sort': SortingAlgorithms.counting_sort,
            'Radix Sort': SortingAlgorithms.radix_sort
        }
        return algorithms.get(algorithm_name) # type: ignore
    
    @staticmethod
    def get_available_algorithms() -> List[str]:
        """Retorna lista de algoritmos disponibles"""
        return [
            'Tree Sort',
            'Bubble Sort',
            'Selection Sort',
            'Insertion Sort',
            'Merge Sort',
            'Quick Sort',
            'Counting Sort',
            'Radix Sort'
        ]