var myCodeMirror = CodeMirror(edit_text, {
  value: text.value,
  mode: "text/x-csrc",
  lineNumbers: true
});

save.onclick = function() {
    text.value = myCodeMirror.getValue()
    SAVE()
}