function createTextLine(del = false) {
    let now_ = document.createElement('div')
    edit_text.append(now_)
    let now = document.createElement('span')
    now_.append(now)
    return now
}

function start() {
    let now = createTextLine(true)

    if (text.value.length == 0) {
        now.textContent = "none"
        return
    }

    for (let i = 0; i < text.value.length; ++i) {
        if (text.value[i] == '\n') {
            if (now.textContent == '') {
                let q = document.createElement('br')
                q.contentEditable = "false"
                now.append(q)
            }
            now = createTextLine()
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

save.onclick = function() {UpdateText(); SAVE()}

function UpdateEditText(e) {
    //return true
    if (edit_text.querySelector('div').textContent == "") {
        let q = edit_text.querySelector('div')
        q.contentEditable = "false"
        let arr = q.querySelectorAll('span')
        if (arr.length == 0) {
            let w = document.createElement('span')
            w.contentEditable = "true"
            q.append(w)
        } else arr[0].contentEditable = "true"
    } else edit_text.querySelector('div').contentEditable = "true"

    /*for (let i of edit_text.querySelectorAll('div'))
        for (let j of i.querySelectorAll('*'))
            if (j instanceof HTMLSpanElement)
                break
            else {
                j.remove()
                }*/

    for (let i of edit_text.querySelectorAll('br'))
        i.contentEditable = 'false'

    return true
}

edit_text.onkeydown = UpdateEditText

/*let STOPDELETE = 0

function UpdateEditText(e) {
    if (edit_text.querySelectorAll("div").length == 0) {
        window.open('/edit', '_self')
    }
}

edit_text.onkeyup = UpdateEditText

edit_text.onkeydown = function(e) {
    if (e.key == 'Control') return true
    if (STOPDELETE == 0 && e.code == 'KeyA' && e.ctrlKey) STOPDELETE = 1
    else if (STOPDELETE == 1 && (e.code == 'Backspace' || (e.code == 'KeyX' && e.ctrlKey) || e.code == 'Delete')) {
        return false
    } else STOPDELETE = 0
}*/

/*edit_text.oncut = function(e) {
    if (STOPDELETE == 1) e.clipboardData()
}*/

/*clear_button.onclick = function() {
    if (confirm('Вы уверены?')) {
        for (let i of edit_text.querySelectorAll('*'))
            i.remove()
        createTextLine().textContent = 'none'
    }
}*/

start()