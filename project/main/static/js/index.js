function COPY_TEXT(text) {
    navigator.clipboard.writeText(text)
    up_text.hidden = false
    setTimeout(function() {up_text.hidden = true}, 1000)
}

/*canvas.height = 2000
canvas.width = 2000
let arr = [], draw = canvas.getContext('2d')
function Add() {
    arr.push([image.getBoundingClientRect().x, image.getBoundingClientRect().y, Math.random() * 50 - 25, 0])
}

function Go() {
    draw.fillStyle = "#ffffff"
    draw.clearRect(0, 0, 2000, 2000)
    for (let i = 0; i < arr.length; ++i) {
        if (arr[i][2] <= 2000) {
            arr[i][0] += arr[i][2]
            arr[i][1] += arr[i][3]
            arr[i][3] += 0.5
            draw.drawImage(image, arr[i][0], arr[i][1], 50, 50)
        }
    }
}

setInterval(Go, 10)*/