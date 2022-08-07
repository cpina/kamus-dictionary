$(document).ready(function () {
    $.fn.select2.defaults.set("theme", "bootstrap-5");
});

$(document).on('select2:open', (e) => {
    const selectId = e.target.id;
    $(".select2-search__field[aria-controls='select2-" + selectId + "-results']").each(function (key, value,) {
        value.focus();
    });
});
