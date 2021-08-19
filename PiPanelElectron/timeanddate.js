const months = ["January", "Feburary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

const timeElem = document.getElementById("time")
const dateElem = document.getElementById("date")


function getFormattedTime()
{
    const time = new Date()
    let h = time.getHours()
    let m = time.getMinutes()
    let s = time.getSeconds()

    if (h > 12) h -= 12
    if (h == 0) h = 12
    if (h < 10) h = "0" + h

    if (m < 10) m = "0" + m

    if (s < 10) s = "0" + s

    return `${h}:${m}:${s}`
}


function getFormattedDate()
{
    const time = new Date()
    const day = days[time.getDay()]
    const month = months[time.getMonth()]
    const date = time.getDate()
    const year = time.getFullYear()

    return `${day}, ${month} ${date}, ${year}`
}


setInterval(() =>
{
    dateElem.textContent = getFormattedDate()
    timeElem.textContent = getFormattedTime()
}, 1000)