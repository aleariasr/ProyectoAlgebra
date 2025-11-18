#!/usr/bin/env python3
"""
Simple Image Lab - Laboratorio de Transformación de Imágenes
Aplicación GUI para explorar transformaciones de álgebra lineal en imágenes.

Este programa permite:
1. Importar y seleccionar imágenes desde tu computadora
2. Aplicar transformaciones de álgebra lineal
3. Visualizar resultados en tiempo real
4. Guardar todas las transformaciones con documentación
"""

import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import numpy as np


# ============================================================================
# UTILIDADES DE PROCESAMIENTO DE IMÁGENES
# ============================================================================

def load_image(path):
    """Carga una imagen desde una ruta."""
    return Image.open(path)


def save_image(img, path):
    """Guarda una imagen creando directorios si es necesario."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def rgb_to_gray(img):
    """
    Convierte imagen RGB a escala de grises usando combinación lineal.
    
    OPERACIÓN DE ÁLGEBRA LINEAL:
    Gray = [0.2989  0.5870  0.1140] · [R]
                                      [G]
                                      [B]
    
    Esta es una proyección lineal que combina los tres canales RGB
    en un solo canal usando un producto punto vectorial.
    Los pesos están basados en la percepción humana de luminosidad.
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    arr = np.asarray(img, dtype=np.float32)
    
    # Vector de pesos para la proyección lineal
    weights = np.array([0.2989, 0.5870, 0.1140], dtype=np.float32)
    
    # Aplicar producto punto (combinación lineal)
    gray = arr @ weights
    gray = np.clip(gray, 0, 255).astype(np.uint8)
    
    return Image.fromarray(gray, mode="L")


def contrast_affine(img_gray, alpha=1.2, beta=0.0):
    """
    Ajusta contraste y brillo usando transformación afín.
    
    OPERACIÓN DE ÁLGEBRA LINEAL:
    Para cada píxel p: p' = α·p + β
    
    Esta es una transformación afín donde:
    - α (alpha) controla el contraste (multiplicación escalar)
    - β (beta) controla el brillo (traslación)
    
    En forma matricial, para cada píxel:
    p' = α·p + β·1
    """
    arr = np.asarray(img_gray, dtype=np.float32)
    
    # Aplicar transformación afín
    out = alpha * arr + beta
    out = np.clip(out, 0, 255).astype(np.uint8)
    
    return Image.fromarray(out, mode="L")


def otsu_threshold(gray_img):
    """
    Binarización automática usando el método de Otsu.
    
    El método de Otsu encuentra el umbral óptimo que maximiza
    la varianza entre clases (objetos vs fondo).
    """
    arr = np.asarray(gray_img, dtype=np.uint8)
    hist = np.bincount(arr.ravel(), minlength=256).astype(np.float64)
    total = arr.size
    sum_total = np.dot(np.arange(256), hist)

    sumB = 0.0
    wB = 0.0
    max_var = -1.0
    threshold = 0

    for t in range(256):
        wB += hist[t]
        if wB == 0:
            continue
        wF = total - wB
        if wF == 0:
            break
        sumB += t * hist[t]
        mB = sumB / wB
        mF = (sum_total - sumB) / wF
        var_between = wB * wF * (mB - mF) ** 2
        if var_between > max_var:
            max_var = var_between
            threshold = t

    binary = (arr > threshold).astype(np.uint8) * 255
    return Image.fromarray(binary, mode="L"), threshold


def fixed_threshold(gray_img, thr=128):
    """
    Binarización con umbral fijo.
    
    OPERACIÓN DE ÁLGEBRA LINEAL:
    Función de paso (step function):
    p' = 255  si p > umbral
    p' = 0    si p ≤ umbral
    
    Esta es una función no lineal aplicada elemento por elemento
    a la matriz de píxeles.
    """
    if gray_img.mode != "L":
        gray_img = gray_img.convert("L")
    arr = np.asarray(gray_img, dtype=np.uint8)
    
    # Aplicar función de paso
    binary = (arr > int(thr)).astype(np.uint8) * 255
    
    return Image.fromarray(binary, mode="L")


