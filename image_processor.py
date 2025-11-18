#!/usr/bin/env python3
"""
Procesador de Imágenes - Álgebra Lineal
Aplicación simple para aplicar transformaciones matemáticas a imágenes.
"""

import os
import tkinter as tk
from tkinter import messagebox
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
        
        # Botones de transformación
        button_frame = tk.Frame(control_frame, bg="#34495e")
        button_frame.pack(pady=10)
        
        buttons = [
            ("Escala de Grises", self.to_grayscale, "#9b59b6"),
            ("Binarizar", self.binarize, "#f39c12"),
            ("Rotar 90°", self.rotate_90, "#1abc9c"),
            ("Invertir Colores", self.invert_colors, "#e67e22"),
            ("Reducir Tamaño", self.resize_image, "#c0392b")
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
        """
        if not self.check_image_loaded():
            return
        
        try:
            # Primero convertir a escala de grises
            img = self.current_image.convert('L')
            arr = np.array(img)
            
            # Calcular umbral (método de Otsu simplificado)
            threshold = np.mean(arr)
            
            # Aplicar binarización: función escalón
            binary = (arr > threshold).astype(np.uint8) * 255
            
            self.processed_image = Image.fromarray(binary, mode='L')
            self.display_image(self.processed_image, self.processed_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
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


def main():
    """Función principal."""
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
