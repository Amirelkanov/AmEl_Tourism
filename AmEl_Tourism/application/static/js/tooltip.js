// Showing tooltip text on hover
function Show_tooltip(tooltip_id) {
    let tooltip = document.getElementById(tooltip_id);
    tooltip.innerHTML = "Скопировать";
}

// Copying coords function
function Copy_coords(span_id, tooltip_id) {
    let temp = $("<input>");
    $("body").append(temp);
    temp.val(document.getElementById(span_id).textContent).select();
    document.execCommand("copy");
    temp.remove();
    let tooltip = document.getElementById(tooltip_id);
    tooltip.innerHTML = "Скопировано";
}