def compute_area(binary_img, ppu=None, object_is_white=True):
    """
    Calcula el área de objetos en una imagen binaria.
    
    Args:
        binary_img: Imagen binaria (modo 'L' o '1')
        ppu: Píxeles por unidad (cm). Si se proporciona, calcula área en cm²
        object_is_white: True si el objeto es blanco, False si es negro
    
    Returns:
        dict: Diccionario con área en píxeles y en unidades (si ppu es dado)
    """
    if binary_img.mode not in ("L", "1"):
        raise ValueError("Se requiere imagen binaria en modo 'L' (0/255) o '1'.")
    
    arr = np.asarray(binary_img)
    if binary_img.mode == "1":
        arr = arr.astype(np.uint8) * 255
    
    # Contar píxeles del objeto usando operaciones vectorizadas
    mask = (arr > 0) if object_is_white else (arr == 0)
    pixel_area = int(mask.sum())
    
    unit_area = None
    if ppu and ppu > 0:
        unit_area = pixel_area / (ppu * ppu)
    
    return {"pixel_area": pixel_area, "unit_area": unit_area}


# ============================================================================
# CLASE PRINCIPAL DE LA APLICACIÓN GUI
# ============================================================================

class SimpleImageLab(tk.Tk):
    """
    Aplicación GUI para transformaciones de imágenes con álgebra lineal.
    """
    
    def __init__(self):
        super().__init__()
        self.title("Simple Image Lab - Transformaciones con Álgebra Lineal")
        self.geometry("1200x750")
        
        # Lista de rutas de imágenes cargadas
        self.images = []
        
        # Directorio de salida para resultados
        self.output_dir = os.path.abspath("outputs")
        
        # Variables para parámetros de transformaciones
        self.var_rotation = tk.DoubleVar(value=25.0)
        self.var_w = tk.StringVar(value="")  # vacío = auto 60%
        self.var_h = tk.StringVar(value="")
        self.var_alpha = tk.DoubleVar(value=1.2)
        self.var_beta = tk.DoubleVar(value=10.0)
        
        # Variables para cálculo de área
        self.object_white = tk.BooleanVar(value=True)
        self.ppu_str = tk.StringVar(value="")
        
        # Construir la interfaz
        self._build_ui()
        
        # Mensaje de bienvenida
        self._log("Bienvenido a Simple Image Lab")
        self._log("Usa 'Abrir imágenes...' para cargar imágenes a color desde tu computadora")
        self._log("Selecciona una imagen de la lista para previsualizar y transformar")
    
    def _build_ui(self):
        """Construye la interfaz gráfica completa."""
        
        # ====================================================================
        # BARRA SUPERIOR - Controles de archivos
        # ====================================================================
        top_frame = ttk.Frame(self, padding=8)
        top_frame.pack(fill=tk.X)
        
        ttk.Button(
            top_frame, 
            text="📁 Abrir imágenes...", 
            command=self.open_images
        ).pack(side=tk.LEFT, padx=4)
        
        ttk.Label(top_frame, text="Carpeta de salida:").pack(side=tk.LEFT, padx=(12, 2))
        self.lbl_out = ttk.Label(top_frame, text=self.output_dir, width=50)
        self.lbl_out.pack(side=tk.LEFT)
        
        ttk.Button(
            top_frame, 
            text="Cambiar...", 
            command=self.change_output
        ).pack(side=tk.LEFT, padx=4)
        
        # ====================================================================
        # PANEL IZQUIERDO - Lista de imágenes y controles
        # ====================================================================
        left_panel = ttk.Frame(self, padding=8)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # --- Lista de imágenes ---
        ttk.Label(
            left_panel, 
            text="📋 Imágenes cargadas", 
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        
        # Frame con scrollbar para la lista
        list_frame = ttk.Frame(left_panel)
        list_frame.pack(fill=tk.BOTH, expand=False, pady=6)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame, 
            height=12, 
            width=55, 
            exportselection=False,
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind("<<ListboxSelect>>", self.on_select_image)
        
        # --- Parámetros de transformaciones ---
        params_frame = ttk.LabelFrame(left_panel, text="⚙️ Parámetros de Transformaciones", padding=8)
        params_frame.pack(fill=tk.X, pady=6)
        
        # Rotación
        r1 = ttk.Frame(params_frame)
        r1.pack(fill=tk.X, pady=3)
        ttk.Label(r1, text="🔄 Rotación (grados):").pack(side=tk.LEFT)
        ttk.Entry(r1, width=10, textvariable=self.var_rotation).pack(side=tk.LEFT, padx=6)
        
        # Redimensionamiento
        r2 = ttk.Frame(params_frame)
        r2.pack(fill=tk.X, pady=3)
        ttk.Label(r2, text="📐 Tamaño (ancho × alto):").pack(side=tk.LEFT)
        ttk.Entry(r2, width=8, textvariable=self.var_w).pack(side=tk.LEFT, padx=3)
        ttk.Label(r2, text="×").pack(side=tk.LEFT)
        ttk.Entry(r2, width=8, textvariable=self.var_h).pack(side=tk.LEFT, padx=3)
        ttk.Label(r2, text="(vacío = 60%)").pack(side=tk.LEFT, padx=6)
        
        # Contraste y brillo
        r3 = ttk.Frame(params_frame)
        r3.pack(fill=tk.X, pady=3)
        ttk.Label(r3, text="🌓 Contraste α:").pack(side=tk.LEFT)
        ttk.Entry(r3, width=8, textvariable=self.var_alpha).pack(side=tk.LEFT, padx=6)
        ttk.Label(r3, text="Brillo β:").pack(side=tk.LEFT)
        ttk.Entry(r3, width=8, textvariable=self.var_beta).pack(side=tk.LEFT, padx=6)
        
        # Botón para guardar transformaciones
        ttk.Button(
            left_panel, 
            text="💾 Guardar todas las transformaciones", 
            command=self.save_transforms
        ).pack(fill=tk.X, pady=(8, 4))
        
        # --- Cálculo de área ---
        area_frame = ttk.LabelFrame(left_panel, text="📊 Cálculo de Área (desde binaria)", padding=8)
        area_frame.pack(fill=tk.X, pady=6)
        
        a1 = ttk.Frame(area_frame)
        a1.pack(fill=tk.X, pady=2)
        ttk.Label(a1, text="PPU (píxeles/cm):").pack(side=tk.LEFT)
        ttk.Entry(a1, width=12, textvariable=self.ppu_str).pack(side=tk.LEFT, padx=6)
        
        a2 = ttk.Frame(area_frame)
        a2.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(
            a2, 
            text="Objeto blanco", 
            variable=self.object_white, 
            value=True
        ).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(
            a2, 
            text="Objeto negro", 
            variable=self.object_white, 
            value=False
        ).pack(side=tk.LEFT, padx=4)
        
        ttk.Button(
            area_frame, 
            text="📏 Calcular área (desde archivo binario...)", 
            command=self.calc_area_from_file
        ).pack(fill=tk.X, pady=(6, 0))
        
        # ====================================================================
        # PANEL DERECHO - Previsualizaciones y log
        # ====================================================================
        right_panel = ttk.Frame(self, padding=8)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # --- Previsualizaciones ---
        preview_frame = ttk.LabelFrame(right_panel, text="👁️ Previsualización", padding=8)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        preview_holder = ttk.Frame(preview_frame)
        preview_holder.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo: Original
        left_preview = ttk.Frame(preview_holder)
        left_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        ttk.Label(left_preview, text="Original", font=("Segoe UI", 9, "bold")).pack()
        self.lbl_original = tk.Label(left_preview, relief="sunken", bg="gray85")
        self.lbl_original.pack(fill=tk.BOTH, expand=True, pady=4)
        
        # Panel derecho: Binaria
        right_preview = ttk.Frame(preview_holder)
        right_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        ttk.Label(right_preview, text="Binaria (Otsu)", font=("Segoe UI", 9, "bold")).pack()
        self.lbl_binary = tk.Label(right_preview, relief="sunken", bg="gray85")
        self.lbl_binary.pack(fill=tk.BOTH, expand=True, pady=4)
        
        # --- Log de consola ---
        log_frame = ttk.LabelFrame(right_panel, text="📝 Registro de Actividad", padding=8)
        log_frame.pack(fill=tk.X, pady=8)
        
        log_scroll = ttk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log = tk.Text(log_frame, height=10, yscrollcommand=log_scroll.set)
        self.log.pack(fill=tk.X)
        log_scroll.config(command=self.log.yview)
    
    # ========================================================================
    # MÉTODOS AUXILIARES DE GUI
    # ========================================================================
    
    def _log(self, msg):
        """Añade un mensaje al log de actividad."""
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
    
    def _set_preview(self, widget, pil_img, title=""):
        """
        Muestra una imagen en un widget de preview.
        
        Args:
            widget: Widget Label donde mostrar la imagen
            pil_img: Imagen PIL a mostrar
            title: Título opcional
        """
        im = pil_img.copy()
        im.thumbnail((520, 480))
        
        # Asegurar que está en modo compatible con Tkinter
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        
        tkimg = ImageTk.PhotoImage(im)
        widget.configure(image=tkimg)
        widget.image = tkimg  # Mantener referencia
    
    # ========================================================================
    # ACCIONES PRINCIPALES
    # ========================================================================
    
    def open_images(self):
        """Abre diálogo para seleccionar imágenes desde el computador."""
        paths = filedialog.askopenfilenames(
            title="Selecciona imágenes a color",
            filetypes=[
                ("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tif;*.tiff"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg;*.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if not paths:
            return
        
        self.images = list(paths)
        self.listbox.delete(0, tk.END)
        
        for p in self.images:
            # Mostrar solo el nombre del archivo en la lista
            display_name = os.path.basename(p)
            self.listbox.insert(tk.END, display_name)
        
        self._log(f"✓ {len(self.images)} imagen(es) cargada(s). Selecciona una para explorar.")
    
    def on_select_image(self, event=None):
        """Maneja la selección de una imagen de la lista."""
        if not self.listbox.curselection():
            return
        
        idx = self.listbox.curselection()[0]
        path = self.images[idx]
        
        try:
            img = load_image(path)
            self._log(f"📷 Previsualizando: {os.path.basename(path)}")
            
            # Mostrar original
            self._set_preview(self.lbl_original, img, "Original")
            
            # Generar y mostrar preview de binaria (Otsu)
            gray = rgb_to_gray(img)
            binary, threshold = otsu_threshold(gray)
            self._set_preview(self.lbl_binary, binary, "Binaria")
            self._log(f"   Umbral Otsu calculado: {threshold}")
            
        except Exception as e:
            self._log(f"❌ Error al previsualizar: {e}")
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")
    
    def change_output(self):
        """Cambia el directorio de salida para los resultados."""
        d = filedialog.askdirectory(
            title="Selecciona carpeta de salida", 
            initialdir=self.output_dir
        )
        if d:
            self.output_dir = d
            self.lbl_out.config(text=self.output_dir)
            self._log(f"📁 Carpeta de salida cambiada: {self.output_dir}")
    
    def save_transforms(self):
        """
        Guarda todas las transformaciones de la imagen seleccionada.
        Documenta cada transformación con su operación de álgebra lineal.
        """
        if not self.listbox.curselection():
            messagebox.showinfo("Información", "Por favor selecciona una imagen de la lista.")
            return
        
        idx = self.listbox.curselection()[0]
        path = self.images[idx]
        
        try:
            self._log("="*60)
            self._log(f"💾 Guardando transformaciones de: {os.path.basename(path)}")
            self._log("="*60)
            
            img = load_image(path)
            base = os.path.splitext(os.path.basename(path))[0]
            outdir = os.path.join(self.output_dir, base)
            os.makedirs(outdir, exist_ok=True)
            
            # Crear archivo de documentación
            doc_path = os.path.join(outdir, "README_TRANSFORMACIONES.txt")
            doc_lines = []
            doc_lines.append("="*70)
            doc_lines.append("DOCUMENTACIÓN DE TRANSFORMACIONES - ÁLGEBRA LINEAL")
            doc_lines.append("="*70)
            doc_lines.append(f"\nImagen original: {os.path.basename(path)}")
            doc_lines.append(f"Tamaño: {img.width} × {img.height} píxeles")
            doc_lines.append(f"Modo: {img.mode}\n")
            
            # 0) ORIGINAL
            out_original = os.path.join(outdir, "00_original.png")
            save_image(img, out_original)
            self._log("✓ 00_original.png")
            
            doc_lines.append("\n" + "-"*70)
            doc_lines.append("IMAGEN ORIGINAL (00_original.png)")
            doc_lines.append("-"*70)
            doc_lines.append("Imagen base sin transformaciones aplicadas.\n")
            
            # 1) ROTACIÓN
            rot_deg = float(self.var_rotation.get())
            rotated = img.rotate(rot_deg, expand=True, resample=Image.BICUBIC)
            out_rot = os.path.join(outdir, "01_rotada.png")
            save_image(rotated, out_rot)
            self._log(f"✓ 01_rotada.png (ángulo: {rot_deg}°)")
            
            theta_rad = np.radians(rot_deg)
            cos_theta = np.cos(theta_rad)
            sin_theta = np.sin(theta_rad)
            
            doc_lines.append("\n" + "-"*70)
            doc_lines.append(f"1. ROTACIÓN (01_rotada.png) - Ángulo: {rot_deg}°")
            doc_lines.append("-"*70)
            doc_lines.append("\nOPERACIÓN DE ÁLGEBRA LINEAL:")
            doc_lines.append("Matriz de rotación 2D:")
            doc_lines.append("R(θ) = [cos(θ)  -sin(θ)]")
            doc_lines.append("       [sin(θ)   cos(θ)]")
            doc_lines.append("\nCada píxel (x, y) se transforma usando:")
            doc_lines.append("[x']   [cos(θ)  -sin(θ)]   [x]")
            doc_lines.append("[y'] = [sin(θ)   cos(θ)] × [y]")
            doc_lines.append(f"\nMatriz de rotación para θ={rot_deg}°:")
            doc_lines.append(f"R = [{cos_theta:.4f}  {-sin_theta:.4f}]")
            doc_lines.append(f"    [{sin_theta:.4f}   {cos_theta:.4f}]")
            doc_lines.append("\nCÓDIGO UTILIZADO:")
            doc_lines.append(f"rotated = img.rotate({rot_deg}, expand=True, resample=Image.BICUBIC)\n")
            
            # 2) REDIMENSIONAMIENTO
            w_txt, h_txt = self.var_w.get().strip(), self.var_h.get().strip()
            if w_txt and h_txt:
                new_size = (int(w_txt), int(h_txt))
            else:
                new_size = (int(img.width * 0.6), int(img.height * 0.6))
            
            resized = img.resize(new_size, resample=Image.LANCZOS)
            out_res = os.path.join(outdir, "02_resized.png")
            save_image(resized, out_res)
            self._log(f"✓ 02_resized.png (tamaño: {new_size[0]} × {new_size[1]})")
            
            scale_x = new_size[0] / img.width
            scale_y = new_size[1] / img.height
            
            doc_lines.append("\n" + "-"*70)
            doc_lines.append(f"2. REDIMENSIONAMIENTO (02_resized.png)")
            doc_lines.append("-"*70)
            doc_lines.append(f"\nTamaño original: {img.width} × {img.height}")
            doc_lines.append(f"Tamaño nuevo: {new_size[0]} × {new_size[1]}")
            doc_lines.append(f"Factor de escala: {scale_x:.3f} × {scale_y:.3f}")
            doc_lines.append("\nOPERACIÓN DE ÁLGEBRA LINEAL:")
            doc_lines.append("Matriz de escalamiento:")
            doc_lines.append("S = [sx  0 ]")
            doc_lines.append("    [0   sy]")
            doc_lines.append("\nCada píxel (x, y) se transforma:")
            doc_lines.append("[x']   [sx  0 ]   [x]")
            doc_lines.append("[y'] = [0   sy] × [y]")
            doc_lines.append(f"\nMatriz de escalamiento aplicada:")
            doc_lines.append(f"S = [{scale_x:.4f}  0.0000]")
            doc_lines.append(f"    [0.0000  {scale_y:.4f}]")
            doc_lines.append("\nCÓDIGO UTILIZADO:")
            doc_lines.append(f"resized = img.resize(({new_size[0]}, {new_size[1]}), resample=Image.LANCZOS)\n")
            
            # 3) CONVERSIÓN A ESCALA DE GRISES
            gray = rgb_to_gray(img)
            out_gray = os.path.join(outdir, "03_grises.png")
            save_image(gray, out_gray)
            self._log("✓ 03_grises.png")
            
            doc_lines.append("\n" + "-"*70)
            doc_lines.append("3. CONVERSIÓN A ESCALA DE GRISES (03_grises.png)")
            doc_lines.append("-"*70)
            doc_lines.append("\nOPERACIÓN DE ÁLGEBRA LINEAL:")
            doc_lines.append("Combinación lineal (producto punto) de los canales RGB:")
            doc_lines.append("Gray = [0.2989  0.5870  0.1140] · [R]")
            doc_lines.append("                                  [G]")
            doc_lines.append("                                  [B]")
            doc_lines.append("\nEsto equivale a:")
            doc_lines.append("Gray = 0.2989·R + 0.5870·G + 0.1140·B")
            doc_lines.append("\nLos pesos están basados en la sensibilidad del ojo humano")
            doc_lines.append("a diferentes longitudes de onda (luminosidad percibida).")
            doc_lines.append("\nCÓDIGO UTILIZADO:")
            doc_lines.append("weights = np.array([0.2989, 0.5870, 0.1140])")
            doc_lines.append("gray = arr @ weights  # Producto punto matricial\n")
            
            # 4) AJUSTE DE CONTRASTE
            alpha = float(self.var_alpha.get())
            beta = float(self.var_beta.get())
            contrast = contrast_affine(gray, alpha=alpha, beta=beta)
            out_contrast = os.path.join(outdir, "04_contraste.png")
            save_image(contrast, out_contrast)
            self._log(f"✓ 04_contraste.png (α={alpha}, β={beta})")
            
            doc_lines.append("\n" + "-"*70)
            doc_lines.append(f"4. AJUSTE DE CONTRASTE (04_contraste.png)")
            doc_lines.append("-"*70)
            doc_lines.append(f"\nParámetros: α={alpha}, β={beta}")
            doc_lines.append("\nOPERACIÓN DE ÁLGEBRA LINEAL:")
            doc_lines.append("Transformación afín aplicada a cada píxel:")
            doc_lines.append("p' = α·p + β")
            doc_lines.append("\nDonde:")
            doc_lines.append("- α (alpha) controla el contraste (multiplicación escalar)")
            doc_lines.append("- β (beta) controla el brillo (traslación)")
            doc_lines.append("\nEn forma matricial extendida:")
            doc_lines.append("p' = [α  β] · [p]")
            doc_lines.append("             [1]")
            doc_lines.append(f"\nTransformación aplicada:")
            doc_lines.append(f"p' = {alpha}·p + {beta}")
            doc_lines.append("\nCÓDIGO UTILIZADO:")
            doc_lines.append(f"contrast = {alpha} * arr + {beta}")
            doc_lines.append("contrast = np.clip(contrast, 0, 255)  # Limitar rango válido\n")
            
            # 5) BINARIA (Otsu)
            binary_otsu, threshold = otsu_threshold(gray)
            out_bin = os.path.join(outdir, "05_binaria_otsu.png")
            save_image(binary_otsu, out_bin)
            self._log(f"✓ 05_binaria_otsu.png (umbral automático: {threshold})")
            
            doc_lines.append("\n" + "-"*70)
            doc_lines.append(f"5. BINARIZACIÓN AUTOMÁTICA - MÉTODO DE OTSU (05_binaria_otsu.png)")
            doc_lines.append("-"*70)
            doc_lines.append(f"\nUmbral calculado automáticamente: {threshold}")
            doc_lines.append("\nOPERACIÓN DE ÁLGEBRA LINEAL:")
            doc_lines.append("Función de paso (step function) aplicada elemento por elemento:")
            doc_lines.append(f"p' = 255  si p > {threshold}")
            doc_lines.append(f"p' = 0    si p ≤ {threshold}")
            doc_lines.append("\nEl método de Otsu encuentra el umbral óptimo que maximiza")
            doc_lines.append("la varianza entre las clases (objetos vs fondo).")
            doc_lines.append("\nCÓDIGO UTILIZADO:")
            doc_lines.append("# Método de Otsu implementado con histograma")
            doc_lines.append("threshold = otsu_threshold(gray)")
            doc_lines.append("binary = (arr > threshold).astype(np.uint8) * 255\n")
            
            # 6) BLANCO Y NEGRO (umbral fijo)
            binary_fixed = fixed_threshold(gray, thr=128)
            out_bn = os.path.join(outdir, "06_blanco_negro.png")
            save_image(binary_fixed, out_bn)
            self._log("✓ 06_blanco_negro.png (umbral fijo: 128)")
            
            doc_lines.append("\n" + "-"*70)
            doc_lines.append("6. BINARIZACIÓN CON UMBRAL FIJO (06_blanco_negro.png)")
            doc_lines.append("-"*70)
            doc_lines.append("\nUmbral fijo: 128")
            doc_lines.append("\nOPERACIÓN DE ÁLGEBRA LINEAL:")
            doc_lines.append("Función de paso (step function):")
            doc_lines.append("p' = 255  si p > 128")
            doc_lines.append("p' = 0    si p ≤ 128")
            doc_lines.append("\nCÓDIGO UTILIZADO:")
            doc_lines.append("binary = (arr > 128).astype(np.uint8) * 255\n")
            
            # Guardar documentación
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(doc_lines))
            
            self._log("✓ README_TRANSFORMACIONES.txt (documentación completa)")
            self._log("="*60)
            self._log(f"✅ Todas las transformaciones guardadas en: {outdir}")
            self._log("="*60)
            
            messagebox.showinfo(
                "Éxito", 
                f"Transformaciones guardadas exitosamente en:\n{outdir}\n\n" +
                "Se han generado:\n" +
                "• 6 imágenes transformadas\n" +
                "• 1 archivo de documentación con las operaciones de álgebra lineal"
            )
            
        except Exception as e:
            self._log(f"❌ Error al guardar transformaciones: {e}")
            messagebox.showerror("Error", f"No se pudieron guardar las transformaciones:\n{e}")
    
    def calc_area_from_file(self):
        """
        Calcula el área de objetos en una imagen binaria seleccionada por el usuario.
        """
        path = filedialog.askopenfilename(
            title="Selecciona imagen BINARIA (blanco y negro)",
            filetypes=[
                ("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"),
                ("PNG", "*.png"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if not path:
            return
        
        try:
            img = load_image(path)
            
            # Obtener PPU si se proporcionó
            ppu = None
            txt = self.ppu_str.get().strip()
            if txt:
                try:
                    ppu = float(txt)
                    if ppu <= 0:
                        ppu = None
                except ValueError:
                    ppu = None
            
            # Calcular área
            res = compute_area(img, ppu=ppu, object_is_white=self.object_white.get())
            
            self._log("="*60)
            self._log(f"📏 CÁLCULO DE ÁREA")
            self._log("="*60)
            self._log(f"Imagen: {os.path.basename(path)}")
            self._log(f"Tipo de objeto: {'Blanco' if self.object_white.get() else 'Negro'}")
            self._log(f"Área en píxeles: {res['pixel_area']:,}")
            
            if res['unit_area'] is not None:
                self._log(f"Área en cm²: {res['unit_area']:.4f}")
                self._log(f"(usando PPU = {ppu} píxeles/cm)")
            
            self._log("="*60)
            
        except Exception as e:
            self._log(f"❌ Error al calcular área: {e}")
            messagebox.showerror("Error", f"No se pudo calcular el área:\n{e}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Inicia la aplicación."""
    app = SimpleImageLab()
    app.mainloop()


if __name__ == "__main__":
    main()
