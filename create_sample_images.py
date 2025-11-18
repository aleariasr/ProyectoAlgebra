#!/usr/bin/env python3
"""
Script para crear imágenes de muestra para el proyecto.
Genera imágenes sintéticas con figuras geométricas simples.
"""

import numpy as np
from PIL import Image, ImageDraw
import os


def create_sample_image_1():
    """
    Crea una imagen de muestra con círculos.
    """
    # Crear imagen RGB
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Dibujar círculos de diferentes colores
    draw.ellipse([100, 100, 300, 300], fill='red', outline='darkred', width=3)
    draw.ellipse([400, 200, 550, 350], fill='blue', outline='darkblue', width=3)
    draw.ellipse([200, 350, 400, 550], fill='green', outline='darkgreen', width=3)
    
    img.save('imagenes_muestra/imagen1_circulos.png')
    print("✓ Imagen 1 creada: imagenes_muestra/imagen1_circulos.png")
    return img


def create_sample_image_2():
    """
    Crea una imagen de muestra con rectángulos.
    """
    # Crear imagen RGB
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='lightgray')
    draw = ImageDraw.Draw(img)
    
    # Dibujar rectángulos de diferentes colores
    draw.rectangle([50, 50, 250, 200], fill='orange', outline='darkorange', width=3)
    draw.rectangle([300, 100, 600, 300], fill='purple', outline='indigo', width=3)
    draw.rectangle([100, 350, 350, 550], fill='yellow', outline='gold', width=3)
    draw.rectangle([450, 400, 700, 550], fill='cyan', outline='teal', width=3)
    
    img.save('imagenes_muestra/imagen2_rectangulos.png')
    print("✓ Imagen 2 creada: imagenes_muestra/imagen2_rectangulos.png")
    return img


def create_sample_image_3():
    """
    Crea una imagen de muestra con formas mixtas.
    """
    # Crear imagen RGB con fondo degradado
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Fondo
    for i in range(height):
        color_value = int(255 - (i / height) * 50)
        draw.line([(0, i), (width, i)], fill=(color_value, color_value, 255))
    
    # Dibujar formas mixtas
    draw.ellipse([100, 100, 350, 350], fill='pink', outline='red', width=3)
    draw.rectangle([400, 50, 700, 250], fill='lightgreen', outline='green', width=3)
    draw.polygon([(200, 400), (400, 550), (0, 550)], fill='lightyellow', outline='orange', width=3)
    draw.ellipse([500, 350, 750, 550], fill='lightblue', outline='blue', width=3)
    
    img.save('imagenes_muestra/imagen3_formas_mixtas.png')
    print("✓ Imagen 3 creada: imagenes_muestra/imagen3_formas_mixtas.png")
    return img


def create_bw_test_images():
    """
    Crea imágenes de prueba en blanco y negro para testing directo.
    """
    # Imagen BW 1: Círculos simples
    width, height = 400, 400
    img1 = Image.new('L', (width, height), color=255)
    draw1 = ImageDraw.Draw(img1)
    draw1.ellipse([50, 50, 150, 150], fill=0)
    draw1.ellipse([200, 100, 350, 250], fill=0)
    draw1.ellipse([100, 250, 200, 350], fill=0)
    img1.save('imagenes_muestra/test_bn_1.png')
    print("✓ Imagen BN 1 creada: imagenes_muestra/test_bn_1.png")
    
    # Imagen BW 2: Rectángulos
    img2 = Image.new('L', (width, height), color=255)
    draw2 = ImageDraw.Draw(img2)
    draw2.rectangle([50, 50, 150, 150], fill=0)
    draw2.rectangle([200, 50, 350, 200], fill=0)
    draw2.rectangle([50, 200, 180, 350], fill=0)
    img2.save('imagenes_muestra/test_bn_2.png')
    print("✓ Imagen BN 2 creada: imagenes_muestra/test_bn_2.png")
    
    # Imagen BW 3: Formas irregulares
    img3 = Image.new('L', (width, height), color=255)
    draw3 = ImageDraw.Draw(img3)
    draw3.polygon([(100, 50), (200, 50), (250, 150), (150, 200), (50, 150)], fill=0)
    draw3.ellipse([200, 200, 350, 350], fill=0)
    img3.save('imagenes_muestra/test_bn_3.png')
    print("✓ Imagen BN 3 creada: imagenes_muestra/test_bn_3.png")


def main():
    """
    Crea todas las imágenes de muestra.
    """
    print("\n" + "="*60)
    print("CREANDO IMÁGENES DE MUESTRA PARA EL PROYECTO")
    print("="*60 + "\n")
    
    os.makedirs('imagenes_muestra', exist_ok=True)
    
    # Crear imágenes a color
    print("Creando imágenes a color...")
    create_sample_image_1()
    create_sample_image_2()
    create_sample_image_3()
    
    print("\nCreando imágenes de prueba en blanco y negro...")
    create_bw_test_images()
    
    print("\n" + "="*60)
    print("IMÁGENES CREADAS EXITOSAMENTE")
    print("="*60)
    print("\nSe han creado las siguientes imágenes:")
    print("\nImágenes a color (para transformaciones):")
    print("  - imagenes_muestra/imagen1_circulos.png")
    print("  - imagenes_muestra/imagen2_rectangulos.png")
    print("  - imagenes_muestra/imagen3_formas_mixtas.png")
    print("\nImágenes en blanco y negro (para prueba de cálculo de área):")
    print("  - imagenes_muestra/test_bn_1.png")
    print("  - imagenes_muestra/test_bn_2.png")
    print("  - imagenes_muestra/test_bn_3.png")
    print()


if __name__ == "__main__":
    main()
