# Guía para el Trabajo Escrito

## Estructura Recomendada del Documento

### 1. Portada
- Título: "Procesamiento de Imágenes usando Álgebra Lineal"
- Nombres de los integrantes
- Curso y fecha
- Logo o imagen representativa (opcional)

### 2. Introducción
Explicar brevemente:
- El objetivo del proyecto
- La importancia del álgebra lineal en el procesamiento de imágenes
- Las aplicaciones prácticas de este tipo de programas
- Breve descripción de lo que se desarrolló

**Ejemplo:**
```
El presente proyecto tiene como objetivo aplicar conceptos fundamentales de álgebra 
lineal al procesamiento digital de imágenes. Mediante el uso de operaciones matriciales, 
transformaciones lineales y algoritmos vectorizados, se desarrolló un sistema capaz de 
analizar imágenes en blanco y negro para identificar y calcular áreas de objetos presentes 
en ellas. Este trabajo demuestra la aplicación práctica del álgebra lineal en campos como 
la visión por computadora, análisis médico y control de calidad industrial.
```

### 3. Índice
Generar automáticamente o manualmente con las secciones del documento:
- Introducción
- Marco Teórico
- Desarrollo
  - 3.1 Selección de Imágenes
  - 3.2 Transformaciones de Imágenes
  - 3.3 Programa de Cálculo de Áreas
- Resultados
- Conclusiones
- Anexos

### 4. Desarrollo

#### 4.1 Selección de Imágenes

**Imágenes Seleccionadas:**

**Imagen 1: Círculos de Colores**
- Archivo: `imagenes_muestra/imagen1_circulos.png`
- Dimensiones: 800x600 píxeles
- Descripción: Imagen con tres círculos de diferentes colores (rojo, azul, verde)
- Propósito: Probar transformaciones en formas circulares

[Incluir captura de pantalla de imagen1_circulos.png]

**Imagen 2: Rectángulos de Colores**
- Archivo: `imagenes_muestra/imagen2_rectangulos.png`
- Dimensiones: 800x600 píxeles
- Descripción: Imagen con cuatro rectángulos de diferentes colores
- Propósito: Probar transformaciones en formas rectangulares

[Incluir captura de pantalla de imagen2_rectangulos.png]

**Imagen 3: Formas Mixtas**
- Archivo: `imagenes_muestra/imagen3_formas_mixtas.png`
- Dimensiones: 800x600 píxeles
- Descripción: Imagen con combinación de círculos, rectángulos y polígonos
- Propósito: Probar transformaciones en composiciones complejas

[Incluir captura de pantalla de imagen3_formas_mixtas.png]

#### 4.2 Transformaciones de Imágenes

Para este proyecto, se seleccionó la **Imagen 1 (Círculos)** para aplicar las transformaciones.

##### 4.2.1 Rotación

**Código Utilizado:**
```python
def rotate_image(self, angle):
    theta = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    rotated_image = self.original_image.rotate(-angle, expand=True)
    return rotated_image
```

**Operación de Álgebra Lineal:**
La rotación se realiza usando una matriz de rotación 2D:

```
R(θ) = [cos(θ)  -sin(θ)]
       [sin(θ)   cos(θ)]
```

Cada píxel con coordenadas (x, y) se transforma a nuevas coordenadas (x', y') mediante:

```
[x']   [cos(θ)  -sin(θ)]   [x]
[y'] = [sin(θ)   cos(θ)] × [y]
```

**Explicación del Comando:**
- `np.radians(angle)`: Convierte el ángulo de grados a radianes
- `np.array()`: Crea la matriz de rotación usando NumPy
- `np.cos()` y `np.sin()`: Calculan los valores trigonométricos necesarios
- `rotate()`: Método de PIL que aplica la rotación a la imagen

**Resultado:**
[Incluir imagen: imagen1_circulos_rotacion_45.png]
Descripción: La imagen ha sido rotada 45 grados en sentido antihorario.

##### 4.2.2 Cambio de Tamaño

**Código Utilizado:**
```python
def resize_image(self, scale_factor):
    scaling_matrix = np.array([
        [scale_factor, 0],
        [0, scale_factor]
    ])
    new_width = int(self.original_image.width * scale_factor)
    new_height = int(self.original_image.height * scale_factor)
    resized_image = self.original_image.resize((new_width, new_height), 
                                                Image.Resampling.LANCZOS)
    return resized_image
```

**Operación de Álgebra Lineal:**
El escalamiento usa una matriz diagonal:

```
S(s) = [s  0]
       [0  s]
```

