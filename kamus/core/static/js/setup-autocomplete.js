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
    let form = $('form')[0];

    if (form.checkValidity()) {
        form.submit();
    } else {
        form.reportValidity();
    }
});

// From: https://stackoverflow.com/a/49261426/9294284
// on first focus (bubbles up to document), open the menu
$(document).on('focus', '.select2-selection.select2-selection--single', function (e) {
    $(this).closest(".select2-container").siblings('select:enabled').select2('open');
});

// steal focus during close - only capture once and stop propogation
$('select.select2').on('select2:closing', function (e) {
    $(e.target).data("select2").$selection.one('focus focusin', function (e) {
        e.stopPropagation();
    });
});
