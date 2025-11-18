# Proyecto de Álgebra Lineal: Procesamiento de Imágenes

## Descripción del Proyecto

Este proyecto utiliza conceptos de **álgebra lineal** para procesar imágenes y aplicar transformaciones matemáticas. Incluye una aplicación GUI completa e interactiva para explorar transformaciones de imágenes, exportar pipelines de procesamiento y calcular áreas de objetos en imágenes binarias.

## Programa Principal

### `image_processor.py` - Aplicación GUI Interactiva

Aplicación gráfica que permite:
- **Cargar imágenes** desde tu computadora
- **Aplicar transformaciones** usando álgebra lineal:
  - Conversión a escala de grises (combinación lineal RGB)
  - Binarización con método de Otsu real o umbral fijo seleccionable
  - Rotación por ángulo arbitrario (matriz de rotación 2D)
  - Ajuste de contraste y brillo (transformación afín)
  - Inversión de colores (transformación afín)
  - Reducción de tamaño (matriz de escalamiento)
- **Vista previa en tiempo real** de los resultados
- **Guardar imágenes procesadas**
- **Exportar pipeline completo** de transformaciones
- **Calcular área** de objetos en imágenes binarias (desde procesada o desde archivo externo)

**Características de la interfaz:**
- 🖼️ Interfaz limpia y fácil de usar
- 👁️ Vista previa lado a lado (original vs procesado)
- 🎨 Diseño visual moderno
- ⚡ Procesamiento rápido
- 💾 Guardar resultados en varios formatos
- 📊 Controles parametrizables para cada transformación

**Uso:**
```bash
python image_processor.py
```

**Pasos:**
1. Haz clic en "Cargar Imagen" para seleccionar una imagen
2. Ajusta los parámetros de las transformaciones (ángulo, α, β, método de binarización, umbral)
3. Elige una transformación de las opciones disponibles
4. Haz clic en "Guardar Resultado" para exportar la imagen procesada

## Controles y Parámetros

### Parámetros de Transformación

- **Ángulo (°)**: Especifica el ángulo de rotación en grados (por defecto: 25.0)
- **α (alfa)**: Factor de contraste (por defecto: 1.2)
- **β (beta)**: Ajuste de brillo (por defecto: 10.0)
- **Método de binarización**: 
  - **Otsu**: Calcula automáticamente el umbral óptimo usando el método de Otsu
  - **Umbral fijo**: Permite especificar un valor de umbral manualmente
- **Umbral**: Valor de umbral para binarización con umbral fijo (por defecto: 128)

### Transformaciones Disponibles

1. **Escala de Grises**: Convierte la imagen a escala de grises usando combinación lineal de canales RGB
2. **Binarizar**: Convierte a blanco y negro usando Otsu o umbral fijo
3. **Rotar Ángulo**: Rota la imagen por el ángulo especificado en el parámetro
4. **Invertir Colores**: Invierte los valores de píxeles (255 - valor)
5. **Reducir Tamaño**: Reduce la imagen al 50% de su tamaño original
6. **Contraste/Brillo**: Ajusta contraste y brillo usando la transformación I' = α·I + β
7. **Calcular Área**: Calcula el área de la imagen binaria procesada
8. **Área desde Archivo...**: Carga un archivo binario externo y calcula su área
9. **Exportar Pipeline**: Exporta el pipeline completo de transformaciones

## Exportar Pipeline de Transformaciones

El botón **"Exportar Pipeline"** genera automáticamente una secuencia completa de transformaciones aplicadas a la imagen cargada. Los archivos se guardan en `outputs/<nombre_base>/`:

**Archivos generados:**
- `00_original.png` - Imagen original sin modificar
- `01_rotada.png` - Imagen rotada con el ángulo especificado
- `02_resized.png` - Imagen redimensionada al 50%
- `03_contraste.png` - Contraste y brillo ajustados (α, β)
- `04_grises.png` - Conversión a escala de grises
- `05_binaria_otsu.png` - Binarización usando método de Otsu
- `06_binaria_umbral.png` - Binarización usando umbral fijo
- `metadata.txt` - Archivo con todos los parámetros utilizados

Este pipeline es útil para:
- Documentar el proceso de transformación completo
- Generar evidencias del procesamiento de imágenes
- Comparar diferentes métodos de binarización
- Reproducir los resultados del procesamiento

## Cálculo de Área

### Desde Imagen Procesada

1. Aplica la transformación "Binarizar" a tu imagen
2. Haz clic en "Calcular Área"
3. Selecciona si el objeto es blanco o negro
4. Opcionalmente, ingresa PPU (píxeles por cm) para convertir a cm²

### Desde Archivo Binario Externo

1. Haz clic en "Área desde Archivo..."
2. Selecciona cualquier archivo de imagen binaria
3. La aplicación validará que la imagen sea binaria (o la binarizará automáticamente)
4. Selecciona si el objeto es blanco o negro
5. Opcionalmente, ingresa PPU para convertir a cm²

**Características del cálculo de área:**
- Soporta imágenes en modo L (escala de grises binaria) y modo 1 (blanco/negro)
- Valida automáticamente que la imagen sea binaria
- Si detecta valores de grises, binariza usando el umbral especificado
- Permite seleccionar objeto blanco o negro
- Conversión opcional a cm² usando PPU (píxeles por unidad)
- Muestra resultados claros en píxeles y cm²

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

## Estructura del Proyecto

