# Proyecto de Álgebra Lineal: Procesamiento de Imágenes

## Descripción del Proyecto

Este proyecto utiliza conceptos de **álgebra lineal** para procesar imágenes y aplicar transformaciones matemáticas. Incluye una aplicación GUI interactiva para explorar transformaciones de imágenes, así como herramientas para calcular áreas de objetos en imágenes binarias.

## Contenido del Proyecto

### 1. Programas Principales

#### `simple_image_lab.py` ⭐ NUEVO - Aplicación GUI Interactiva
Aplicación gráfica completa que permite:
- **Importar imágenes** desde tu computadora
- **Explorar y seleccionar** imágenes para transformar
- **Aplicar transformaciones** con álgebra lineal:
  - Rotación (matriz de rotación 2D)
  - Redimensionamiento (matriz de escalamiento)
  - Ajuste de contraste y brillo (transformación afín)
  - Conversión a escala de grises (combinación lineal RGB)
  - Binarización automática (método de Otsu)
  - Binarización con umbral fijo
- **Previsualización en tiempo real** de las imágenes
- **Guardar todas las transformaciones** con documentación automática
- **Calcular áreas** de objetos en imágenes binarias

**Características de la interfaz:**
- 📁 Carga múltiples imágenes fácilmente
- 👁️ Previsualización de original y binaria
- ⚙️ Controles para ajustar parámetros
- 📝 Log de actividad en tiempo real
- 💾 Exporta transformaciones con documentación de álgebra lineal

**Uso:**
```bash
python simple_image_lab.py
```

Luego:
1. Haz clic en "📁 Abrir imágenes..." para seleccionar imágenes de tu computadora
2. Selecciona una imagen de la lista para previsualizar
3. Ajusta los parámetros de transformación según necesites
4. Haz clic en "💾 Guardar todas las transformaciones"

**Salida generada:**
- `outputs/<nombre_imagen>/00_original.png` - Imagen original
- `outputs/<nombre_imagen>/01_rotada.png` - Rotación aplicada
- `outputs/<nombre_imagen>/02_resized.png` - Redimensionamiento
- `outputs/<nombre_imagen>/03_grises.png` - Escala de grises
- `outputs/<nombre_imagen>/04_contraste.png` - Contraste ajustado
- `outputs/<nombre_imagen>/05_binaria_otsu.png` - Binarización Otsu
- `outputs/<nombre_imagen>/06_blanco_negro.png` - Umbral fijo
- `outputs/<nombre_imagen>/README_TRANSFORMACIONES.txt` - Documentación completa con:
  - Código utilizado para cada transformación
  - Operación de álgebra lineal involucrada
  - Explicación matemática detallada

---

#### `image_area_calculator.py`
Programa principal que procesa imágenes en blanco y negro para:
- Cargar y convertir imágenes a matrices (álgebra lineal)
- Binarizar imágenes usando operaciones de umbral
- Detectar objetos mediante algoritmo de componentes conectados
- Calcular áreas usando operaciones vectorizadas de NumPy

**Uso:**
```bash
python image_area_calculator.py <ruta_imagen> [umbral]
```

**Ejemplos:**
```bash
python image_area_calculator.py imagenes_muestra/test_bn_1.png
python image_area_calculator.py imagen.png 150
```

#### `image_transformations.py`
Programa que aplica transformaciones de álgebra lineal a imágenes:
- **Rotación**: Usando matrices de rotación 2D
- **Cambio de tamaño**: Usando matrices de escalamiento
- **Ajuste de contraste**: Usando transformaciones afines
- **Conversión a escala de grises**: Usando combinación lineal de canales RGB
- **Conversión a blanco y negro**: Usando función umbral

**Uso:**
```bash
python image_transformations.py <ruta_imagen>
```

**Ejemplo:**
```bash
python image_transformations.py imagenes_muestra/imagen1_circulos.png
```

### 2. Scripts Auxiliares

#### `create_sample_images.py`
Genera imágenes de muestra para probar los programas:
- 3 imágenes a color con diferentes formas geométricas
- 3 imágenes en blanco y negro para pruebas directas

**Uso:**
```bash
python create_sample_images.py
```

