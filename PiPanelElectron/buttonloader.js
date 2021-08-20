const buttonContainer = document.getElementById("right-panel")

fetch("http://localhost:5000/getbuttons")
.then(resp => resp.json())
.then(data =>
{
    const buttonList = data.buttons

    for (i in buttonList)
    {
        const buttonTextStr = buttonList[i].toUpperCase()
        const button = document.createElement("div")
        const buttonIcon = document.createElement("i")
        const buttonText = document.createElement("p")

        button.classList.add("button")
        buttonIcon.classList.add("fas")
        buttonIcon.classList.add("fa-laptop-code")
        button.appendChild(buttonIcon)
        buttonText.textContent = buttonTextStr
        button.appendChild(buttonText)
        buttonContainer.appendChild(button)

        button.addEventListener("click", () =>
        {
            fetch("http://localhost:5000/setprogram", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"program": buttonTextStr})
            })
        })
    }
})
