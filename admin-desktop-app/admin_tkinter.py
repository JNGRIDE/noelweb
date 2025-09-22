#!/usr/bin/env python3
"""
Panel de Administración Desktop usando Tkinter
Alternativa simple sin dependencias externas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import subprocess
import threading
import requests
from datetime import datetime

class AdminDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel Moreno - Panel de Administración")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        self.check_server_status()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Noel Moreno - Panel de Administración", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status del servidor
        self.status_frame = ttk.LabelFrame(main_frame, text="Estado del Servidor", padding="10")
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.status_frame.columnconfigure(1, weight=1)
        
        self.status_label = ttk.Label(self.status_frame, text="Verificando...", foreground="orange")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.refresh_btn = ttk.Button(self.status_frame, text="Actualizar", 
                                     command=self.check_server_status)
        self.refresh_btn.grid(row=0, column=1, sticky=tk.E)
        
        # Botones de acceso
        access_frame = ttk.LabelFrame(main_frame, text="Acceso Rápido", padding="10")
        access_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        access_frame.columnconfigure(0, weight=1)
        access_frame.columnconfigure(1, weight=1)
        
        # Botones principales
        ttk.Button(access_frame, text="🌐 Panel Web", 
                  command=self.open_admin_panel).grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(access_frame, text="🏠 Frontend", 
                  command=self.open_frontend).grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(access_frame, text="📊 API", 
                  command=self.open_api).grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(access_frame, text="🔄 Recargar Servidor", 
                  command=self.restart_server).grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Secciones de gestión
        sections_frame = ttk.LabelFrame(main_frame, text="Gestión de Contenido", padding="10")
        sections_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        sections_frame.columnconfigure(0, weight=1)
        sections_frame.columnconfigure(1, weight=1)
        
        # Botones de gestión
        ttk.Button(sections_frame, text="📧 Mensajes de Contacto", 
                  command=lambda: self.open_section("contactmessage")).grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(sections_frame, text="💼 Proyectos", 
                  command=lambda: self.open_section("project")).grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(sections_frame, text="⭐ Testimonios", 
                  command=lambda: self.open_section("testimonial")).grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(sections_frame, text="📝 Blog", 
                  command=lambda: self.open_section("blogpost")).grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Información del sistema
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        info_text = """
Credenciales de acceso:
• Usuario: admin
• Contraseña: admin123

URLs importantes:
• Panel Admin: http://localhost:5000/admin
• Frontend: http://localhost:5000
• API: http://localhost:5000/api

Para iniciar el servidor manualmente:
python backend/app.py
        """
        
        info_label = ttk.Label(info_frame, text=info_text.strip(), justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
    def check_server_status(self):
        """Verificar el estado del servidor"""
        def check():
            try:
                response = requests.get("http://localhost:5000/admin/", timeout=5)
                if response.status_code == 200:
                    self.status_label.config(text="✅ Servidor ejecutándose", foreground="green")
                else:
                    self.status_label.config(text="⚠️ Servidor con problemas", foreground="orange")
            except requests.exceptions.RequestException:
                self.status_label.config(text="❌ Servidor no encontrado", foreground="red")
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=check, daemon=True).start()
        
    def open_admin_panel(self):
        """Abrir panel de administración"""
        webbrowser.open("http://localhost:5000/admin/")
        
    def open_frontend(self):
        """Abrir frontend del sitio"""
        webbrowser.open("http://localhost:5000/")
        
    def open_api(self):
        """Abrir documentación de API"""
        webbrowser.open("http://localhost:5000/api/")
        
    def open_section(self, section):
        """Abrir sección específica del admin"""
        url = f"http://localhost:5000/admin/{section}/"
        webbrowser.open(url)
        
    def restart_server(self):
        """Reiniciar el servidor"""
        result = messagebox.askyesno("Reiniciar Servidor", 
                                   "¿Estás seguro de que quieres reiniciar el servidor?\n\nEsto cerrará todas las conexiones activas.")
        if result:
            try:
                # Intentar detener procesos Python existentes
                subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                             capture_output=True, text=True)
                
                # Esperar un momento
                import time
                time.sleep(2)
                
                # Iniciar servidor
                subprocess.Popen(["python", "backend/app.py"], 
                               cwd="..",  # Directorio padre
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                
                messagebox.showinfo("Servidor", "Servidor reiniciado correctamente")
                self.check_server_status()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al reiniciar servidor: {str(e)}")

def main():
    root = tk.Tk()
    app = AdminDesktopApp(root)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