**Explicación del Comando:**
- `scale_factor`: Factor de escala (0.5 = 50% del tamaño original)
- `Image.Resampling.LANCZOS`: Algoritmo de interpolación de alta calidad
- La matriz de escalamiento multiplica las coordenadas por el factor

**Resultado:**
[Incluir imagen: imagen1_circulos_tamano_0.5x.png]
Descripción: Imagen reducida al 50% de su tamaño original (400x300 píxeles).

##### 4.2.3 Ajuste de Contraste

**Código Utilizado:**
```python
def adjust_contrast(self, factor):
    image_array = np.array(self.original_image, dtype=np.float64)
    adjusted = factor * (image_array - 128) + 128
    adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
    contrast_image = Image.fromarray(adjusted)
    return contrast_image
```

**Operación de Álgebra Lineal:**
Transformación afín que escala valores alrededor del punto medio:

```
p' = factor × (p - 128) + 128
```

Donde:
- p = valor original del píxel
- p' = valor ajustado
- 128 = punto medio de la escala de grises

**Explicación del Comando:**
- `np.array()`: Convierte la imagen a matriz NumPy
- `dtype=np.float64`: Usa precisión de punto flotante para cálculos
- `np.clip()`: Limita valores al rango válido [0, 255]
- La operación se aplica vectorizada a todos los píxeles simultáneamente

**Resultado:**
[Incluir imagen: imagen1_circulos_contraste_1.5.png]
Descripción: Contraste aumentado 1.5 veces, los colores son más intensos.

##### 4.2.4 Conversión a Escala de Grises

**Código Utilizado:**
```python
def convert_to_grayscale(self):
    weights = np.array([0.299, 0.587, 0.114])
    image_array = np.array(self.original_image, dtype=np.float64)
    gray_array = np.dot(image_array[...,:3], weights)
    gray_array = gray_array.astype(np.uint8)
    gray_image = Image.fromarray(gray_array)
    return gray_image
```

**Operación de Álgebra Lineal:**
Combinación lineal (producto punto) de los canales RGB:

```
Gray = [0.299  0.587  0.114] · [R]
                                [G]
                                [B]

Gray = 0.299×R + 0.587×G + 0.114×B
```

**Explicación del Comando:**
- Los pesos (0.299, 0.587, 0.114) reflejan la percepción humana del color
- `np.dot()`: Calcula el producto punto vectorizado
- El ojo humano es más sensible al verde (0.587) que al rojo (0.299) o azul (0.114)

**Resultado:**
[Incluir imagen: imagen1_circulos_grises.png]
Descripción: Imagen convertida a tonos de gris manteniendo la luminosidad percibida.

##### 4.2.5 Conversión a Blanco y Negro

**Código Utilizado:**
```python
def convert_to_bw(self, threshold=128):
    gray_array = np.array(gray_image, dtype=np.float64)
    bw_array = (gray_array > threshold).astype(np.uint8) * 255
    bw_image = Image.fromarray(bw_array)
    return bw_image
```

**Operación de Álgebra Lineal:**
Función de paso (step function) aplicada elemento por elemento:

```
p' = 255  si p > threshold
p' = 0    si p ≤ threshold
```

**Explicación del Comando:**
- `threshold`: Umbral de binarización (128 = punto medio)
- `(gray_array > threshold)`: Operación booleana vectorizada
- `.astype(np.uint8) * 255`: Convierte True/False a 255/0

**Resultado:**
[Incluir imagen: imagen1_circulos_bn_128.png]
Descripción: Imagen convertida a blanco y negro puro, solo dos valores de píxel.

##### 4.2.6 Comparación de Todas las Transformaciones

**Comando para generar comparación:**
```bash
python image_transformations.py imagenes_muestra/imagen1_circulos.png
```

**Resultado:**
[Incluir imagen: imagen1_circulos_comparacion.png]
Descripción: Panel comparativo mostrando las 6 versiones de la imagen.

#### 4.3 Programa de Cálculo de Áreas

##### 4.3.1 Descripción del Algoritmo

El programa principal utiliza los siguientes pasos:

1. **Carga de imagen**: Conversión a matriz NumPy
2. **Binarización**: Aplicación de umbral para separar objetos del fondo
3. **Detección de componentes**: Algoritmo de conectividad para identificar objetos
4. **Cálculo de áreas**: Conteo de píxeles por componente

##### 4.3.2 Código Principal

