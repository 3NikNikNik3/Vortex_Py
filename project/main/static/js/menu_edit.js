function DOWNLOAD() {
    if (confirm('Все несохранёные изменения будут потеряны!')) {
        window.open('save?from=' + window.location.pathname, '_self')
    }
}

function SAVE() {
    main_form.submit()
}

download.onclick = DOWNLOAD
save.onclick = SAVE