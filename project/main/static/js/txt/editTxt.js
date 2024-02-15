function start() {
    let now_ = document.createElement('div')
    edit_text.append(now_)
    let now = document.createElement('span')
    now_.append(now)

    if (text.value.length == 0) {
        now.textContent = "none"
        return
    }

    for (let i = 0; i < text.value.length; ++i) {
        if (text.value[i] == '\n') {
            now_ = document.createElement('div')
            edit_text.append(now_)
            now = document.createElement('span')
            now_.append(now)
        } else now.textContent += text.value[i]
    }
}

function UpdateText() {
    let ans = ""
    for (let el of edit_text.querySelectorAll("div")) {
        for (let el_ of el.querySelectorAll("span"))
            ans += el_.textContent
        ans += "\n"
    }
    text.textContent = ans
}

let STOPDELETE = 0

function UpdateEditText(e) {
    if (edit_text.querySelectorAll("div").length == 0) {
        window.open('/edit', '_self')
    }
}

save.onclick = function() {UpdateText(); SAVE()}

edit_text.onkeyup = UpdateEditText

edit_text.onkeydown = function(e) {
    if (e.key == 'Control') return true
    if (STOPDELETE == 0 && e.code == 'KeyA' && e.ctrlKey) STOPDELETE = 1
    else if (STOPDELETE == 1 && (e.code == 'Backspace' || (e.code == 'KeyX' && e.ctrlKey) || e.code == 'Delete')) {
        /*window.open('/edit', '_self')
        UpdateText()
        SAVE()*/
        return false
    } else STOPDELETE = 0
}

edit_text.oncut = function(e) {
    if (STOPDELETE == 1) e.clipboardData()
}

start()