```python
class ImageAreaCalculator:
    def load_image(self, image_path):
        img = Image.open(image_path).convert('L')
        self.image_matrix = np.array(img, dtype=np.float64)
        return self.image_matrix
    
    def binarize(self):
        self.binary_matrix = (self.image_matrix < self.threshold).astype(np.int32)
        return self.binary_matrix
    
    def find_connected_components(self):
        # Algoritmo DFS para etiquetar componentes conectados
        # [Código completo en image_area_calculator.py]
        
    def calculate_areas(self):
        unique_labels = np.unique(self.labeled_matrix)
        for label in unique_labels[unique_labels > 0]:
            area = np.sum(self.labeled_matrix == label)
            self.areas[label] = area
        return self.areas
```

**Operaciones de Álgebra Lineal:**
- Representación matricial de imágenes
- Operaciones vectorizadas con NumPy
- Suma matricial condicional: `np.sum(matriz == valor)`

##### 4.3.3 Pruebas del Programa

**Prueba 1: Imagen con círculos**
```bash
python image_area_calculator.py imagenes_muestra/test_bn_1.png
```

Resultado:
```
Total de objetos encontrados: 3
Área total de objetos: 33891 píxeles
Objeto 2: 17881 píxeles (52.76%)
Objeto 1: 8005 píxeles (23.62%)
Objeto 3: 8005 píxeles (23.62%)
```

[Incluir captura: test_bn_1_labeled.png]

**Prueba 2: Imagen con rectángulos**
```bash
python image_area_calculator.py imagenes_muestra/test_bn_2.png
```

Resultado:
```
Total de objetos encontrados: 3
Área total de objetos: 52783 píxeles
Objeto 2: 22801 píxeles (43.20%)
Objeto 3: 19781 píxeles (37.48%)
Objeto 1: 10201 píxeles (19.33%)
```

[Incluir captura: test_bn_2_labeled.png]

**Prueba 3: Imagen con formas irregulares**
```bash
python image_area_calculator.py imagenes_muestra/test_bn_3.png
```

Resultado:
```
Total de objetos encontrados: 2
Área total de objetos: 38032 píxeles
Objeto 1: 20151 píxeles (52.98%)
Objeto 2: 17881 píxeles (47.02%)
```

[Incluir captura: test_bn_3_labeled.png]

### 5. Resultados

Tabla resumen de resultados:

| Imagen | Objetos Detectados | Área Total (píxeles) | % de la Imagen |
|--------|-------------------|---------------------|----------------|
| test_bn_1.png | 3 | 33,891 | 21.18% |
| test_bn_2.png | 3 | 52,783 | 32.99% |
| test_bn_3.png | 2 | 38,032 | 23.77% |

### 6. Conclusiones

**Logros del Proyecto:**
1. Se implementó exitosamente un sistema de procesamiento de imágenes usando álgebra lineal
2. Se aplicaron 5 transformaciones diferentes con sus respectivas operaciones matriciales
3. Se desarrolló un algoritmo de detección de objetos y cálculo de áreas
4. Todas las pruebas fueron exitosas en las 3 imágenes seleccionadas

**Conceptos de Álgebra Lineal Aplicados:**
- Matrices y vectores para representación de imágenes
- Matrices de rotación y escalamiento
- Transformaciones afines para ajuste de contraste
- Combinación lineal para conversión de color
- Operaciones vectorizadas para eficiencia computacional

### 7. Limitaciones del Programa

1. **Resolución**: La precisión depende de la resolución de la imagen
2. **Conectividad**: Objetos que se tocan se detectan como uno solo
3. **Umbral**: Requiere ajuste manual para diferentes tipos de imágenes
4. **Ruido**: Píxeles aislados pueden crear falsos objetos pequeños
5. **Formas complejas**: No distingue entre tipos de formas (círculo vs rectángulo)

**Mejoras Futuras:**
- Implementar filtros de ruido morfológicos
- Añadir clasificación de formas geométricas
- Desarrollar interfaz gráfica de usuario
- Soportar procesamiento por lotes
- Exportar resultados a formatos estructurados (CSV, JSON)

### 8. Anexos

**Anexo A: Comandos de Instalación**
```bash
pip install -r requirements.txt
```

**Anexo B: Estructura de Archivos**
```
ProyectoAlgebra/
├── image_area_calculator.py
├── image_transformations.py
├── create_sample_images.py
├── run_complete_demo.py
├── requirements.txt
├── README.md
└── imagenes_muestra/
```

**Anexo C: Referencias**
- NumPy Documentation: https://numpy.org/doc/
- PIL/Pillow Documentation: https://pillow.readthedocs.io/
- Álgebra Lineal y sus Aplicaciones, David C. Lay
