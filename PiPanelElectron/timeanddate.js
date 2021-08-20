const months = ["January", "Feburary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

const timeElem = document.getElementById("time")
const dateElem = document.getElementById("date")


function getFormattedTime()
{
    const time = new Date()
    let h = time.getHours()
    let m = time.getMinutes()

    if (h > 12) h -= 12
    if (h == 0) h = 12
    if (h < 10) h = "0" + h

    if (m < 10) m = "0" + m

    return `${h}:${m}`
}


function getFormattedDate()
{
    const time = new Date()
    const day = days[time.getDay()]
    const month = months[time.getMonth()]
    const date = time.getDate()

    return `${day}, ${month} ${date}`
}


setInterval(() =>
{
    dateElem.textContent = getFormattedDate()
    timeElem.textContent = getFormattedTime()
}, 2000)