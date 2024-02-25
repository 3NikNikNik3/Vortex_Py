why.onchange = function() {
    option.innerHTML = document.getElementById('DIV' + why.value).innerHTML
}

option.innerHTML = document.getElementById('DIV' + why.value).innerHTML

form1.onsubmit = function() {
    output1.value = why.value
    form1.submit()
}

form2.onsubmit = function() {
    output2.value = why.value
    form2.submit()
}