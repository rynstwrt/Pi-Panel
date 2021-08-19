const buttonContainer = document.getElementById("button-container")

fetch("http://localhost:5000/getbuttons")
.then(resp => resp.json())
.then(data =>
{
    const buttonList = data.buttons

    for (i in buttonList)
    {
        const button_text = buttonList[i]
        const button = document.createElement("button")
        button.textContent = button_text

        button.addEventListener("click", () =>
        {
            fetch("http://localhost:5000/setprogram", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"program": button_text})
            })
        })

        buttonContainer.appendChild(button)
    }
})
