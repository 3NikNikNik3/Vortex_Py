var myCodeMirror = CodeMirror(edit_text, {
  value: text.value,
  mode: "text/x-csrc",
  lineNumbers: true
});

myCodeMirror.setSize(null, window.screen.height - edit_text.getBoundingClientRect().y - 150)
myCodeMirror.addKeyMap({'Ctrl-S': function(e) {text.value = myCodeMirror.getValue(); SAVE()}})
myCodeMirror.setOption('mode', sinte.value)

sinte.onchange = function() {
    myCodeMirror.setOption('mode', sinte.value)
}

save.onclick = function() {
    text.value = myCodeMirror.getValue()
    SAVE()
}