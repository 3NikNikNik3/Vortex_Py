let sizeX
let now_select = 0, max_ = 0
let change = false

function Select(id) {
    change = false
    let q = document.getElementById("li_" + now_select.toString())
    for (let i = 0; i < 2 & q != null; ++i) {
        q.style.backgroundColor = "rgb(50, 50, 50)"
        q.style.color = "rgb(200, 200, 200)"
        if (i == 0) q = document.getElementById("li2_" + now_select.toString())
    }
    q = document.getElementById("li_" + id.toString())
    for (let i = 0; i < 2; ++i) {
        q.style.backgroundColor = "rgb(200, 200, 200)"
        q.style.color = "rgb(50, 50, 50)"
        if (i == 0) q = document.getElementById("li2_" + id.toString())
    }
    now_select = id
}

function f(e) {Select(Number(e.target.id.substr(3)))}
function f_(e) {Select(Number(e.target.id.substr(4)))}

function GetChar(id) {
    id = parseInt(id, 16)
    if (id == 10) return "\\n"
    else if (id == 13) return "\\r"
    else if (id == 9) return "\\t"
    else if (id == 8) return "\\b"
    else if (id == 12) return "\\f"
    else if (id == 11) return "\\v"
    return String.fromCharCode(id)
}

function load(e) {
    if (e == '') e = "00"
    sizeX = Math.floor(window.innerWidth / 2 / 23)
    //tab.style.width = (sizeX * 23 + 20).toString() + "px"
    let now, now2
    let count = sizeX
    max_ = 0
    for (let i = 0; i < e.length / 2; ++i) {
        if (count >= sizeX) {
            count = 0
            now = document.createElement('tr')
            now2 = document.createElement('tr')
            tab.appendChild(now)
            tab2.appendChild(now2)
        }
        let q = document.createElement('td')
        q.id = "li_" + i.toString()
        q.innerText = e[2 * i] + e[2 * i + 1]
        q.onclick = f
        q.style.backgroundColor = "rgb(50, 50, 50)"
        q.style.color = "rgb(200, 200, 200)"
        now.appendChild(q)
        let w = document.createElement('td')
        w.id = "li2_" + i.toString()
        w.innerText = GetChar(e[2 * i] + e[2 * i + 1])
        w.onclick = f_
        w.style.backgroundColor = "rgb(50, 50, 50)"
        w.style.color = "rgb(200, 200, 200)"
        now2.appendChild(w)
        max_ += 1
        count += 1
    }
}

function KeyOn(e) {
    if (e.code == "ArrowLeft" & document.getElementById("li_" + (now_select - 1).toString()) != null) {
        Select(now_select - 1)
        e.preventDefault()
    }
    else if (e.code == "ArrowRight" & document.getElementById("li_" + (now_select + 1).toString()) != null) {
        Select(now_select + 1)
        e.preventDefault()
    }
    else if (e.code == "ArrowUp" & document.getElementById("li_" + (now_select - sizeX).toString()) != null) {
        Select(now_select - sizeX)
        e.preventDefault()
    }
    else if (e.code == "ArrowDown" & document.getElementById("li_" + (now_select + sizeX).toString()) != null) {
        Select(now_select + sizeX)
        e.preventDefault()
    }
    else if (e.key == "a" | e.key == "b" | e.key == "c" | e.key == "d" | e.key == "e" | e.key == "f" | Number(e.key).toString() != "NaN") {
        if (!change) {
            document.getElementById("li_" + now_select.toString()).innerText = e.key.toUpperCase() + document.getElementById("li_" + now_select.toString()).innerText[1]
            change = true
        } else {
            document.getElementById("li_" + now_select.toString()).innerText = document.getElementById("li_" + now_select.toString()).innerText[0] + e.key.toUpperCase()
            change = false
        }
        document.getElementById("li2_" + now_select.toString()).innerText = GetChar(document.getElementById("li_" + now_select.toString()).innerText)
    }
}

