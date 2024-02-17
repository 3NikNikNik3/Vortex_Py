var myCodeMirror = CodeMirror(edit_text, {
  value: text.value,
  mode: "text/x-csrc",
  lineNumbers: true
});

myCodeMirror.setSize(null, window.screen.height - edit_text.getBoundingClientRect().y - 150)
myCodeMirror.addKeyMap({'Ctrl-S': function(e) {text.value = myCodeMirror.getValue(); SAVE()}})

save.onclick = function() {
    text.value = myCodeMirror.getValue()
    SAVE()
}