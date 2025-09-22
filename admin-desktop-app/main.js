const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');

// Mantener una referencia global del objeto window
let mainWindow;

function createWindow() {
  // Crear la ventana del navegador
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false
    },
    icon: path.join(__dirname, 'assets/icon.png'),
    titleBarStyle: 'default',
    show: false
  });

  // Cargar la URL del panel de administración
  mainWindow.loadURL('http://localhost:5000/admin/');

  // Mostrar la ventana cuando esté lista
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Abrir DevTools en desarrollo
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  // Manejar enlaces externos
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Crear menú personalizado
  createMenu();
}

function createMenu() {
  const template = [
    {
      label: 'Archivo',
      submenu: [
        {
          label: 'Recargar',
          accelerator: 'CmdOrCtrl+R',
          click: () => {
            mainWindow.reload();
          }
        },
        {
          label: 'Recargar Ignorando Cache',
          accelerator: 'CmdOrCtrl+Shift+R',
          click: () => {
            mainWindow.webContents.reloadIgnoringCache();
          }
        },
        { type: 'separator' },
        {
          label: 'Salir',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Ver',
      submenu: [
        {
          label: 'Pantalla Completa',
          accelerator: 'F11',
          click: () => {
            mainWindow.setFullScreen(!mainWindow.isFullScreen());
          }
        },
        {
          label: 'Zoom In',
          accelerator: 'CmdOrCtrl+Plus',
          click: () => {
            mainWindow.webContents.zoomLevel += 0.5;
          }
        },
        {
          label: 'Zoom Out',
          accelerator: 'CmdOrCtrl+-',
          click: () => {
            mainWindow.webContents.zoomLevel -= 0.5;
          }
        },
        {
          label: 'Zoom Reset',
          accelerator: 'CmdOrCtrl+0',
          click: () => {
            mainWindow.webContents.zoomLevel = 0;
          }
        }
      ]
    },
    {
      label: 'Navegación',
      submenu: [
        {
          label: 'Panel Principal',
          accelerator: 'CmdOrCtrl+1',
          click: () => {
            mainWindow.loadURL('http://localhost:5000/admin/');
          }
        },
        {
          label: 'Mensajes',
          accelerator: 'CmdOrCtrl+2',
          click: () => {
            mainWindow.loadURL('http://localhost:5000/admin/contactmessage/');
          }
        },
        {
          label: 'Proyectos',
          accelerator: 'CmdOrCtrl+3',
          click: () => {
            mainWindow.loadURL('http://localhost:5000/admin/project/');
          }
        },
        {
          label: 'Testimonios',
          accelerator: 'CmdOrCtrl+4',
          click: () => {
            mainWindow.loadURL('http://localhost:5000/admin/testimonial/');
          }
        },
        {
          label: 'Blog',
          accelerator: 'CmdOrCtrl+5',
          click: () => {
            mainWindow.loadURL('http://localhost:5000/admin/blogpost/');
          }
        }
      ]
    },
    {
      label: 'Herramientas',
      submenu: [
        {
          label: 'Frontend del Sitio',
          click: () => {
            shell.openExternal('http://localhost:5000');
          }
        },
        {
          label: 'API Endpoints',
          click: () => {
            shell.openExternal('http://localhost:5000/api/');
          }
        },
        { type: 'separator' },
        {
          label: 'Desarrollador',
          submenu: [
            {
              label: 'Abrir DevTools',
              accelerator: 'F12',
              click: () => {
                mainWindow.webContents.toggleDevTools();
              }
            }
          ]
        }
      ]
    },
    {
      label: 'Ayuda',
      submenu: [
        {
          label: 'Acerca de',
          click: () => {
            const { dialog } = require('electron');
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Acerca de',
              message: 'Noel Moreno Admin Panel',
              detail: 'Panel de administración desktop para el sitio web de Noel Moreno.\nVersión 1.0.0\n\nDesarrollado para gestionar proyectos, testimonios, mensajes y contenido del blog.'
            });
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Este método se llamará cuando Electron haya terminado de inicializarse
app.whenReady().then(createWindow);

// Salir cuando todas las ventanas estén cerradas
app.on('window-all-closed', () => {
  // En macOS es común que las aplicaciones y su barra de menú
  // permanezcan activas hasta que el usuario salga explícitamente con Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // En macOS es común recrear una ventana en la aplicación cuando el
  // icono del dock es clickeado y no hay otras ventanas abiertas
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Verificar que el servidor esté ejecutándose
app.on('ready', () => {
  const { net } = require('electron');
  
  const checkServer = () => {
    const request = net.request('http://localhost:5000/admin/');
    request.on('response', (response) => {
      if (response.statusCode === 200) {
        console.log('✅ Servidor encontrado');
      }
    });
    request.on('error', () => {
      console.log('❌ Servidor no encontrado. Asegúrate de que el backend esté ejecutándose.');
      const { dialog } = require('electron');
      dialog.showErrorBox(
        'Servidor no encontrado',
        'No se puede conectar al servidor backend.\n\nAsegúrate de que el servidor esté ejecutándose con:\npython backend/app.py'
      );
    });
    request.end();
  };

  // Verificar después de 2 segundos
  setTimeout(checkServer, 2000);
});
