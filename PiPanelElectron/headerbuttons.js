const exitButton = document.getElementById("exit-button")
const refreshButton = document.getElementById("refresh-button")
const ipcRenderer = require("electron").ipcRenderer

exitButton.addEventListener("click", () =>
{
    ipcRenderer.invoke("close-button-clicked")
})

refreshButton.addEventListener("click", () =>
{
    ipcRenderer.invoke("refresh-button-clicked")
})