```
ProyectoAlgebra/
│
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias de Python
├── image_processor.py             # Aplicación principal
├── images/                        # Carpeta para imágenes de entrada
│   ├── .gitkeep                   # Mantiene la carpeta en git
│   └── README.md                  # Instrucciones para las imágenes
└── outputs/                       # Carpeta generada para resultados del pipeline
    └── <nombre_imagen>/           # Una carpeta por imagen procesada
        ├── 00_original.png
        ├── 01_rotada.png
        ├── 02_resized.png
        ├── 03_contraste.png
        ├── 04_grises.png
        ├── 05_binaria_otsu.png
        ├── 06_binaria_umbral.png
        └── metadata.txt
```

## Preparación de Imágenes de Entrada

1. Coloca 3 imágenes a color (PNG/JPG) en la carpeta `images/`
2. Se recomienda nombrarlas de forma descriptiva (ej: `img1.png`, `img2.jpg`, `img3.jpg`)
3. No subir imágenes con copyright no-permitido
4. Las imágenes pueden ser de cualquier tamaño (se redimensionarán automáticamente para visualización)

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

### 2. Conversión a Escala de Grises
Combinación lineal (producto punto) de canales RGB:
```
Gray = [0.299  0.587  0.114] · [R]
                                [G]
                                [B]

Gray = 0.299×R + 0.587×G + 0.114×B
```

Los pesos reflejan la sensibilidad del ojo humano a diferentes colores.

### 3. Binarización

#### Método de Otsu
El método de Otsu calcula el umbral óptimo maximizando la varianza entre clases:

1. Calcula el histograma de la imagen (256 bins)
2. Para cada posible umbral t (0-255):
   - Calcula el peso de cada clase (fondo y objeto)
   - Calcula la media de cada clase
   - Calcula la varianza entre clases
3. Selecciona el umbral que maximiza la varianza entre clases

Varianza entre clases:
```
σ²ₐ(t) = wₐ(t) × wₒ(t) × [μₐ(t) - μₒ(t)]²
```

Donde:
- wₐ(t): peso de la clase fondo
- wₒ(t): peso de la clase objeto
- μₐ(t): media de la clase fondo
- μₒ(t): media de la clase objeto

#### Umbral Fijo
Función de paso aplicada elemento por elemento:
```
p' = 255  si p > umbral
p' = 0    si p ≤ umbral
```

En forma matricial:
```python
binary_matrix = (image_matrix > threshold).astype(int) * 255
```

### 4. Transformación de Rotación
Matriz de rotación 2D para ángulo θ:
```
R(θ) = [cos(θ)  -sin(θ)]
       [sin(θ)   cos(θ)]
```

### 5. Ajuste de Contraste y Brillo
Transformación afín sobre cada píxel:
```
I'(x,y) = α × I(x,y) + β
```

Donde:
- α > 1: aumenta contraste; α < 1: reduce contraste
- β > 0: aumenta brillo; β < 0: reduce brillo

En forma matricial:
```python
adjusted = α * image_matrix + β
adjusted = clip(adjusted, 0, 255)
```

### 6. Inversión de Colores
Transformación afín:
```
p' = 255 - p
```

### 7. Escalamiento (Reducción de Tamaño)
Matriz de escalamiento:
```
S(0.5) = [0.5  0  ]
         [0    0.5]
```

## Ejemplo de Uso Completo

```bash
# 1. Ejecutar la aplicación
python image_processor.py

# 2. En la interfaz:
#    - Cargar una imagen desde images/
#    - Ajustar parámetros: ángulo=45, α=1.5, β=20, método=Otsu
#    - Probar diferentes transformaciones
#    - Exportar pipeline completo
#    - Calcular área de la imagen binarizada

# 3. Revisar resultados en outputs/<nombre_imagen>/
```

**Flujo de trabajo recomendado:**
1. Ejecuta el programa
2. Carga una imagen de la carpeta `images/`
3. Experimenta con los parámetros de transformación
4. Prueba diferentes transformaciones haciendo clic en los botones
5. Exporta el pipeline completo para documentar el proceso
6. Calcula el área de objetos en imágenes binarias
7. Usa "Limpiar" para empezar con una nueva imagen

## Conceptos de Álgebra Lineal Aplicados

1. **Matrices y Vectores**: Representación de imágenes como matrices numéricas
2. **Producto Punto**: Combinación lineal para conversión a escala de grises
3. **Transformaciones Lineales**: Rotación y escalamiento
4. **Transformaciones Afines**: Contraste/brillo e inversión de colores
5. **Operaciones Vectorizadas**: Procesamiento eficiente usando NumPy
6. **Espacios Vectoriales**: Representación de colores en espacio RGB
7. **Funciones Escalón**: Binarización de imágenes
8. **Optimización**: Método de Otsu para encontrar umbral óptimo
9. **Estadística sobre Matrices**: Cálculo de histogramas, medias y varianzas

## Aplicaciones Prácticas

Las transformaciones de imágenes tienen aplicaciones en:
- **Visión por computadora**: Preprocesamiento de imágenes
- **Análisis de imágenes**: Detección de bordes y características
- **Fotografía digital**: Ajustes y filtros
- **Ciencia de datos**: Preparación de datos para machine learning
- **Medición y metrología**: Cálculo de áreas y dimensiones de objetos
- **Control de calidad**: Inspección automatizada de productos

## Autor

Proyecto desarrollado para el curso de Álgebra Lineal - UCR Sede de Occidente.

## Licencia

Este proyecto es de uso educativo.