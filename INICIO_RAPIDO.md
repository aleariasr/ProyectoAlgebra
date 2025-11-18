# Guía Rápida de Inicio

## Instalación en 3 Pasos

### Paso 1: Verificar Python
```bash
python3 --version
```
Debe mostrar Python 3.7 o superior.

### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Crear Imágenes de Muestra
```bash
python3 create_sample_images.py
```

¡Listo! Ya puede usar el programa.

---

## Uso Rápido

### Opción 1: Ejecutar Demo Completo
```bash
python3 run_complete_demo.py
```
Esto ejecuta todas las funcionalidades automáticamente.

### Opción 2: Uso Individual

#### Aplicar Transformaciones
```bash
python3 image_transformations.py imagenes_muestra/imagen1_circulos.png
```

Genera 6 archivos:
- `imagen1_circulos_rotacion_45.png`
- `imagen1_circulos_tamano_0.5x.png`
- `imagen1_circulos_contraste_1.5.png`
- `imagen1_circulos_grises.png`
- `imagen1_circulos_bn_128.png`
- `imagen1_circulos_comparacion.png`

#### Calcular Áreas
```bash
python3 image_area_calculator.py imagenes_muestra/test_bn_1.png
```

Muestra:
- Número de objetos encontrados
- Área de cada objeto en píxeles
- Porcentaje de la imagen ocupado
- Genera imagen etiquetada

---

## Comandos Más Usados

### Con Imágenes de Muestra

**Transformar las 3 imágenes:**
```bash
python3 image_transformations.py imagenes_muestra/imagen1_circulos.png
python3 image_transformations.py imagenes_muestra/imagen2_rectangulos.png
python3 image_transformations.py imagenes_muestra/imagen3_formas_mixtas.png
```

**Calcular áreas en las 3 imágenes BN:**
```bash
python3 image_area_calculator.py imagenes_muestra/test_bn_1.png
python3 image_area_calculator.py imagenes_muestra/test_bn_2.png
python3 image_area_calculator.py imagenes_muestra/test_bn_3.png
```

### Con Tus Propias Imágenes

**Transformar tu imagen:**
```bash
python3 image_transformations.py /ruta/a/tu/imagen.jpg
```

**Calcular área (imagen debe estar en blanco y negro):**
```bash
python3 image_area_calculator.py /ruta/a/tu/imagen_bn.png
```

**Calcular área con umbral personalizado:**
```bash
python3 image_area_calculator.py imagen.png 150
```
(El número es el umbral: 0-255, default=128)

---

## Flujo de Trabajo Típico

### Preparación del Documento Escrito

1. **Generar todas las imágenes:**
   ```bash
   python3 run_complete_demo.py
   ```

2. **Tomar capturas de pantalla:**
   - Imágenes originales (carpeta `imagenes_muestra/`)
   - Imágenes transformadas (archivos `*_rotacion_*.png`, etc.)
   - Resultados en terminal
   - Imágenes etiquetadas (`*_labeled.png`)

3. **Abrir `GUIA_TRABAJO_ESCRITO.md`** para seguir la estructura

### Preparación del Video

1. **Leer `GUIA_VIDEO.md`** completamente

2. **Preparar el entorno:**
   ```bash
   # Terminal en pantalla completa
   cd ProyectoAlgebra
   clear
   # Aumentar tamaño de fuente del terminal
   ```

3. **Tener archivos abiertos en editor:**
   - `image_transformations.py`
   - `image_area_calculator.py`

4. **Practicar el guion** una vez antes de grabar

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'numpy'"
**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "No such file or directory: 'imagen.png'"
**Solución:**
- Verificar que la ruta es correcta
- Usar rutas completas si es necesario
- Verificar que el archivo existe: `ls -la imagen.png`

### Las áreas calculadas parecen incorrectas
**Solución:**
- Ajustar el umbral: `python3 image_area_calculator.py imagen.png 150`
- Verificar que la imagen esté en blanco y negro
- Probar con diferentes valores de umbral (50, 100, 128, 150, 200)

### La imagen transformada no se ve bien
**Solución:**
- Las transformaciones están preconfiguradas
- Para personalizar, editar `image_transformations.py`
- Cambiar parámetros en las funciones (ángulo, factor, etc.)

