$(document).ready(function () {
    $.fn.select2.defaults.set("theme", "bootstrap-5");

    // If the user types something in the autocomplete and then click
    // "Translate": it closes the autocomplete and submits the form
    // (so the user does not need to close the autocomplete before
    // pressing Translate)
    $.fn.select2.defaults.set("selectOnClose", true);
});


// Clicking the select2 puts the cursor inside to start typing straight away
$(document).on('select2:open', (e) => {
    const selectId = e.target.id;
    $(".select2-search__field[aria-controls='select2-" + selectId + "-results']").each(function (key, value,) {
        value.focus();
    });
});

// When click on an option: submit the form
$(document).on('select2:select', function () {
    let form = $('form')[0];

    if (form.checkValidity()) {
        form.submit();
    } else {
        form.reportValidity();
    }
});

// From: https://stackoverflow.com/a/49261426/9294284
// on focus open the select2 (for example on TAB)
$(document).on('focus', '.select2-selection.select2-selection--single', function (e) {
    $(this).closest(".select2-container").siblings('select:enabled').select2('open');
});
// steal focus during close - only capture once and stop propagation
$('select.select2').on('select2:closing', function (e) {
    $(e.target).data("select2").$selection.one('focus focusin', function (e) {
        e.stopPropagation();
    });
});

