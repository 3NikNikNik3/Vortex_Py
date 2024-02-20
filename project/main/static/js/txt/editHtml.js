var myCodeMirror = CodeMirror(editor, {
  value: text.value,
  mode: 'xml',
  htmlMode: true,
  lineNumbers: true
});

myCodeMirror.setSize(null, window.screen.height - editor.getBoundingClientRect().y - 150)
myCodeMirror.addKeyMap({'Ctrl-S': function(e) {text.value = myCodeMirror.getValue(); SAVE()}})

save.onclick = function() {
    text.value = myCodeMirror.getValue()
    SAVE()
}

let MODE = 0
change_button.onclick = function() {
    if (MODE == 0) {
        editor.hidden = true
        change_button.textContent = "К коду"
        //vis.innerHTML = myCodeMirror.getValue()
        text_to_load.value = myCodeMirror.getValue()
        form_to_load.submit()
        setTimeout(() => {
            vis.innerHTML = "<iframe src='static/js/txt/data/" + ID + ".html'>Произошла какая-то ошибка</iframe>"
        }, 100);
    } else {
        editor.hidden = false
        change_button.textContent = "К виду"
        vis.innerHTML = ""
    }
    MODE = (MODE + 1) % 2
}

ID = id_user.textContent