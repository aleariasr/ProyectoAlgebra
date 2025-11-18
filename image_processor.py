#!/usr/bin/env python3
"""
Procesador de Imágenes - Álgebra Lineal
Aplicación simple para aplicar transformaciones matemáticas a imágenes.
"""

import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import numpy as np


class ImageProcessor:
    """Aplicación para procesar imágenes con álgebra lineal."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador de Imágenes - Álgebra Lineal")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")
        
        # Estado de la aplicación
        self.current_image = None
        self.processed_image = None
        self.image_path = None
        
        # Parámetros de transformación
        self.rotation_angle = tk.DoubleVar(value=25.0)
        self.contrast_alpha = tk.DoubleVar(value=1.2)
        self.brightness_beta = tk.DoubleVar(value=10.0)
        self.threshold_value = tk.IntVar(value=128)
        self.binarization_method = tk.StringVar(value="otsu")  # "otsu" o "fixed"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        
        # Título
        title = tk.Label(
            self.root,
            text="PROCESADOR DE IMÁGENES",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title.pack(pady=15)
        
        # Frame para botones de archivo
        file_frame = tk.Frame(self.root, bg="#34495e", bd=2, relief="ridge")
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            file_frame,
            text="Cargar Imagen",
            command=self.load_image,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            pady=5
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(
            file_frame,
            text="Guardar Resultado",
            command=self.save_image,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            pady=5
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(
            file_frame,
            text="Limpiar",
            command=self.clear_all,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            pady=5
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Frame para mostrar imágenes
        display_frame = tk.Frame(self.root, bg="#2c3e50")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Imagen original
        left_frame = tk.Frame(display_frame, bg="#34495e", bd=2, relief="sunken")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            left_frame,
            text="Imagen Original",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        ).pack(pady=8)
        
        self.original_label = tk.Label(left_frame, bg="#7f8c8d", text="No hay imagen")
        self.original_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Imagen procesada
        right_frame = tk.Frame(display_frame, bg="#34495e", bd=2, relief="sunken")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(
            right_frame,
            text="Resultado Procesado",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        ).pack(pady=8)
        
        self.processed_label = tk.Label(right_frame, bg="#7f8c8d", text="Aplicar transformación")
        self.processed_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de controles
        control_frame = tk.Frame(self.root, bg="#34495e", bd=2, relief="ridge")
        control_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        tk.Label(
            control_frame,
            text="Transformaciones Disponibles:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        ).pack(pady=10)
        
        # Panel de parámetros
        params_frame = tk.Frame(control_frame, bg="#34495e")
        params_frame.pack(pady=5, padx=10, fill=tk.X)
        
        # Parámetros de rotación
        rot_frame = tk.Frame(params_frame, bg="#34495e")
        rot_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(rot_frame, text="Ángulo (°):", bg="#34495e", fg="#ecf0f1", font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Entry(rot_frame, textvariable=self.rotation_angle, width=8, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        # Parámetros de contraste/brillo
        contrast_frame = tk.Frame(params_frame, bg="#34495e")
        contrast_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(contrast_frame, text="α:", bg="#34495e", fg="#ecf0f1", font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Entry(contrast_frame, textvariable=self.contrast_alpha, width=6, font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Label(contrast_frame, text="β:", bg="#34495e", fg="#ecf0f1", font=("Arial", 9)).pack(side=tk.LEFT, padx=(5,0))
        tk.Entry(contrast_frame, textvariable=self.brightness_beta, width=6, font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # Parámetros de binarización
        bin_frame = tk.Frame(params_frame, bg="#34495e")
        bin_frame.pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(bin_frame, text="Otsu", variable=self.binarization_method, value="otsu", 
                      bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50", font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Radiobutton(bin_frame, text="Umbral:", variable=self.binarization_method, value="fixed",
                      bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50", font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Entry(bin_frame, textvariable=self.threshold_value, width=6, font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # Botones de transformación
        button_frame = tk.Frame(control_frame, bg="#34495e")
        button_frame.pack(pady=10)
        
        buttons = [
            ("Escala de Grises", self.to_grayscale, "#9b59b6"),
            ("Binarizar", self.binarize, "#f39c12"),
            ("Rotar Ángulo", self.rotate_angle, "#1abc9c"),
            ("Invertir Colores", self.invert_colors, "#e67e22"),
            ("Reducir Tamaño", self.resize_image, "#c0392b"),
            ("Contraste/Brillo", self.adjust_contrast_brightness_ui, "#8e44ad"),
            ("Calcular Área", self.calculate_area, "#16a085"),
            ("Área desde Archivo...", self.calculate_area_from_file, "#27ae60"),
            ("Exportar Pipeline", self.export_pipeline, "#d35400")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 10, "bold"),
                width=18,
                pady=8
            ).grid(row=i // 3, column=i % 3, padx=8, pady=5)
    
    def load_image(self):
        """Carga una imagen desde el sistema de archivos."""
        # Fix for macOS: use initialdir parameter instead of defaultextension
        file_path = askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Todos", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )
        
        if not file_path:
            return
        
        try:
            self.image_path = file_path
            self.current_image = Image.open(file_path)
            self.processed_image = None
            
            # Mostrar imagen original
            self.display_image(self.current_image, self.original_label)
            
            # Limpiar imagen procesada
            self.processed_label.config(image='', text="Aplicar transformación")
            
            messagebox.showinfo("Éxito", "Imagen cargada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
    
    def save_image(self):
        """Guarda la imagen procesada."""
        if self.processed_image is None:
            messagebox.showwarning("Advertencia", "No hay imagen procesada para guardar")
            return
        
        file_path = asksaveasfilename(
            title="Guardar Imagen",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("Todos", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("Éxito", f"Imagen guardada en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{str(e)}")
    
    def clear_all(self):
        """Limpia todas las imágenes."""
        self.current_image = None
        self.processed_image = None
        self.image_path = None
        
        self.original_label.config(image='', text="No hay imagen")
        self.processed_label.config(image='', text="Aplicar transformación")
    
    def display_image(self, img, label):
        """Muestra una imagen en un label."""
        # Redimensionar para que quepa en el display
        display_img = img.copy()
        display_img.thumbnail((350, 250), Image.Resampling.LANCZOS)
        
        # Convertir a formato compatible con Tkinter
        if display_img.mode not in ('RGB', 'L'):
            display_img = display_img.convert('RGB')
        
        photo = ImageTk.PhotoImage(display_img)
        label.config(image=photo, text='')
        label.image = photo  # Mantener referencia
    
    def check_image_loaded(self):
        """Verifica si hay una imagen cargada."""
        if self.current_image is None:
            messagebox.showwarning("Advertencia", "Primero carga una imagen")
            return False
        return True
    
    # Transformaciones
    
    def to_grayscale(self):
        """
        Convierte la imagen a escala de grises.
        Álgebra Lineal: Combinación lineal de canales RGB
        Gray = 0.299*R + 0.587*G + 0.114*B
        """
        if not self.check_image_loaded():
            return
        
        try:
            # Convertir a RGB si no lo es
            img = self.current_image
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Matriz de la imagen
            arr = np.array(img, dtype=np.float32)
            
            # Vector de pesos para la proyección (combinación lineal)
            weights = np.array([0.299, 0.587, 0.114])
            
            # Aplicar producto punto
            gray = np.dot(arr, weights)
            gray = np.clip(gray, 0, 255).astype(np.uint8)
            
            self.processed_image = Image.fromarray(gray, mode='L')
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def binarize(self):
        """
        Binariza la imagen (blanco y negro).
        Álgebra Lineal: Función escalón sobre matriz
        Soporta método de Otsu real o umbral fijo seleccionable.
        """
        if not self.check_image_loaded():
            return
        
        try:
            # Primero convertir a escala de grises
            img = self.current_image.convert('L')
            arr = np.array(img)
            
            # Seleccionar método de binarización
            if self.binarization_method.get() == "otsu":
                threshold = self.otsu_threshold(arr)
            else:
                threshold = self.threshold_value.get()
            
            # Aplicar binarización: función escalón
            binary = (arr > threshold).astype(np.uint8) * 255
            
            self.processed_image = Image.fromarray(binary, mode='L')
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def otsu_threshold(self, gray_array):
        """
        Calcula el umbral óptimo usando el método de Otsu.
        Maximiza la varianza entre clases.
        
        Args:
            gray_array: Array NumPy de imagen en escala de grises
            
        Returns:
            int: Umbral óptimo
        """
        # Calcular histograma (256 bins para 0-255)
        histogram, _ = np.histogram(gray_array.flatten(), bins=256, range=(0, 256))
        histogram = histogram.astype(float)
        
        # Normalizar histograma (probabilidades)
        total_pixels = gray_array.size
        prob = histogram / total_pixels
        
        # Calcular media global
        bins = np.arange(256)
        mean_global = np.sum(bins * prob)
        
        # Inicializar variables
        max_variance = 0
        optimal_threshold = 0
        
        # Probar cada umbral posible
        weight_background = 0
        sum_background = 0
        
        for t in range(256):
            # Peso y suma acumulada para el fondo (clase 0)
            weight_background += prob[t]
            sum_background += t * prob[t]
            
            # Si no hay píxeles en el fondo o en el frente, continuar
            if weight_background == 0 or weight_background == 1:
                continue
            
            weight_foreground = 1 - weight_background
            
            # Media de cada clase
            mean_background = sum_background / weight_background
            mean_foreground = (mean_global - sum_background) / weight_foreground
            
            # Varianza entre clases
            variance_between = (weight_background * weight_foreground * 
                              (mean_background - mean_foreground) ** 2)
            
            # Actualizar si encontramos una mejor varianza
            if variance_between > max_variance:
                max_variance = variance_between
                optimal_threshold = t
        
        return optimal_threshold
    
    def rotate_90(self):
        """
        Rota la imagen 90 grados.
        Álgebra Lineal: Matriz de rotación 2D
        """
        if not self.check_image_loaded():
            return
        
        try:
            self.processed_image = self.current_image.rotate(-90, expand=True)
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def rotate_angle(self):
        """
        Rota la imagen por un ángulo arbitrario.
        Álgebra Lineal: Matriz de rotación 2D
        """
        if not self.check_image_loaded():
            return
        
        try:
            angle = self.rotation_angle.get()
            self.processed_image = self.current_image.rotate(
                angle, 
                expand=True, 
                resample=Image.Resampling.BICUBIC
            )
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def invert_colors(self):
        """
        Invierte los colores de la imagen.
        Álgebra Lineal: Transformación afín p' = 255 - p
        """
        if not self.check_image_loaded():
            return
        
        try:
            # Convertir a RGB si es necesario
            img = self.current_image
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            arr = np.array(img)
            
            # Transformación afín: invertir valores
            inverted = 255 - arr
            
            self.processed_image = Image.fromarray(inverted.astype(np.uint8))
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def resize_image(self):
        """
        Reduce el tamaño de la imagen al 50%.
        Álgebra Lineal: Matriz de escalamiento
        """
        if not self.check_image_loaded():
            return
        
        try:
            width, height = self.current_image.size
            new_size = (width // 2, height // 2)
            
            self.processed_image = self.current_image.resize(new_size, Image.Resampling.LANCZOS)
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def adjust_contrast_brightness_ui(self):
        """
        Ajusta el contraste y brillo de la imagen usando los valores de la UI.
        Álgebra Lineal: Transformación afín I' = α·I + β
        """
        if not self.check_image_loaded():
            return
        
        try:
            alpha = self.contrast_alpha.get()
            beta = self.brightness_beta.get()
            
            # Convertir a escala de grises para simplificar
            img = self.current_image.convert('L')
            arr = np.array(img, dtype=np.float32)
            
            # Aplicar transformación afín: out = α * arr + β
            adjusted = alpha * arr + beta
            adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
            
            self.processed_image = Image.fromarray(adjusted, mode='L')
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def calculate_area(self):
        """
        Calcula el área de una imagen binaria.
        Permite cargar una imagen binaria y calcula el área en píxeles.
        Opcionalmente convierte a cm² si se proporciona PPU (píxeles por unidad).
        """
        if self.processed_image is None or self.processed_image.mode != 'L':
            messagebox.showinfo(
                "Información",
                "Primero aplica una transformación de Binarización para calcular el área.\n\n"
                "El cálculo de área funciona sobre imágenes binarizadas (blanco y negro)."
            )
            return
        
        try:
            # Obtener la imagen binaria procesada
            binary_img = self.processed_image
            arr = np.asarray(binary_img, dtype=np.uint8)
            
            # Preguntar si el objeto es blanco o negro
            response = messagebox.askyesnocancel(
                "Selección de objeto",
                "¿El objeto a medir es BLANCO?\n\n"
                "Sí = objeto blanco\n"
                "No = objeto negro\n"
                "Cancelar = cancelar operación"
            )
            
            if response is None:  # Cancelar
                return
            
            object_is_white = response
            
            # Calcular área en píxeles
            if object_is_white:
                mask = (arr > 127)  # Píxeles blancos
            else:
                mask = (arr <= 127)  # Píxeles negros
            
            pixel_area = int(mask.sum())
            
            # Preguntar si quiere convertir a cm²
            ppu_input = tk.simpledialog.askstring(
                "Conversión a cm²",
                f"Área en píxeles: {pixel_area}\n\n"
                "Si desea convertir a cm², ingrese PPU (píxeles por cm).\n"
                "Deje vacío para omitir:",
                parent=self.root
            )
            
            result_msg = f"Área calculada:\n\n"
            result_msg += f"Píxeles: {pixel_area}\n"
            
            if ppu_input and ppu_input.strip():
                try:
                    ppu = float(ppu_input.strip())
                    if ppu > 0:
                        area_cm2 = pixel_area / (ppu * ppu)
                        result_msg += f"Área en cm²: {area_cm2:.4f}\n"
                except ValueError:
                    pass
            
            messagebox.showinfo("Resultado - Cálculo de Área", result_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular área:\n{str(e)}")
    
    def calculate_area_from_file(self):
        """
        Calcula el área desde un archivo de imagen binaria externa.
        Soporta imágenes en modo L o 1 (binaria).
        """
        try:
            # Abrir diálogo para seleccionar archivo
            file_path = askopenfilename(
                title="Seleccionar Imagen Binaria",
                filetypes=[
                    ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),
                    ("Todos", "*.*")
                ],
                initialdir=os.path.expanduser("~")
            )
            
            if not file_path:
                return
            
            # Cargar imagen
            img = Image.open(file_path)
            
            # Convertir a L si es modo 1
            if img.mode == '1':
                img = img.convert('L')
            elif img.mode != 'L':
                # Si no es binaria, convertir a L
                img = img.convert('L')
            
            arr = np.array(img, dtype=np.uint8)
            
            # Verificar si es binaria (solo 0 y 255)
            unique_values = np.unique(arr)
            if not (len(unique_values) <= 2 and all(v in [0, 255] for v in unique_values)):
                # Forzar binarización con umbral fijo
                threshold = self.threshold_value.get()
                arr = (arr > threshold).astype(np.uint8) * 255
                messagebox.showinfo(
                    "Imagen binarizada",
                    f"La imagen tenía valores de grises. Se binarizó usando umbral {threshold}."
                )
            
            # Preguntar si el objeto es blanco o negro
            response = messagebox.askyesnocancel(
                "Selección de objeto",
                "¿El objeto a medir es BLANCO?\n\n"
                "Sí = objeto blanco\n"
                "No = objeto negro\n"
                "Cancelar = cancelar operación"
            )
            
            if response is None:  # Cancelar
                return
            
            object_is_white = response
            
            # Calcular área en píxeles
            if object_is_white:
                mask = (arr > 127)  # Píxeles blancos
            else:
                mask = (arr <= 127)  # Píxeles negros
            
            pixel_area = int(mask.sum())
            
            # Preguntar si quiere convertir a cm²
            ppu_input = tk.simpledialog.askstring(
                "Conversión a cm²",
                f"Área en píxeles: {pixel_area}\n\n"
                "Si desea convertir a cm², ingrese PPU (píxeles por cm).\n"
                "Deje vacío para omitir:",
                parent=self.root
            )
            
            result_msg = f"Área calculada desde archivo:\n{os.path.basename(file_path)}\n\n"
            result_msg += f"Píxeles: {pixel_area}\n"
            
            if ppu_input and ppu_input.strip():
                try:
                    ppu = float(ppu_input.strip())
                    if ppu > 0:
                        area_cm2 = pixel_area / (ppu * ppu)
                        result_msg += f"Área en cm²: {area_cm2:.4f}\n"
                except ValueError:
                    pass
            
            messagebox.showinfo("Resultado - Cálculo de Área", result_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular área desde archivo:\n{str(e)}")
    
    def export_pipeline(self):
        """
        Exporta el pipeline completo de transformaciones aplicadas a la imagen actual.
        Guarda todas las transformaciones intermedias en outputs/<nombre_base>/.
        """
        if self.current_image is None:
            messagebox.showwarning("Advertencia", "Primero carga una imagen")
            return
        
        try:
            # Obtener nombre base de la imagen
            if self.image_path:
                base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            else:
                base_name = "imagen"
            
            # Crear directorio de salida
            output_dir = os.path.join("outputs", base_name)
            os.makedirs(output_dir, exist_ok=True)
            
            # Obtener parámetros
            angle = self.rotation_angle.get()
            alpha = self.contrast_alpha.get()
            beta = self.brightness_beta.get()
            threshold = self.threshold_value.get()
            bin_method = self.binarization_method.get()
            
            # Lista para metadata
            metadata = []
            metadata.append(f"Pipeline de Transformaciones - {base_name}")
            metadata.append(f"Fecha: {os.popen('date').read().strip()}")
            metadata.append(f"\nParámetros utilizados:")
            metadata.append(f"- Ángulo de rotación: {angle}°")
            metadata.append(f"- Contraste (α): {alpha}")
            metadata.append(f"- Brillo (β): {beta}")
            metadata.append(f"- Método de binarización: {bin_method}")
            metadata.append(f"- Umbral fijo: {threshold}")
            metadata.append(f"\nArchivos generados:")
            
            # 00 - Original
            orig_path = os.path.join(output_dir, "00_original.png")
            self.current_image.save(orig_path)
            metadata.append(f"- 00_original.png")
            
            # 01 - Rotada
            rotated = self.current_image.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
            rot_path = os.path.join(output_dir, "01_rotada.png")
            rotated.save(rot_path)
            metadata.append(f"- 01_rotada.png (ángulo: {angle}°)")
            
            # 02 - Redimensionada (50%)
            width, height = rotated.size
            new_size = (width // 2, height // 2)
            resized = rotated.resize(new_size, Image.Resampling.LANCZOS)
            res_path = os.path.join(output_dir, "02_resized.png")
            resized.save(res_path)
            metadata.append(f"- 02_resized.png (50% del tamaño)")
            
            # 03 - Contraste/Brillo
            gray_for_contrast = resized.convert('L')
            arr_contrast = np.array(gray_for_contrast, dtype=np.float32)
            adjusted = alpha * arr_contrast + beta
            adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
            contrast_img = Image.fromarray(adjusted, mode='L')
            con_path = os.path.join(output_dir, "03_contraste.png")
            contrast_img.save(con_path)
            metadata.append(f"- 03_contraste.png (α={alpha}, β={beta})")
            
            # 04 - Escala de grises
            gray_img = contrast_img  # Ya está en L
            gray_path = os.path.join(output_dir, "04_grises.png")
            gray_img.save(gray_path)
            metadata.append(f"- 04_grises.png")
            
            # 05 - Binaria Otsu
            arr_gray = np.array(gray_img)
            threshold_otsu = self.otsu_threshold(arr_gray)
            binary_otsu = (arr_gray > threshold_otsu).astype(np.uint8) * 255
            otsu_img = Image.fromarray(binary_otsu, mode='L')
            otsu_path = os.path.join(output_dir, "05_binaria_otsu.png")
            otsu_img.save(otsu_path)
            metadata.append(f"- 05_binaria_otsu.png (umbral Otsu: {threshold_otsu})")
            
            # 06 - Binaria umbral fijo
            binary_fixed = (arr_gray > threshold).astype(np.uint8) * 255
            fixed_img = Image.fromarray(binary_fixed, mode='L')
            fixed_path = os.path.join(output_dir, "06_binaria_umbral.png")
            fixed_img.save(fixed_path)
            metadata.append(f"- 06_binaria_umbral.png (umbral fijo: {threshold})")
            
            # Guardar metadata
            metadata_path = os.path.join(output_dir, "metadata.txt")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(metadata))
            
            messagebox.showinfo(
                "Pipeline Exportado",
                f"Pipeline exportado exitosamente en:\n{os.path.abspath(output_dir)}\n\n"
                f"Se generaron 7 archivos de imagen y metadata.txt"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar pipeline:\n{str(e)}")


def main():
    """Función principal."""
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
