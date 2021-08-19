const  { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

let win

function createWindow () { 
    win = new BrowserWindow({
        width: 1024, 
        height: 600, 
        fullscreen: true,
        webPreferences: { 
            nodeIntegration: true,  
            contextIsolation: false
        }
    })

    win.removeMenu()

    win.loadURL("file://" + path.join(__dirname, "/index.html"))

    // win.webContents.openDevTools()

    win.on('closed', () => {
        win = null
    })

    ipcMain.handle("close-button-clicked", () =>
    {
        app.exit(0)
    })

    ipcMain.handle("refresh-button-clicked", () =>
    {
        win.reload()
    })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (win === null) {
        createWindow()
    }
})
