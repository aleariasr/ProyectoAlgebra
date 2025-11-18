# Guía para el Video Explicativo

## Estructura del Video (Duración estimada: 8-12 minutos)

### 1. Saludo e Introducción (1 minuto)
**Script sugerido:**
```
"Hola, bienvenidos a nuestra presentación del proyecto de Álgebra Lineal sobre 
procesamiento de imágenes. Mi nombre es [NOMBRE] y el día de hoy les mostraré 
cómo aplicamos conceptos de álgebra lineal para analizar imágenes en blanco y 
negro y calcular el área de objetos presentes en ellas.

El proyecto consiste en dos programas principales:
1. Un programa que aplica transformaciones de álgebra lineal a imágenes
2. Un programa que calcula áreas de objetos en imágenes en blanco y negro

Empecemos con las transformaciones de imágenes."
```

**Elementos visuales:**
- Mostrar pantalla con el proyecto abierto
- Mostrar brevemente las imágenes de muestra

---

### 2. Aplicación de Transformaciones (5-6 minutos)

#### 2.1 Preparación (30 segundos)
**Acciones:**
1. Abrir terminal
2. Navegar al directorio del proyecto
3. Mostrar las imágenes disponibles

**Comandos a mostrar:**
```bash
cd ProyectoAlgebra
ls imagenes_muestra/
```

#### 2.2 Transformación 1: Rotación (1 minuto)

**Script:**
```
"Primero aplicaremos una rotación de 45 grados. Esta transformación usa una 
matriz de rotación 2D que multiplica las coordenadas de cada píxel."
```

**En pantalla, mostrar:**
1. Abrir `image_transformations.py` y señalar el código de rotación:
```python
rotation_matrix = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])
```

2. Explicar la matriz:
```
"Esta es la matriz de rotación clásica del álgebra lineal:
R(θ) = [cos(θ)  -sin(θ)]
       [sin(θ)   cos(θ)]

Cada píxel en posición (x,y) se multiplica por esta matriz para obtener 
su nueva posición (x',y')."
```

3. Ejecutar y mostrar resultado:
```bash
python image_transformations.py imagenes_muestra/imagen1_circulos.png
```

4. Abrir y mostrar `imagen1_circulos_rotacion_45.png`

#### 2.3 Transformación 2: Cambio de Tamaño (45 segundos)

**Script:**
```
"La segunda transformación es el cambio de tamaño, usando una matriz de 
escalamiento que reduce la imagen al 50%."
```

**Mostrar código:**
```python
scaling_matrix = np.array([
    [scale_factor, 0],
    [0, scale_factor]
])
```

**Explicar:**
```
"La matriz de escalamiento es diagonal:
S(s) = [s  0]
       [0  s]

En nuestro caso s = 0.5, lo que reduce las coordenadas a la mitad."
```

**Mostrar resultado:** `imagen1_circulos_tamano_0.5x.png`

#### 2.4 Transformación 3: Ajuste de Contraste (45 segundos)

**Script:**
```
"El ajuste de contraste usa una transformación afín que escala los valores 
de intensidad alrededor del punto medio."
```

**Mostrar código:**
```python
adjusted = factor * (image_array - 128) + 128
```

**Explicar:**
```
"Esta operación se aplica a cada píxel p:
p' = 1.5 × (p - 128) + 128

Esto aumenta la diferencia entre píxeles claros y oscuros, incrementando 
el contraste."
```

**Mostrar resultado:** `imagen1_circulos_contraste_1.5.png`

#### 2.5 Transformación 4: Escala de Grises (1 minuto)

**Script:**
```
"La conversión a escala de grises es una de las aplicaciones más interesantes 
del álgebra lineal en procesamiento de imágenes."
```

**Mostrar código:**
```python
weights = np.array([0.299, 0.587, 0.114])
gray_array = np.dot(image_array[...,:3], weights)
```

**Explicar:**
```
"Usamos una combinación lineal, que es un producto punto:

Gray = 0.299×R + 0.587×G + 0.114×B

Los pesos no son arbitrarios - reflejan cómo el ojo humano percibe los colores.
Somos más sensibles al verde (0.587) que al rojo (0.299) o al azul (0.114)."
```

**Mostrar resultado:** `imagen1_circulos_grises.png`

#### 2.6 Transformación 5: Blanco y Negro (45 segundos)

**Script:**
```
"Finalmente, convertimos a blanco y negro puro usando una función umbral."
```

**Mostrar código:**
```python
bw_array = (gray_array > threshold).astype(np.uint8) * 255
```

**Explicar:**
```
"Esta es una función de paso:
p' = 255 si p > 128
p' = 0   si p ≤ 128

Se aplica vectorizada a toda la matriz de píxeles simultáneamente."
```

**Mostrar resultado:** `imagen1_circulos_bn_128.png`

#### 2.7 Comparación Visual (30 segundos)

**Script:**
```
"El programa genera automáticamente una comparación visual de todas las 
transformaciones aplicadas."
```

**Mostrar:** `imagen1_circulos_comparacion.png`

**Señalar:**
- Imagen original
- Cada transformación
- Diferencias visuales

---

### 3. Ejecución del Programa de Cálculo de Áreas (3-4 minutos)

#### 3.1 Explicación del Programa (1 minuto)

**Script:**
```
"Ahora pasamos al programa principal que calcula áreas de objetos. 
Este programa utiliza varios conceptos de álgebra lineal:

1. Representación matricial de imágenes
2. Operaciones vectorizadas con NumPy
3. Algoritmo de componentes conectados para identificar objetos
4. Suma matricial condicional para calcular áreas"
```

