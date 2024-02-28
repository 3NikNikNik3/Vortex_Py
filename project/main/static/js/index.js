function COPY_TEXT(text) {
    navigator.clipboard.writeText(text);
    up_text.hidden = false
    setTimeout(function() {up_text.hidden = true}, 1000)
}