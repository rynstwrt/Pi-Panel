const exitButton = document.getElementById("exit-button")
const refreshButton = document.getElementById("reload-button")
const ipcRenderer = require("electron").ipcRenderer

exitButton.addEventListener("click", () =>
{
    ipcRenderer.invoke("close-button-clicked")
})

refreshButton.addEventListener("click", () =>
{
    ipcRenderer.invoke("reload-button-clicked")
})