**Mostrar código brevemente:**
```python
# Binarización
self.binary_matrix = (self.image_matrix < self.threshold).astype(np.int32)

# Cálculo de área
area = np.sum(self.labeled_matrix == label)
```

#### 3.2 Demostración con Imagen 1 (1 minuto)

**Script:**
```
"Vamos a procesar nuestra primera imagen de prueba que contiene tres círculos 
en blanco y negro."
```

**Ejecutar:**
```bash
python image_area_calculator.py imagenes_muestra/test_bn_1.png
```

**Leer resultados en pantalla:**
```
"Como vemos en los resultados:
- Se encontraron 3 objetos (los tres círculos)
- Área total: 33,891 píxeles
- Esto representa el 21.18% de la imagen
- El objeto 2 es el más grande con 17,881 píxeles"
```

**Mostrar imagen etiquetada:**
```
"El programa generó una imagen etiquetada donde cada objeto tiene un 
color diferente para visualizar la detección."
```

Abrir: `imagenes_muestra/test_bn_1_labeled.png`

#### 3.3 Demostración con Imagen 2 (1 minuto)

**Script:**
```
"Probemos con la segunda imagen que tiene rectángulos."
```

**Ejecutar:**
```bash
python image_area_calculator.py imagenes_muestra/test_bn_2.png
```

**Comentar resultados:**
```
"En esta imagen:
- 3 rectángulos detectados
- Área total mayor: 52,783 píxeles (32.99%)
- Los rectángulos tienen tamaños variados que el programa detecta correctamente"
```

**Mostrar:** `imagenes_muestra/test_bn_2_labeled.png`

#### 3.4 Demostración con Imagen 3 (1 minuto)

**Script:**
```
"Finalmente, una imagen con formas irregulares."
```

**Ejecutar:**
```bash
python image_area_calculator.py imagenes_muestra/test_bn_3.png
```

**Comentar:**
```
"Aquí tenemos:
- 2 objetos de formas irregulares
- El programa no se limita a formas geométricas simples
- Puede detectar cualquier forma presente en la imagen"
```

**Mostrar:** `imagenes_muestra/test_bn_3_labeled.png`

---

### 4. Demostración con Imágenes Transformadas (1-2 minutos)

**Script:**
```
"Ahora vamos a demostrar el flujo completo: tomar una imagen a color, 
aplicar transformaciones, y calcular el área de la versión en blanco y negro."
```

**Ejecutar:**
```bash
# Ya aplicamos las transformaciones antes, ahora calculamos área
python image_area_calculator.py imagen1_circulos_bn_128.png
```

**Comentar:**
```
"Como pueden ver, el programa funciona perfectamente con las imágenes que 
nosotros mismos transformamos. Esto demuestra la integración completa de 
ambos programas."
```

---

### 5. Cierre (1 minuto)

**Script:**
```
"Para resumir, en este proyecto hemos:

1. Aplicado cinco transformaciones de álgebra lineal a imágenes:
   - Rotación con matrices de rotación
   - Escalamiento con matrices diagonales
   - Ajuste de contraste con transformaciones afines
   - Conversión a grises con combinación lineal
   - Binarización con función umbral

2. Desarrollado un programa que:
   - Detecta objetos automáticamente
   - Calcula sus áreas con precisión
   - Genera visualizaciones etiquetadas

3. Demostrado la aplicación práctica del álgebra lineal en procesamiento 
   de imágenes, un campo con aplicaciones en medicina, industria, 
   astronomía y más.

El código completo está documentado y disponible en el repositorio del proyecto.

Muchas gracias por su atención."
```

---

## Consejos para la Grabación

### Técnicos:
1. **Resolución**: Grabar en al menos 1080p (1920x1080)
2. **Audio**: Usar micrófono externo si es posible
3. **Software recomendado**: 
   - OBS Studio (gratuito)
   - Zoom (grabar sesión)
   - Loom (navegador)
   
### Preparación:
1. **Antes de grabar:**
   - Cerrar programas innecesarios
   - Aumentar tamaño de fuente del terminal
   - Preparar todas las imágenes en carpetas fáciles de acceder
   - Probar todos los comandos previamente
   - Tener un guion escrito

2. **Durante la grabación:**
   - Hablar claro y a ritmo pausado
   - Dar tiempo para que se vean los resultados
   - No apresurarse al ejecutar comandos
   - Si cometes un error, pausar y editar después

3. **Edición:**
   - Cortar silencios largos
   - Añadir zoom a secciones importantes del código
   - Incluir subtítulos si es posible
   - Agregar intro/outro simple

### Estructura de Carpetas para Grabación:
```
Preparar:
/ProyectoAlgebra/
├── imagenes_muestra/ (ya listas)
├── Terminal abierta en esta carpeta
├── Editor de código con archivos principales abiertos
└── Carpeta de resultados visible
```

### Checklist Pre-Grabación:
- [ ] Probar todos los comandos
- [ ] Verificar que todas las imágenes están disponibles
- [ ] Ajustar tamaño de fuente del terminal (16-18pt mínimo)
- [ ] Cerrar notificaciones del sistema
- [ ] Tener agua cerca
- [ ] Cronometrar el guion (debe ser 8-12 minutos)
- [ ] Preparar música de fondo suave (opcional)

### Secciones que Puede Editar/Acelerar:
- Esperas de ejecución de comandos (usar corte)
- Navegación de archivos (acelerar 1.5x-2x)
- Mostrar múltiples resultados similares (resumir)

### Secciones que Debe Mostrar Completas:
- Explicación de matrices de álgebra lineal
- Primera ejecución de cada programa
- Resultados de cálculo de áreas
- Comparación de imágenes transformadas
