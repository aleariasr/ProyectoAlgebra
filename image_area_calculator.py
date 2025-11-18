#!/usr/bin/env python3
"""
Calculadora de Área de Objetos en Imágenes en Blanco y Negro
Utiliza álgebra lineal para procesar imágenes y calcular áreas de objetos.
"""

import numpy as np
from PIL import Image
import sys
import os


class ImageAreaCalculator:
    """
    Clase para procesar imágenes en blanco y negro y calcular áreas de objetos
    utilizando conceptos de álgebra lineal.
    """
    
    def __init__(self, threshold=128):
        """
        Inicializa el calculador de áreas.
        
        Args:
            threshold: Umbral para binarización de la imagen (0-255)
        """
        self.threshold = threshold
        self.image_matrix = None
        self.binary_matrix = None
        self.labeled_matrix = None
        self.areas = {}
        
    def load_image(self, image_path):
        """
        Carga una imagen y la convierte en una matriz usando álgebra lineal.
        
        Args:
            image_path: Ruta al archivo de imagen
            
        Returns:
            numpy.ndarray: Matriz que representa la imagen
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No se encontró el archivo: {image_path}")
        
        # Cargar imagen y convertir a escala de grises
        img = Image.open(image_path).convert('L')
        
        # Convertir a matriz NumPy (álgebra lineal)
        self.image_matrix = np.array(img, dtype=np.float64)
        
        print(f"Imagen cargada: {img.size[0]}x{img.size[1]} píxeles")
        print(f"Dimensiones de la matriz: {self.image_matrix.shape}")
        
        return self.image_matrix
    
    def binarize(self):
        """
        Binariza la imagen usando operaciones matriciales.
        Aplica un umbral para convertir la imagen en blanco y negro puro.
        Los objetos oscuros (píxeles < umbral) se marcan como 1.
        
        Returns:
            numpy.ndarray: Matriz binaria (0s y 1s)
        """
        if self.image_matrix is None:
            raise ValueError("Primero debe cargar una imagen")
        
        # Operación matricial: aplicar función umbral
        # Usa álgebra lineal vectorizada para eficiencia
        # Los píxeles oscuros (objetos) se marcan como 1
        self.binary_matrix = (self.image_matrix < self.threshold).astype(np.int32)
        
        print(f"Imagen binarizada con umbral {self.threshold}")
        return self.binary_matrix
    
    def find_connected_components(self):
        """
        Encuentra componentes conectados usando búsqueda en profundidad (DFS)
        con operaciones matriciales.
        
        Returns:
            numpy.ndarray: Matriz con etiquetas de componentes
        """
        if self.binary_matrix is None:
            raise ValueError("Primero debe binarizar la imagen")
        
        rows, cols = self.binary_matrix.shape
        self.labeled_matrix = np.zeros((rows, cols), dtype=np.int32)
        label = 0
        
        def dfs(r, c, label):
            """Búsqueda en profundidad para etiquetar componentes conectados"""
            # Usar una pila para evitar recursión profunda
            stack = [(r, c)]
            
            while stack:
                curr_r, curr_c = stack.pop()
                
                # Verificar límites y si ya fue visitado
                if (curr_r < 0 or curr_r >= rows or 
                    curr_c < 0 or curr_c >= cols or
                    self.binary_matrix[curr_r, curr_c] == 0 or
                    self.labeled_matrix[curr_r, curr_c] != 0):
                    continue
                
                # Etiquetar el píxel actual
                self.labeled_matrix[curr_r, curr_c] = label
                
                # Agregar vecinos (conectividad 8)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr != 0 or dc != 0:
                            stack.append((curr_r + dr, curr_c + dc))
        
        # Recorrer toda la matriz para encontrar componentes
        for i in range(rows):
            for j in range(cols):
                if self.binary_matrix[i, j] == 1 and self.labeled_matrix[i, j] == 0:
                    label += 1
                    dfs(i, j, label)
        
        print(f"Se encontraron {label} objetos en la imagen")
        return self.labeled_matrix
    
    def calculate_areas(self):
        """
        Calcula el área de cada objeto usando operaciones de álgebra lineal.
        El área se calcula contando los píxeles de cada componente.
        
        Returns:
            dict: Diccionario con áreas de cada objeto {label: area}
        """
        if self.labeled_matrix is None:
            raise ValueError("Primero debe encontrar los componentes conectados")
        
        # Usar operaciones vectorizadas de NumPy para contar píxeles
        unique_labels = np.unique(self.labeled_matrix)
        unique_labels = unique_labels[unique_labels > 0]  # Excluir fondo (0)
        
        self.areas = {}
        for label in unique_labels:
            # Operación matricial: contar elementos que coinciden con la etiqueta
            area = np.sum(self.labeled_matrix == label)
            self.areas[label] = area
        
        return self.areas
    
    def process_image(self, image_path):
        """
        Procesa una imagen completa: carga, binariza, encuentra objetos y calcula áreas.
        
        Args:
            image_path: Ruta al archivo de imagen
            
        Returns:
            dict: Diccionario con áreas de cada objeto
        """
        print(f"\n{'='*60}")
        print(f"Procesando imagen: {image_path}")
        print(f"{'='*60}\n")
        
        self.load_image(image_path)
        self.binarize()
        self.find_connected_components()
        areas = self.calculate_areas()
        
        return areas
    
    def print_results(self):
        """
        Imprime los resultados del análisis de la imagen.
        """
        if not self.areas:
            print("No se encontraron objetos en la imagen")
            return
        
        print(f"\n{'='*60}")
        print("RESULTADOS DEL ANÁLISIS")
        print(f"{'='*60}\n")
        
        total_area = sum(self.areas.values())
        total_pixels = self.image_matrix.size
        
        print(f"Total de objetos encontrados: {len(self.areas)}")
        print(f"Área total de objetos: {total_area} píxeles")
        print(f"Tamaño de la imagen: {total_pixels} píxeles")
        print(f"Porcentaje ocupado: {(total_area/total_pixels)*100:.2f}%\n")
        
        print("Detalle por objeto:")
        print("-" * 60)
        for label, area in sorted(self.areas.items(), key=lambda x: x[1], reverse=True):
            percentage = (area / total_area) * 100
            print(f"Objeto {label}: {area} píxeles ({percentage:.2f}% del total de objetos)")
        
        print(f"\n{'='*60}\n")
    
    def save_labeled_image(self, output_path):
        """
        Guarda una visualización de los objetos etiquetados.
        
        Args:
            output_path: Ruta donde guardar la imagen
        """
        if self.labeled_matrix is None:
            raise ValueError("Primero debe procesar una imagen")
        
        # Normalizar las etiquetas para visualización
        if self.labeled_matrix.max() > 0:
            normalized = (self.labeled_matrix * 255 / self.labeled_matrix.max()).astype(np.uint8)
        else:
            normalized = self.labeled_matrix.astype(np.uint8)
        
        img = Image.fromarray(normalized)
        img.save(output_path)
        print(f"Imagen etiquetada guardada en: {output_path}")


def main():
    """
    Función principal del programa.
    """
    if len(sys.argv) < 2:
        print("Uso: python image_area_calculator.py <ruta_imagen> [umbral]")
        print("\nEjemplo:")
        print("  python image_area_calculator.py imagen.png")
        print("  python image_area_calculator.py imagen.jpg 150")
        print("\nParámetros:")
        print("  ruta_imagen: Ruta al archivo de imagen en blanco y negro")
        print("  umbral: (Opcional) Valor de umbral para binarización (0-255, default=128)")
        sys.exit(1)
    
    image_path = sys.argv[1]
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 128
    
    try:
        # Crear calculador y procesar imagen
        calculator = ImageAreaCalculator(threshold=threshold)
        calculator.process_image(image_path)
        calculator.print_results()
        
        # Guardar imagen etiquetada si hay objetos
        if calculator.areas:
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_labeled.png"
            calculator.save_labeled_image(output_path)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
