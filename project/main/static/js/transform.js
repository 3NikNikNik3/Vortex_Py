why.onchange = function() {
    option.innerHTML = document.getElementById('DIV' + why.value).innerHTML.replaceAll('&lt;', '<').replaceAll('&gt;', '>')
}

why.onchange()

button1.onclick = function() {
    type_.name = 'go'
    output.value = why.value
}

button2.onclick = function() {
    type_.name = 'save'
    output.value = why.value
}
