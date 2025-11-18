# Guía de Uso - Procesador de Imágenes

## Inicio Rápido

### 1. Instalación

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python image_processor.py
```

## Flujo de Trabajo Recomendado

### Paso 1: Preparar Imágenes
- Coloca 3 imágenes a color en la carpeta `images/`
- Formatos soportados: PNG, JPG, JPEG, BMP, GIF

### Paso 2: Cargar Imagen
1. Haz clic en **"Cargar Imagen"**
2. Selecciona una imagen de la carpeta `images/`
3. La imagen aparecerá en el panel izquierdo

### Paso 3: Ajustar Parámetros
Antes de aplicar transformaciones, ajusta los parámetros:

- **Ángulo (°)**: Para rotación (por defecto: 25.0)
- **α (alfa)**: Factor de contraste (por defecto: 1.2)
  - α > 1: Aumenta contraste
  - α < 1: Reduce contraste
- **β (beta)**: Ajuste de brillo (por defecto: 10.0)
  - β > 0: Aumenta brillo
  - β < 0: Reduce brillo
- **Método de binarización**: 
  - **Otsu**: Calcula automáticamente el mejor umbral
  - **Umbral fijo**: Usa el valor especificado (por defecto: 128)

### Paso 4: Aplicar Transformaciones

Haz clic en cualquiera de los botones de transformación:

1. **Escala de Grises**: Convierte a blanco y negro
2. **Binarizar**: Aplica binarización (Otsu o umbral fijo)
3. **Rotar Ángulo**: Rota con el ángulo especificado
4. **Invertir Colores**: Invierte los valores de píxeles
5. **Reducir Tamaño**: Reduce al 50% del tamaño
6. **Contraste/Brillo**: Ajusta con α y β

El resultado aparecerá en el panel derecho.

### Paso 5: Exportar Pipeline Completo

1. Haz clic en **"Exportar Pipeline"**
2. Se creará la carpeta `outputs/<nombre_imagen>/` con:
   - `00_original.png` - Imagen original
   - `01_rotada.png` - Rotación aplicada
   - `02_resized.png` - Redimensionada 50%
   - `03_contraste.png` - Contraste/brillo ajustado
   - `04_grises.png` - Escala de grises
   - `05_binaria_otsu.png` - Binarización Otsu
   - `06_binaria_umbral.png` - Binarización umbral fijo
   - `metadata.txt` - Parámetros usados

### Paso 6: Calcular Área

#### Opción A: Desde Imagen Procesada
1. Aplica **"Binarizar"** primero
2. Haz clic en **"Calcular Área"**
3. Selecciona si el objeto es blanco o negro
4. Opcionalmente, ingresa PPU para convertir a cm²

#### Opción B: Desde Archivo Externo
1. Haz clic en **"Área desde Archivo..."**
2. Selecciona un archivo de imagen binaria
3. La aplicación validará que sea binaria
4. Selecciona objeto blanco/negro
5. Ingresa PPU si deseas cm²

## Ejemplos de Uso

### Ejemplo 1: Mejorar Contraste de Foto Oscura
```
1. Cargar imagen oscura
2. Ajustar: α=1.5, β=20
3. Clic en "Contraste/Brillo"
4. Guardar resultado
```

### Ejemplo 2: Preparar Imagen para Análisis
```
1. Cargar imagen a color
2. "Escala de Grises"
3. Ajustar umbral si necesario
4. "Binarizar" (método Otsu)
5. "Calcular Área"
```

### Ejemplo 3: Documentar Proceso Completo
```
1. Cargar imagen
2. Ajustar todos los parámetros
3. "Exportar Pipeline"
4. Revisar outputs/<nombre>/ para ver todas las etapas
```

## Conversión de Unidades (PPU)

PPU = Píxeles Por Unidad de medida (cm)

Si sabes que tu imagen tiene una escala conocida:
1. Mide un objeto conocido en píxeles
2. Calcula: PPU = píxeles_medidos / tamaño_real_cm
3. Usa este valor al calcular área

Ejemplo:
- Regla de 10 cm ocupa 100 píxeles
- PPU = 100 / 10 = 10 píxeles/cm
- Área de 400 píxeles = 400 / (10²) = 4 cm²

## Consejos

1. **Usa Otsu para imágenes con objetos claros**: El método de Otsu funciona mejor cuando hay una clara separación entre objeto y fondo
2. **Ajusta el umbral manualmente para casos difíciles**: Si Otsu no da buenos resultados, prueba con umbral fijo
3. **Exporta el pipeline para documentación**: Útil para reportes y presentaciones
4. **Experimenta con α y β**: Prueba diferentes valores para encontrar el mejor resultado
5. **Guarda resultados intermedios**: Usa "Guardar Resultado" después de cada transformación importante

## Solución de Problemas

### La imagen no se carga
- Verifica que sea un formato soportado (PNG, JPG, etc.)
- Verifica que el archivo no esté corrupto

### La binarización no se ve bien
- Prueba cambiar entre Otsu y umbral fijo
- Ajusta el valor del umbral manualmente
- Aplica contraste/brillo antes de binarizar

### El cálculo de área da resultado inesperado
- Verifica que la imagen esté correctamente binarizada
- Confirma si estás midiendo objeto blanco o negro
- Revisa el valor de PPU si usas conversión a cm²

## Estructura de Carpetas

```
ProyectoAlgebra/
├── images/              # Coloca aquí tus imágenes de entrada
├── outputs/             # Resultados del pipeline (auto-generado)
│   └── <imagen>/        # Una carpeta por imagen procesada
├── image_processor.py   # Aplicación principal
├── README.md           # Documentación completa
└── requirements.txt    # Dependencias
```

## Atajos de Teclado

- No hay atajos de teclado específicos
- Usa el ratón para todos los controles

## Notas Importantes

1. **outputs/** está excluido de git (.gitignore)
2. No subas imágenes con copyright no-permitido
3. Los archivos de pipeline se sobrescriben si procesas la misma imagen dos veces
4. La aplicación valida automáticamente imágenes binarias al calcular área

## Soporte

Para problemas o preguntas, revisa:
1. Este archivo (USAGE_GUIDE.md)
2. README.md para documentación técnica
3. Comentarios en el código (image_processor.py)