## Instalación

### Requisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- **NumPy**: Para operaciones de álgebra lineal y matrices
- **Pillow (PIL)**: Para carga y manipulación de imágenes
- **Matplotlib**: Para visualización de resultados

## Operaciones de Álgebra Lineal Utilizadas

### 1. Representación Matricial de Imágenes
Las imágenes se representan como matrices NumPy donde cada elemento representa un píxel.

```python
# Imagen en escala de grises: matriz 2D
imagen = np.array([[p11, p12, ...],
                   [p21, p22, ...],
                   ...])

# Imagen RGB: matriz 3D (altura × ancho × 3 canales)
imagen_rgb = np.array([[[R, G, B], ...], ...])
```

### 2. Transformación de Rotación
Matriz de rotación 2D:
```
R(θ) = [cos(θ)  -sin(θ)]
       [sin(θ)   cos(θ)]
```

Cada píxel `(x, y)` se transforma:
```
[x']   [cos(θ)  -sin(θ)]   [x]
[y'] = [sin(θ)   cos(θ)] × [y]
```

### 3. Transformación de Escalamiento
Matriz de escalamiento:
```
S(s) = [s  0]
       [0  s]
```

Transforma coordenadas:
```
[x']   [s  0]   [x]
[y'] = [0  s] × [y]
```

### 4. Conversión a Escala de Grises
Combinación lineal (producto punto) de canales RGB:
```
Gray = [0.299  0.587  0.114] · [R]
                                [G]
                                [B]

Gray = 0.299×R + 0.587×G + 0.114×B
```

Los pesos reflejan la sensibilidad del ojo humano a diferentes colores.

### 5. Ajuste de Contraste
Transformación afín que escala valores alrededor del punto medio:
```
p' = factor × (p - 128) + 128
```

### 6. Binarización (Conversión a Blanco y Negro)
Función de paso aplicada elemento por elemento:
```
p' = 255  si p > umbral
p' = 0    si p ≤ umbral
```

En forma matricial:
```python
binary_matrix = (image_matrix > threshold).astype(int) * 255
```

### 7. Cálculo de Área
El área se calcula usando operaciones vectorizadas:
```python
area = np.sum(labeled_matrix == label)
```

## Ejemplos de Uso

### Ejemplo 1: Aplicar Transformaciones a una Imagen

```bash
# Aplicar todas las transformaciones
python image_transformations.py imagenes_muestra/imagen1_circulos.png
```

Esto genera:
- `imagen1_circulos_rotacion_45.png` - Imagen rotada 45°
- `imagen1_circulos_tamano_0.5x.png` - Imagen reducida al 50%
- `imagen1_circulos_contraste_1.5.png` - Contraste aumentado 1.5x
- `imagen1_circulos_grises.png` - Conversión a escala de grises
- `imagen1_circulos_bn_128.png` - Conversión a blanco y negro
- `imagen1_circulos_comparacion.png` - Comparación de todas las transformaciones

### Ejemplo 2: Calcular Área de Objetos

```bash
# Procesar imagen en blanco y negro
python image_area_calculator.py imagenes_muestra/test_bn_1.png
```

Salida esperada:
```
============================================================
Procesando imagen: imagenes_muestra/test_bn_1.png
============================================================

Imagen cargada: 400x400 píxeles
Dimensiones de la matriz: (400, 400)
Imagen binarizada con umbral 128
Se encontraron 3 objetos en la imagen

============================================================
RESULTADOS DEL ANÁLISIS
============================================================

Total de objetos encontrados: 3
Área total de objetos: 33891 píxeles
Tamaño de la imagen: 160000 píxeles
Porcentaje ocupado: 21.18%

Detalle por objeto:
------------------------------------------------------------
Objeto 2: 17881 píxeles (52.76% del total de objetos)
Objeto 1: 8005 píxeles (23.62% del total de objetos)
Objeto 3: 8005 píxeles (23.62% del total de objetos)

============================================================

Imagen etiquetada guardada en: imagenes_muestra/test_bn_1_labeled.png
```

### Ejemplo 3: Flujo de Trabajo Completo

