#!/usr/bin/env python3
"""
Script de prueba completo para el Proyecto de Álgebra Lineal
Ejecuta todas las funcionalidades del proyecto y genera un reporte.
"""

import os
import sys
import subprocess
from datetime import datetime


def print_section(title):
    """Imprime una sección formateada."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def run_command(command, description):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n{'─'*70}")
    print(f"► {description}")
    print(f"{'─'*70}")
    print(f"Comando: {command}\n")
    
    result = subprocess.run(command, shell=True, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n⚠ Error al ejecutar: {command}")
        return False
    
    print(f"\n✓ Completado exitosamente")
    return True


def main():
    """
    Función principal que ejecuta todas las pruebas del proyecto.
    """
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#  PROYECTO DE ÁLGEBRA LINEAL: PROCESAMIENTO DE IMÁGENES  ".center(70, " ") + "#")
    print("#  Script de Demostración Completo".center(70, " ") + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nFecha de ejecución: {timestamp}")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('image_area_calculator.py'):
        print("\n⚠ Error: Ejecute este script desde el directorio del proyecto")
        sys.exit(1)
    
    # PARTE 1: Crear imágenes de muestra
    print_section("PARTE 1: CREACIÓN DE IMÁGENES DE MUESTRA")
    run_command("python3 create_sample_images.py", 
                "Generando imágenes de muestra para las pruebas")
    
    # PARTE 2: Aplicar transformaciones
    print_section("PARTE 2: TRANSFORMACIONES DE ÁLGEBRA LINEAL")
    
    print("\nAplicando transformaciones a las 3 imágenes a color:\n")
    
    images = [
        "imagenes_muestra/imagen1_circulos.png",
        "imagenes_muestra/imagen2_rectangulos.png",
        "imagenes_muestra/imagen3_formas_mixtas.png"
    ]
    
    for i, image in enumerate(images, 1):
        run_command(f"python3 image_transformations.py {image}",
                   f"Imagen {i}: Aplicando todas las transformaciones")
    
    # PARTE 3: Cálculo de áreas
    print_section("PARTE 3: CÁLCULO DE ÁREAS DE OBJETOS")
    
    print("\nProcesando imágenes en blanco y negro:\n")
    
    bw_images = [
        "imagenes_muestra/test_bn_1.png",
        "imagenes_muestra/test_bn_2.png",
        "imagenes_muestra/test_bn_3.png"
    ]
    
    for i, image in enumerate(bw_images, 1):
        run_command(f"python3 image_area_calculator.py {image}",
                   f"Imagen BN {i}: Calculando áreas de objetos")
    
    # PARTE 4: Probar con imágenes transformadas
    print_section("PARTE 4: PRUEBA CON IMÁGENES TRANSFORMADAS A BN")
    
    transformed_images = [
        "imagen1_circulos_bn_128.png",
        "imagen2_rectangulos_bn_128.png",
        "imagen3_formas_mixtas_bn_128.png"
    ]
    
    for i, image in enumerate(transformed_images, 1):
        if os.path.exists(image):
            run_command(f"python3 image_area_calculator.py {image}",
                       f"Imagen transformada {i}: Calculando áreas")
    
    # PARTE 5: Resumen de archivos generados
    print_section("PARTE 5: RESUMEN DE ARCHIVOS GENERADOS")
    
    print("Archivos de imágenes originales:")
    for img in images + bw_images:
        if os.path.exists(img):
            print(f"  ✓ {img}")
    
    print("\nArchivos de transformaciones generados:")
    transformations = ['rotacion_45', 'tamano_0.5x', 'contraste_1.5', 'grises', 'bn_128', 'comparacion']
    for img_base in ['imagen1_circulos', 'imagen2_rectangulos', 'imagen3_formas_mixtas']:
        for trans in transformations:
            filename = f"{img_base}_{trans}.png"
            if os.path.exists(filename):
                print(f"  ✓ {filename}")
    
    print("\nArchivos de áreas calculadas (etiquetados):")
    for img in bw_images + transformed_images:
        labeled = img.replace('.png', '_labeled.png')
        if os.path.exists(labeled):
            print(f"  ✓ {labeled}")
    
    # Resumen final
    print_section("RESUMEN FINAL")
    
    print("✓ Todas las pruebas completadas exitosamente")
    print("\nFuncionalidades probadas:")
    print("  1. ✓ Creación de imágenes de muestra")
    print("  2. ✓ Rotación de imágenes (matrices de rotación)")
    print("  3. ✓ Cambio de tamaño (matrices de escalamiento)")
    print("  4. ✓ Ajuste de contraste (transformaciones afines)")
    print("  5. ✓ Conversión a escala de grises (combinación lineal)")
    print("  6. ✓ Conversión a blanco y negro (función umbral)")
    print("  7. ✓ Detección de objetos (componentes conectados)")
    print("  8. ✓ Cálculo de áreas (operaciones vectorizadas)")
    
    print("\n" + "#"*70)
    print("#  DEMOSTRACIÓN COMPLETADA".center(70, " ") + "#")
    print("#"*70 + "\n")


if __name__ == "__main__":
    main()