// yes, I know...
function KeyOn2(e) {
    if (e.code == "ArrowLeft" & document.getElementById("li2_" + (now_select - 1).toString()) != null) {
        Select(now_select - 1)
        e.preventDefault()
    }
    else if (e.code == "ArrowRight" & document.getElementById("li2_" + (now_select + 1).toString()) != null) {
        Select(now_select + 1)
    }
    else if (e.code == "ArrowUp" & document.getElementById("li2_" + (now_select - sizeX).toString()) != null) {
        Select(now_select - sizeX)
        e.preventDefault()
    }
    else if (e.code == "ArrowDown" & document.getElementById("li2_" + (now_select + sizeX).toString()) != null){
        Select(now_select + sizeX)
        e.preventDefault()
    }
    else if (e.key.length == 1 & e.key.charCodeAt() < 256) {
        document.getElementById("li2_" + now_select.toString()).innerText = e.key
        document.getElementById("li_" + now_select.toString()).innerText = e.key.charCodeAt().toString(16)
    }
}

function UpdatePage() {
    ioput.value = ''
    let q = document.getElementById("li_0")
    for (let i = 1; q != null; ++i) {
        ioput.value += q.innerText
        q = document.getElementById("li_" + i.toString())
    }
    while (tab.childNodes.length != 0)
        tab.removeChild(tab.firstChild)
    while (tab2.childNodes.length != 0)
        tab2.removeChild(tab2.firstChild)
    load(ioput.value)
}

function AddByte() {
    let q = Number(prompt('Сколько?'))
    if (q.toString != "NaN") {
        let now = tab.lastChild, now2 = tab2.lastChild
        for (let i = 0; i < q; ++i) {
            if (max_ % sizeX == 0) {
                now = document.createElement('tr')
                now2 = document.createElement('tr')
                tab.appendChild(now)
                tab2.appendChild(now2)
            }
            let q = document.createElement('td')
            q.id = "li_" + max_.toString()
            q.innerText = '00'
            q.onclick = f
            q.style.backgroundColor = "rgb(50, 50, 50)"
            q.style.color = "rgb(200, 200, 200)"
            now.appendChild(q)
            let w = document.createElement('td')
            w.id = "li2_" + max_.toString()
            w.innerText = GetChar('00')
            w.onclick = f_
            w.style.backgroundColor = "rgb(50, 50, 50)"
            w.style.color = "rgb(200, 200, 200)"
            now2.appendChild(w)
            max_ += 1
        }
    }
}

function DelByte() {
    let q = Number(prompt('Сколько?'))
    if (q.toString != "NaN") {
        while (tab.lastChild.childElementCount <= q) {
            q -= tab.lastChild.childElementCount
            max_ -= tab.lastChild.childElementCount
            tab.lastChild.remove()
            tab2.lastChild.remove()

            if (tab.childElementCount == 0) {
                let now = document.createElement('tr')
                let now2 = document.createElement('tr')
                tab.appendChild(now)
                tab2.appendChild(now2)
                let q = document.createElement('td')
                q.id = "li_0"
                q.innerText = '00'
                q.onclick = f
                q.style.backgroundColor = "rgb(50, 50, 50)"
                q.style.color = "rgb(200, 200, 200)"
                now.appendChild(q)
                let w = document.createElement('td')
                w.id = "li2_0"
                w.innerText = GetChar('00')
                w.onclick = f_
                w.style.backgroundColor = "rgb(50, 50, 50)"
                w.style.color = "rgb(200, 200, 200)"
                now2.appendChild(w)
                max_ = 1
            }
        }

        if (q != 0)
            for (; q != 0; --q) {
                max_ -= 1
                tab.lastChild.lastChild.remove()
                tab2.lastChild.lastChild.remove()
            }

        if (now_select >= max_)
            Select(max_ - 1)
    }
}

function Go() {
    let add_count = Number(prompt('На сколько? (можно отрицательный)'))
    if (add_count.toString() != 'Nan') {
        for (let i = 0; i < max_; ++i) {
            let q = (parseInt(document.getElementById('li_' + i.toString()).innerText, 16) + add_count) % 256
            document.getElementById("li_" + i.toString()).innerText = q.toString(16)
            document.getElementById("li2_" + i.toString()).innerText = GetChar(q.toString(16))
        }
    }
}

tab.onkeydown = KeyOn
tab2.onkeydown = KeyOn2

save.onclick = function() {
    ioput.value = ''
    let q = document.getElementById("li_0")
    for (let i = 1; q != null; ++i) {
        ioput.value += q.innerText
        q = document.getElementById("li_" + i.toString())
    }
    main_form.submit()
}

load(ioput.value)
Select(0)