```bash
# 1. Crear imágenes de muestra
python create_sample_images.py

# 2. Aplicar transformaciones a una imagen a color
python image_transformations.py imagenes_muestra/imagen1_circulos.png

# 3. Calcular área en la imagen convertida a blanco y negro
python image_area_calculator.py imagen1_circulos_bn_128.png

# 4. Probar con diferentes umbrales
python image_area_calculator.py imagen1_circulos_bn_128.png 100
python image_area_calculator.py imagen1_circulos_bn_128.png 180
```

## Estructura del Proyecto

```
ProyectoAlgebra/
│
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias de Python
│
├── image_area_calculator.py       # Programa principal de cálculo de áreas
├── image_transformations.py       # Programa de transformaciones
├── create_sample_images.py        # Generador de imágenes de muestra
│
└── imagenes_muestra/              # Directorio de imágenes de ejemplo
    ├── imagen1_circulos.png       # Imagen 1: círculos de colores
    ├── imagen2_rectangulos.png    # Imagen 2: rectángulos de colores
    ├── imagen3_formas_mixtas.png  # Imagen 3: formas mixtas
    ├── test_bn_1.png              # Prueba BN 1: círculos
    ├── test_bn_2.png              # Prueba BN 2: rectángulos
    └── test_bn_3.png              # Prueba BN 3: formas irregulares
```

## Conceptos de Álgebra Lineal Aplicados

1. **Matrices y Vectores**: Representación de imágenes como matrices numéricas
2. **Operaciones Matriciales**: Multiplicación de matrices para transformaciones
3. **Producto Punto**: Combinación lineal para conversión a escala de grises
4. **Transformaciones Lineales**: Rotación, escalamiento, traslación
5. **Transformaciones Afines**: Ajuste de contraste
6. **Operaciones Vectorizadas**: Procesamiento eficiente usando NumPy
7. **Espacios Vectoriales**: Representación de colores en espacio RGB

## Algoritmos Implementados

### Componentes Conectados (Connected Components)
El algoritmo de componentes conectados utiliza búsqueda en profundidad (DFS) para identificar y etiquetar objetos:

1. **Inicialización**: Crear matriz de etiquetas (zeros)
2. **Recorrido**: Iterar sobre cada píxel de la imagen binarizada
3. **Etiquetado**: Si el píxel pertenece a un objeto no etiquetado:
   - Asignar nueva etiqueta
   - Aplicar DFS para etiquetar todos los píxeles conectados
4. **Resultado**: Matriz donde cada objeto tiene una etiqueta única

### Cálculo de Área
El área se calcula contando los píxeles de cada componente usando operaciones vectorizadas de NumPy:

```python
for label in unique_labels:
    area = np.sum(labeled_matrix == label)
```

## Limitaciones y Consideraciones

### Limitaciones del Programa

1. **Resolución**: La precisión del área depende de la resolución de la imagen
2. **Conectividad**: Se usa conectividad 8 (incluye diagonales)
3. **Umbral**: El umbral de binarización puede requerir ajuste según la imagen
4. **Objetos Tocándose**: Objetos que se tocan se consideran como uno solo
5. **Ruido**: Píxeles aislados pueden ser detectados como objetos pequeños

### Mejoras Potenciales

1. Implementar filtros de ruido (morphological operations)
2. Añadir detección de formas específicas (círculos, rectángulos)
3. Implementar cálculo de perímetro y otras métricas
4. Añadir interfaz gráfica de usuario (GUI)
5. Soportar procesamiento por lotes de múltiples imágenes
6. Exportar resultados a formato CSV o JSON

## Aplicaciones Prácticas

Este tipo de procesamiento de imágenes tiene aplicaciones en:
- **Visión por computadora**: Detección y reconocimiento de objetos
- **Análisis médico**: Medición de áreas en radiografías y resonancias
- **Control de calidad**: Inspección industrial de productos
- **Agricultura**: Análisis de cultivos desde imágenes aéreas
- **Astronomía**: Detección y medición de cuerpos celestes
- **Microscopía**: Conteo y medición de células

## Autores

Proyecto desarrollado para el curso de Álgebra Lineal.

## Licencia

Este proyecto es de uso educativo.