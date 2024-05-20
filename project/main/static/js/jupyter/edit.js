arr = []

function add(text) {
    let q = document.createElement('div'), w = document.createElement('tr')
    w.id = 'tr_' + arr.length.toString()
    table_main.append(w)
    let e = document.createElement('td')
    e.classList.add('stol')
    w.append(e)
    e.innerHTML = `<p style='color: white'>${arr.length}</p><button class="but" onclick="Up(${arr.length})">↑</button><button class="but" onclick="Del(${arr.length})">-</button><button class="but" onclick="Down(${arr.length})">↓</button>`
    e = document.createElement('td')
    w.append(e)
    e.append(q)

    let el = CodeMirror(q, {
             value: text,
             mode: style.value,
             lineNumbers: true,
             indentUnit: 4,
             viewportMargin: Infinity,
            })
    //el.theme({'&': {  }})
    el.setSize(window.screen.width - q.getBoundingClientRect().x - 75, "auto")
    el.addKeyMap({'Ctrl-S': SAVE})
    arr.push(el)
}

for (let i = 0; i < Number(input_count.innerText); ++i) {
    add(document.getElementById('input_' + i.toString()).innerText)
}

function Up(id) {
    if (id > 0) {
        document.getElementById('tr_' + id.toString()).id = 'swap'
        let q = document.getElementById('tr_' + (id - 1).toString())
        q.remove()
        swap.after(q)
        q.firstChild.innerHTML = q.firstChild.innerHTML.replaceAll((id - 1).toString(), id.toString())
        q.id = 'tr_' + id.toString()
        swap.firstChild.innerHTML = swap.firstChild.innerHTML.replaceAll(id.toString(), (id - 1).toString())
        swap.id = 'tr_' + (id - 1).toString()
    }
}

function Down(id) {
    if (id < arr.length - 1) {
        document.getElementById('tr_' + id.toString()).id = 'swap'
        let q = document.getElementById('tr_' + (id + 1).toString())
        q.remove()
        swap.before(q)
        q.firstChild.innerHTML = q.firstChild.innerHTML.replaceAll((id + 1).toString(), id.toString())
        q.id = 'tr_' + id.toString()
        swap.firstChild.innerHTML = swap.firstChild.innerHTML.replaceAll(id.toString(), (id + 1).toString())
        swap.id = 'tr_' + (id + 1).toString()
    }
}

function Del(id) {
    arr.splice(id, 1)
    document.getElementById('tr_' + id.toString()).remove()
    for (let i = id + 1; i <= arr.length; ++i) {
        document.getElementById('tr_' + i.toString()).firstChild.innerHTML =
            document.getElementById('tr_' + i.toString()).firstChild.innerHTML.replaceAll(i.toString(), (i - 1).toString())
        document.getElementById('tr_' + i.toString()).id = 'tr_' + (i - 1).toString()
    }

    if (arr.length == 0)
        add('')
}

function SelectStyle() {
    for (let i = 0; i < arr.length; ++i) {
        arr[i].setOption('mode', style.value)
    }
}

function SAVE() {
    let q = document.createElement('input')
    q.type = 'text'
    q.name = 'count'
    q.value = arr.length.toString()
    main_form.append(q)
    for (let i = 0; i < arr.length; ++i) {
        q = document.createElement('textarea')
        q.name = 'block_' + i.toString()
        q.value = arr[i].getValue()
        main_form.append(q)
    }
    main_form.submit()
}

save.onclick = SAVE

SelectStyle()