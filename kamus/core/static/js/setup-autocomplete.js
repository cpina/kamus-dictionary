//Any JavaScript related to the autocomplete

$(document).ready(function () {
    $.fn.select2.defaults.set("theme", "bootstrap-5");

    // If the user types something in the autocomplete and then click
    // "Translate": it closes the autocomplete and submits the form
    // (so the user does not need to close the autocomplete before
    // pressing Translate)
    $.fn.select2.defaults.set("selectOnClose", true);
});

function handle_key_press_search(event) {
    let target = event["target"];
    if (target["className"] === "select2-search__field" && event["keyCode"] === 13) {

        // TODO: get "Searching…" from select2... in case that it changes
        if ($("#select2-id_word-results li:first")[0].textContent === "Searching…") {
            let text = target.value

            let data = {
                id: text,
                text: text
            };

            let newOption = new Option(data.text, data.id, true, true);

            let word_select = $('#id_word');

            word_select.append(newOption).trigger('change');

            word_select.select2('close');

            submit_form();
        }
    }
}

function submit_form() {
    let form = $('form')[0];

    if (form.checkValidity()) {
        form.submit();
    } else {
        form.reportValidity();
    }

}

document.addEventListener('keydown', handle_key_press_search, true);

// Clicking the select2 puts the cursor inside to start typing straight away
$(document).on('select2:open', (e) => {
    const selectId = e.target.id;
    $(".select2-search__field[aria-controls='select2-" + selectId + "-results']").each(function (key, value,) {
        value.focus();
    });
});

// When click on an option: submit the form
$(document).on('select2:select', submit_form);

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

