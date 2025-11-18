#!/usr/bin/env python3
"""
Transformaciones de Imágenes usando Álgebra Lineal
Este programa aplica diversas transformaciones a imágenes y muestra
las operaciones de álgebra lineal involucradas.
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys
import os


class ImageTransformer:
    """
    Clase para aplicar transformaciones de álgebra lineal a imágenes.
    """
    
    def __init__(self, image_path):
        """
        Inicializa el transformador con una imagen.
        
        Args:
            image_path: Ruta a la imagen a transformar
        """
        self.original_image = Image.open(image_path)
        self.image_path = image_path
        self.base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Convertir a matriz RGB para operaciones
        self.image_matrix = np.array(self.original_image, dtype=np.float64)
        
        print(f"Imagen cargada: {self.original_image.size}")
        print(f"Dimensiones de la matriz: {self.image_matrix.shape}")
        print(f"Tipo de imagen: {'RGB' if len(self.image_matrix.shape) == 3 else 'Escala de grises'}")
    
    def rotate_image(self, angle):
        """
        Rota una imagen usando transformaciones de matriz de rotación.
        
        Operación de Álgebra Lineal:
        Matriz de rotación 2D:
        R(θ) = [cos(θ)  -sin(θ)]
               [sin(θ)   cos(θ)]
        
        Cada píxel (x,y) se transforma usando: [x'] = R(θ) * [x]
                                                [y']         [y]
        
        Args:
            angle: Ángulo de rotación en grados
            
        Returns:
            PIL.Image: Imagen rotada
        """
        print(f"\n{'='*60}")
        print(f"ROTACIÓN - Ángulo: {angle}°")
        print(f"{'='*60}")
        
        # Convertir ángulo a radianes
        theta = np.radians(angle)
        
        # Matriz de rotación (Álgebra Lineal)
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])
        
        print("\nMatriz de Rotación:")
        print(rotation_matrix)
        print("\nExplicación:")
        print("Esta es una matriz de rotación 2D que transforma las coordenadas")
        print("de cada píxel aplicando la operación matricial [x', y'] = R(θ) * [x, y]")
        
        # PIL tiene rotación incorporada, pero mostramos el concepto
        rotated_image = self.original_image.rotate(-angle, expand=True)
        
        output_path = f"{self.base_name}_rotacion_{angle}.png"
        rotated_image.save(output_path)
        print(f"\nImagen guardada: {output_path}")
        
        return rotated_image
    
    def resize_image(self, scale_factor):
        """
        Cambia el tamaño de la imagen usando escalamiento matricial.
        
        Operación de Álgebra Lineal:
        Matriz de escalamiento:
        S(s) = [s  0]
               [0  s]
        
        Cada píxel (x,y) se transforma: [x'] = S(s) * [x]
                                         [y']         [y]
        
        Args:
            scale_factor: Factor de escala (ej: 0.5 para 50%, 2.0 para 200%)
            
        Returns:
            PIL.Image: Imagen redimensionada
        """
        print(f"\n{'='*60}")
        print(f"CAMBIO DE TAMAÑO - Factor: {scale_factor}x")
        print(f"{'='*60}")
        
        # Matriz de escalamiento (Álgebra Lineal)
        scaling_matrix = np.array([
            [scale_factor, 0],
            [0, scale_factor]
        ])
        
        print("\nMatriz de Escalamiento:")
        print(scaling_matrix)
        print("\nExplicación:")
        print("Esta matriz de escalamiento multiplica las coordenadas de cada píxel")
        print("por el factor de escala, expandiendo o contrayendo la imagen")
        
        new_width = int(self.original_image.width * scale_factor)
        new_height = int(self.original_image.height * scale_factor)
        
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        output_path = f"{self.base_name}_tamano_{scale_factor}x.png"
        resized_image.save(output_path)
        print(f"\nTamaño original: {self.original_image.size}")
        print(f"Tamaño nuevo: {resized_image.size}")
        print(f"Imagen guardada: {output_path}")
        
        return resized_image
    
    def adjust_contrast(self, factor):
        """
        Ajusta el contraste de la imagen usando operaciones matriciales.
        
        Operación de Álgebra Lineal:
        Para cada píxel p en la matriz de imagen:
        p' = factor * (p - 128) + 128
        
        Esto es una transformación afín que escala los valores alrededor del punto medio.
        
        Args:
            factor: Factor de contraste (>1 aumenta, <1 disminuye)
            
        Returns:
            PIL.Image: Imagen con contraste ajustado
        """
        print(f"\n{'='*60}")
        print(f"AJUSTE DE CONTRASTE - Factor: {factor}")
        print(f"{'='*60}")
        
        print("\nOperación de Álgebra Lineal:")
        print(f"Para cada píxel p: p' = {factor} * (p - 128) + 128")
        print("\nExplicación:")
        print("Esta transformación afín escala los valores de intensidad alrededor")
        print("del punto medio (128), aumentando o disminuyendo el contraste")
        
        # Aplicar operación vectorizada usando NumPy
        image_array = np.array(self.original_image, dtype=np.float64)
        
        # Transformación afín (Álgebra Lineal)
        adjusted = factor * (image_array - 128) + 128
        
        # Recortar valores al rango válido [0, 255]
        adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
        
        contrast_image = Image.fromarray(adjusted)
        
        output_path = f"{self.base_name}_contraste_{factor}.png"
        contrast_image.save(output_path)
        print(f"Imagen guardada: {output_path}")
        
        return contrast_image
    
    def convert_to_grayscale(self):
        """
        Convierte imagen a escala de grises usando combinación lineal de canales RGB.
        
        Operación de Álgebra Lineal:
        Gray = [0.299  0.587  0.114] * [R]
                                        [G]
                                        [B]
        
        Esta es una combinación lineal de los canales RGB basada en la
        percepción humana de luminosidad.
        
        Returns:
            PIL.Image: Imagen en escala de grises
        """
        print(f"\n{'='*60}")
        print("CONVERSIÓN A ESCALA DE GRISES")
        print(f"{'='*60}")
        
        # Vector de pesos para conversión (Álgebra Lineal)
        weights = np.array([0.299, 0.587, 0.114])
        
        print("\nVector de pesos para conversión:")
        print(f"R: {weights[0]}")
        print(f"G: {weights[1]}")
        print(f"B: {weights[2]}")
        print("\nOperación de Álgebra Lineal:")
        print("Gray = 0.299*R + 0.587*G + 0.114*B")
        print("\nExplicación:")
        print("Esta es una combinación lineal (producto punto) de los canales RGB")
        print("Los pesos reflejan la sensibilidad del ojo humano a diferentes colores")
        
        # Si ya está en escala de grises
        if len(self.image_matrix.shape) == 2:
            print("\nLa imagen ya está en escala de grises")
            gray_image = self.original_image
        else:
            # Aplicar combinación lineal usando producto punto
            image_array = np.array(self.original_image, dtype=np.float64)
            gray_array = np.dot(image_array[...,:3], weights)
            gray_array = gray_array.astype(np.uint8)
            
            gray_image = Image.fromarray(gray_array)
        
        output_path = f"{self.base_name}_grises.png"
        gray_image.save(output_path)
        print(f"Imagen guardada: {output_path}")
        
        return gray_image
    
    def convert_to_bw(self, threshold=128):
        """
        Convierte imagen a blanco y negro puro usando función umbral.
        
        Operación de Álgebra Lineal:
        Para cada píxel p:
        p' = 255 si p > threshold
        p' = 0   si p ≤ threshold
        
        Esta es una función de paso (step function) aplicada elemento por elemento.
        
        Args:
            threshold: Umbral para binarización (0-255)
            
        Returns:
            PIL.Image: Imagen en blanco y negro
        """
        print(f"\n{'='*60}")
        print(f"CONVERSIÓN A BLANCO Y NEGRO - Umbral: {threshold}")
        print(f"{'='*60}")
        
        print("\nOperación de Álgebra Lineal:")
        print(f"Para cada píxel p:")
        print(f"  p' = 255 si p > {threshold}")
        print(f"  p' = 0   si p ≤ {threshold}")
        print("\nExplicación:")
        print("Esta es una función de paso (step function) que binariza la imagen")
        print("aplicándose elemento por elemento a la matriz de píxeles")
        
        # Primero convertir a escala de grises si es necesario
        if len(self.image_matrix.shape) == 3:
            gray_image = self.original_image.convert('L')
        else:
            gray_image = self.original_image
        
        gray_array = np.array(gray_image, dtype=np.float64)
        
        # Aplicar umbral (operación vectorizada)
        bw_array = (gray_array > threshold).astype(np.uint8) * 255
        
        bw_image = Image.fromarray(bw_array)
        
        output_path = f"{self.base_name}_bn_{threshold}.png"
        bw_image.save(output_path)
        print(f"Imagen guardada: {output_path}")
        
        return bw_image
    
    def apply_all_transformations(self):
        """
        Aplica todas las transformaciones a la imagen y guarda los resultados.
        """
        print(f"\n{'#'*60}")
        print(f"APLICANDO TODAS LAS TRANSFORMACIONES")
        print(f"Imagen: {self.image_path}")
        print(f"{'#'*60}\n")
        
        results = {}
        
        # 1. Rotación
        results['rotation'] = self.rotate_image(45)
        
        # 2. Cambio de tamaño
        results['resize'] = self.resize_image(0.5)
        
        # 3. Ajuste de contraste
        results['contrast'] = self.adjust_contrast(1.5)
        
        # 4. Conversión a escala de grises
        results['grayscale'] = self.convert_to_grayscale()
        
        # 5. Conversión a blanco y negro
        results['bw'] = self.convert_to_bw(128)
        
        print(f"\n{'#'*60}")
        print("TRANSFORMACIONES COMPLETADAS")
        print(f"{'#'*60}\n")
        
        return results
    
    def create_comparison_figure(self):
        """
        Crea una figura con todas las transformaciones para comparación visual.
        """
        results = self.apply_all_transformations()
        
        # Crear figura con subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Transformaciones de Imagen usando Álgebra Lineal', fontsize=16)
        
        # Imagen original
        axes[0, 0].imshow(self.original_image)
        axes[0, 0].set_title('Original')
        axes[0, 0].axis('off')
        
        # Rotación
        axes[0, 1].imshow(results['rotation'])
        axes[0, 1].set_title('Rotación 45°')
        axes[0, 1].axis('off')
        
        # Cambio de tamaño
        axes[0, 2].imshow(results['resize'])
        axes[0, 2].set_title('Tamaño 0.5x')
        axes[0, 2].axis('off')
        
        # Contraste
        axes[1, 0].imshow(results['contrast'])
        axes[1, 0].set_title('Contraste 1.5x')
        axes[1, 0].axis('off')
        
        # Escala de grises
        axes[1, 1].imshow(results['grayscale'], cmap='gray')
        axes[1, 1].set_title('Escala de Grises')
        axes[1, 1].axis('off')
        
        # Blanco y Negro
        axes[1, 2].imshow(results['bw'], cmap='gray')
        axes[1, 2].set_title('Blanco y Negro')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        output_path = f"{self.base_name}_comparacion.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\nFigura de comparación guardada: {output_path}")
        
        return output_path


def main():
    """
    Función principal del programa.
    """
    if len(sys.argv) < 2:
        print("Uso: python image_transformations.py <ruta_imagen>")
        print("\nEjemplo:")
        print("  python image_transformations.py imagen.jpg")
        print("\nEste programa aplica las siguientes transformaciones:")
        print("  1. Rotación (45 grados)")
        print("  2. Cambio de tamaño (50%)")
        print("  3. Ajuste de contraste (1.5x)")
        print("  4. Conversión a escala de grises")
        print("  5. Conversión a blanco y negro")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: No se encontró el archivo '{image_path}'")
        sys.exit(1)
    
    try:
        transformer = ImageTransformer(image_path)
        transformer.create_comparison_figure()
        
        print("\n" + "="*60)
        print("PROCESO COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("\nSe han generado las siguientes imágenes:")
        print(f"  - {transformer.base_name}_rotacion_45.png")
        print(f"  - {transformer.base_name}_tamano_0.5x.png")
        print(f"  - {transformer.base_name}_contraste_1.5.png")
        print(f"  - {transformer.base_name}_grises.png")
        print(f"  - {transformer.base_name}_bn_128.png")
        print(f"  - {transformer.base_name}_comparacion.png")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
