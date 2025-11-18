#!/bin/bash
echo "=========================================="
echo "VERIFICACIÓN FINAL DEL PROYECTO"
echo "=========================================="
echo ""

echo "1. Verificando instalación de dependencias..."
python3 -c "import numpy; import PIL; import matplotlib; print('✓ Todas las dependencias instaladas')"

echo ""
echo "2. Probando generación de imágenes..."
python3 create_sample_images.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Generación de imágenes: OK"
else
    echo "✗ Error en generación de imágenes"
fi

echo ""
echo "3. Probando transformaciones..."
python3 image_transformations.py imagenes_muestra/imagen1_circulos.png > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Transformaciones: OK"
else
    echo "✗ Error en transformaciones"
fi

echo ""
echo "4. Probando cálculo de áreas..."
python3 image_area_calculator.py imagenes_muestra/test_bn_1.png > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Cálculo de áreas: OK"
else
    echo "✗ Error en cálculo de áreas"
fi

echo ""
echo "5. Verificando archivos de documentación..."
docs=("README.md" "GUIA_TRABAJO_ESCRITO.md" "GUIA_VIDEO.md" "INICIO_RAPIDO.md" "RESUMEN_PROYECTO.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "✓ $doc"
    else
        echo "✗ Falta $doc"
    fi
done

echo ""
echo "=========================================="
echo "VERIFICACIÓN COMPLETADA"
echo "=========================================="
