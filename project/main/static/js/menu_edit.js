function DOWNLOAD() {
    if (confirm('Все несохранёные изменения будут потеряны!')) {
        window.open('save?from=' + window.location.pathname, '_self')
    }
}

function SAVE() {
    main_form.submit()
}

function LOAD() {
    if (confirm('Нынешний файл будет удалён!')) {
        window.open('load', '_self')
    }
}

download.onclick = DOWNLOAD
save.onclick = SAVE
load.onclick = LOAD
transform.onclick = function() {
    if (confirm('Все несохранёные изменения будут потеряны!')) {
        window.open('transform', '_self')
    }
}

new_file.onclick = function() {
    if (confirm('Нынешний файл будет удалён!')) {
        window.open('new', '_self')
    }
}