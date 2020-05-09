function Insert_text(el, text, offset) {
    let val = el.value, endIndex;
    endIndex = el.selectionEnd;
    el.value = val.slice(0, endIndex) + text + val.slice(endIndex);
    el.selectionStart = el.selectionEnd = endIndex + text.length + (offset ? offset : 0);
}
