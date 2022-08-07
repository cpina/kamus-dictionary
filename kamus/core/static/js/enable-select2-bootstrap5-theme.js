$(document).ready(function () {
    $.fn.select2.defaults.set("theme", "bootstrap-5");
});

$(document).on('select2:open', (e) => {
    const selectId = e.target.id;
    $(".select2-search__field[aria-controls='select2-" + selectId + "-results']").each(function (key, value,) {
        value.focus();
    });
});

// TODO attach only to the correct thing
$('*').on('select2:select', function () {
    $('form')[0].submit();
});
