# Noel Moreno Admin Panel - Aplicación Desktop

Esta es una aplicación de escritorio para gestionar el panel de administración de Noel Moreno Website.

## 🚀 Instalación

### Prerrequisitos
- Node.js (versión 16 o superior)
- El servidor backend ejecutándose en http://localhost:5000

### Pasos de instalación

1. **Instalar dependencias:**
```bash
cd admin-desktop-app
npm install
```

2. **Ejecutar la aplicación:**
```bash
npm start
```

3. **Compilar para distribución (opcional):**
```bash
npm run build
```

## 🎯 Características

- ✅ **Interfaz nativa**: Aplicación de escritorio con menús y atajos de teclado
- ✅ **Navegación rápida**: Atajos de teclado para acceder a cada sección
- ✅ **Zoom integrado**: Control de zoom para mejor visualización
- ✅ **Pantalla completa**: Modo pantalla completa para trabajo enfocado
- ✅ **Menú contextual**: Acceso rápido a funciones comunes
- ✅ **Verificación de servidor**: Alerta si el backend no está ejecutándose

## ⌨️ Atajos de Teclado

- `Ctrl+R` - Recargar página
- `Ctrl+Shift+R` - Recargar ignorando cache
- `F11` - Pantalla completa
- `Ctrl+Plus` - Zoom in
- `Ctrl+-` - Zoom out
- `Ctrl+0` - Reset zoom
- `Ctrl+1` - Panel principal
- `Ctrl+2` - Mensajes
- `Ctrl+3` - Proyectos
- `Ctrl+4` - Testimonios
- `Ctrl+5` - Blog
- `F12` - Abrir DevTools

## 📁 Estructura del Proyecto

```
admin-desktop-app/
├── main.js          # Archivo principal de Electron
├── package.json     # Configuración y dependencias
├── README.md        # Este archivo
└── assets/          # Iconos y recursos
```

## 🔧 Desarrollo

Para desarrollo, puedes usar:
```bash
NODE_ENV=development npm start
```

Esto abrirá automáticamente las herramientas de desarrollador.

## 📦 Distribución

Para crear ejecutables para distribución:

```bash
# Windows
npm run build

# Los archivos se generarán en la carpeta dist/
```

## 🐛 Solución de Problemas

### Error: "Servidor no encontrado"
- Asegúrate de que el servidor backend esté ejecutándose
- Ejecuta: `python backend/app.py`
- Verifica que esté en http://localhost:5000

### La aplicación no inicia
- Verifica que Node.js esté instalado
- Ejecuta `npm install` para instalar dependencias
- Verifica que el puerto 5000 esté libre
