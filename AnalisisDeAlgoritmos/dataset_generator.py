# dataset_generator.py
import os
import json
import string
from typing import List, Any


class DatasetGenerator:
    """Genera y gestiona conjuntos de datos de diferentes tipos"""
    
    DATASET_DIR = "datasets"
    
    @staticmethod
    def ensure_dataset_dir():
        if not os.path.exists(DatasetGenerator.DATASET_DIR):
            os.makedirs(DatasetGenerator.DATASET_DIR)
    
    @staticmethod
    def generate_int_dataset(max_size: int = 15) -> List[List[int]]:
        """Genera conjuntos de enteros escalables"""
        datasets = []
        size = 1
        for i in range(max_size):
            data = list(range(size))
            datasets.append(data)
            size = size * 2 + size // 2
        return datasets
    
    @staticmethod
    def generate_float_dataset(max_size: int = 15) -> List[List[float]]:
        """Genera conjuntos de flotantes escalables"""
        datasets = []
        size = 1
        for i in range(max_size):
            data = [float(x) * 1.5 for x in range(size)]
            datasets.append(data)
            size = size * 2 + size // 2
        return datasets
    
    @staticmethod
    def generate_string_dataset(max_size: int = 15) -> List[List[str]]:
        """Genera conjuntos de strings escalables"""
        datasets = []
        size = 1
        chars = string.ascii_lowercase
        for i in range(max_size):
            data = []
            for j in range(size):
                str_len = (j % 10) + 1
                random_str = ''.join([chars[(j * k) % len(chars)] for k in range(str_len)])
                data.append(random_str)
            datasets.append(data)
            size = size * 2 + size // 2
        return datasets
    
    @staticmethod
    def save_dataset(data_type: str, datasets: List[List[Any]]):
        """Guarda el conjunto de datos en archivo JSON"""
        DatasetGenerator.ensure_dataset_dir()
        filename = os.path.join(DatasetGenerator.DATASET_DIR, f"{data_type}.json")
        with open(filename, 'w') as f:
            json.dump(datasets, f)
    
    @staticmethod
    def load_dataset(data_type: str) -> List[List[Any]]:
        """Carga el conjunto de datos desde archivo JSON"""
        filename = os.path.join(DatasetGenerator.DATASET_DIR, f"{data_type}.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None # type: ignore
    
    @staticmethod
    def get_or_create_dataset(data_type: str) -> List[List[Any]]:
        """Obtiene o crea un conjunto de datos"""
        dataset = DatasetGenerator.load_dataset(data_type)
        if dataset is not None:
            return dataset
        
        if data_type == "int":
            dataset = DatasetGenerator.generate_int_dataset()
        elif data_type == "float":
            dataset = DatasetGenerator.generate_float_dataset()
        elif data_type == "string":
            dataset = DatasetGenerator.generate_string_dataset()
        else:
            raise ValueError(f"Tipo de dato no soportado: {data_type}")
        
        DatasetGenerator.save_dataset(data_type, dataset)
        return dataset