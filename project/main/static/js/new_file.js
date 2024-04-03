function ChangeType() {
    dop_op.innerHTML = document.getElementById(type_select.value).innerHTML.replaceAll('&lt;', '<').replaceAll('&gt;', '>')
}

ChangeType()