---

## Archivos Importantes

### Programas Principales
- **`image_area_calculator.py`**: Calcula áreas de objetos
- **`image_transformations.py`**: Aplica transformaciones

### Utilidades
- **`create_sample_images.py`**: Genera imágenes de prueba
- **`run_complete_demo.py`**: Ejecuta demo completo

### Documentación
- **`README.md`**: Documentación completa del proyecto
- **`GUIA_TRABAJO_ESCRITO.md`**: Guía para el documento escrito
- **`GUIA_VIDEO.md`**: Guía para el video explicativo
- **`INICIO_RAPIDO.md`**: Este archivo

### Configuración
- **`requirements.txt`**: Dependencias de Python
- **`.gitignore`**: Archivos a excluir de Git

---

## Atajos Útiles

### Ver ayuda de un programa
```bash
python3 image_area_calculator.py
python3 image_transformations.py
```
(Sin argumentos muestra la ayuda)

### Listar imágenes generadas
```bash
ls -lh *.png
ls -lh imagenes_muestra/
```

### Limpiar imágenes generadas
```bash
# ¡CUIDADO! Esto borra todas las imágenes generadas
rm -f *_rotacion_*.png *_tamano_*.png *_contraste_*.png
rm -f *_grises.png *_bn_*.png *_comparacion.png *_labeled.png
```

### Ver imagen en terminal (si soporta)
```bash
# En algunos terminales modernos
imgcat imagen.png  # macOS iTerm2
catimg imagen.png  # Linux con catimg instalado
```

---

## Checklist del Proyecto

### Para el Trabajo Escrito (7.5%)
- [ ] Portada con nombres y fecha
- [ ] Introducción al proyecto
- [ ] Índice
- [ ] Selección de 3 imágenes a color
- [ ] Capturas de código de cada transformación
- [ ] Explicación de operaciones de álgebra lineal
- [ ] Imágenes resultantes de cada transformación
- [ ] Código del programa de cálculo de áreas
- [ ] Resultados en las 3 imágenes
- [ ] Conclusiones y limitaciones
- [ ] Documento en formato PDF

### Para el Video (7.5%)
- [ ] Saludo e introducción (1 min)
- [ ] Demostración de transformaciones en vivo (5-6 min)
- [ ] Explicación de cada código
- [ ] Ejecución del programa de áreas (3-4 min)
- [ ] Prueba con las 3 imágenes
- [ ] Cierre (1 min)
- [ ] Duración total: 8-12 minutos
- [ ] Buena calidad de audio y video

### Para el Programa (5%)
- [ ] Todos los códigos incluidos
- [ ] Código comentado y documentado
- [ ] Funciona correctamente
- [ ] Incluye requirements.txt
- [ ] Incluye README.md
- [ ] Incluye imágenes de muestra

### Para la Entrega
- [ ] Documento PDF del trabajo escrito
- [ ] Video explicativo (MP4 o similar)
- [ ] Carpeta con todos los programas
- [ ] Imágenes de muestra incluidas
- [ ] Todo comprimido en archivo ZIP
- [ ] Nombre del archivo: `Apellido1_Apellido2_ProyectoAlgebra.zip`
- [ ] Subido a Mediación Virtual antes de la fecha límite

---

## Contacto y Recursos

### Recursos de Aprendizaje
- NumPy: https://numpy.org/doc/stable/user/quickstart.html
- Pillow: https://pillow.readthedocs.io/en/stable/
- Álgebra Lineal: Khan Academy (español)

### Comandos de Ayuda
```bash
# Ver documentación de NumPy
python3 -c "import numpy; help(numpy.array)"

# Ver información de las librerías instaladas
pip list

# Actualizar una librería
pip install --upgrade numpy
```

---

## Últimos Consejos

1. **Empezar temprano**: No dejar para el último día
2. **Probar todo**: Ejecutar cada comando al menos una vez
3. **Hacer respaldo**: Guardar copias del trabajo
4. **Pedir ayuda**: Si algo no funciona, preguntar
5. **Revisar rúbrica**: Asegurarse de cumplir todos los requisitos
6. **Practicar video**: Hacer una prueba antes de la grabación final

---

**¡Éxito con el proyecto!**
