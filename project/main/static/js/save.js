function fromS(event) {
    event.preventDefault()
    if (name_.value == '') {
        alert('Ввидите имя файла')
        return false;
    }
    form.submit()
    return true;
}

function Back() {
    let q = window.location.search.search('from=')
    if (q == -1) window.open('/edit', '_self')
    else window.open(window.location.search.substr(q + 5), '_self')
}

form.addEventListener('submit', fromS)
button_.onclick = Back