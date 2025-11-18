# Proyecto de Álgebra Lineal: Procesamiento de Imágenes

## Descripción del Proyecto

Este proyecto utiliza conceptos de **álgebra lineal** para procesar imágenes y aplicar transformaciones matemáticas. Incluye una aplicación GUI simple e interactiva para explorar transformaciones de imágenes.

## Programa Principal

### `image_processor.py` - Aplicación GUI Interactiva

Aplicación gráfica que permite:
- **Cargar imágenes** desde tu computadora
- **Aplicar transformaciones** usando álgebra lineal:
  - Conversión a escala de grises (combinación lineal RGB)
  - Binarización automática (función escalón)
  - Rotación 90° (matriz de rotación 2D)
  - Inversión de colores (transformación afín)
  - Reducción de tamaño (matriz de escalamiento)
- **Vista previa en tiempo real** de los resultados
- **Guardar imágenes procesadas**

**Características de la interfaz:**
- 🖼️ Interfaz limpia y fácil de usar
- 👁️ Vista previa lado a lado (original vs procesado)
- 🎨 Diseño visual moderno
- ⚡ Procesamiento rápido
- 💾 Guardar resultados en varios formatos

**Uso:**
```bash
python image_processor.py
```

**Pasos:**
1. Haz clic en "Cargar Imagen" para seleccionar una imagen
2. Elige una transformación de las opciones disponibles
3. Haz clic en "Guardar Resultado" para exportar la imagen procesada

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
Matriz de rotación 2D para 90°:
```
R(90°) = [0   -1]
         [1    0]
```

### 5. Inversión de Colores
Transformación afín:
```
p' = 255 - p
```

### 6. Escalamiento (Reducción de Tamaño)
Matriz de escalamiento:
```
S(0.5) = [0.5  0  ]
         [0    0.5]
```

## Ejemplo de Uso

```bash
# Ejecutar la aplicación
python image_processor.py
```

**Flujo de trabajo:**
1. Ejecuta el programa
2. Haz clic en "Cargar Imagen" y selecciona una imagen de tu computadora
3. Prueba diferentes transformaciones haciendo clic en los botones
4. Cuando estés satisfecho con el resultado, haz clic en "Guardar Resultado"
5. Usa "Limpiar" para empezar con una nueva imagen

## Estructura del Proyecto

```
ProyectoAlgebra/
│
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias de Python
└── image_processor.py             # Aplicación principal
```

## Conceptos de Álgebra Lineal Aplicados

1. **Matrices y Vectores**: Representación de imágenes como matrices numéricas
2. **Producto Punto**: Combinación lineal para conversión a escala de grises
3. **Transformaciones Lineales**: Rotación y escalamiento
4. **Transformaciones Afines**: Inversión de colores
5. **Operaciones Vectorizadas**: Procesamiento eficiente usando NumPy
6. **Espacios Vectoriales**: Representación de colores en espacio RGB
7. **Funciones Escalón**: Binarización de imágenes

## Aplicaciones Prácticas

Las transformaciones de imágenes tienen aplicaciones en:
- **Visión por computadora**: Preprocesamiento de imágenes
- **Análisis de imágenes**: Detección de bordes y características
- **Fotografía digital**: Ajustes y filtros
- **Ciencia de datos**: Preparación de datos para machine learning

## Autor

Proyecto desarrollado para el curso de Álgebra Lineal.

## Licencia

Este proyecto es de uso educativo.