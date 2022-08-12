$(document).ready(function () {
    function can_swap() {
        let from_select = $("#id_from");
        let to_select = $("#id_to");

        let from_language = from_select.val();
        let to_language = to_select.val();

        let from_languages = $('#id_from option');

        let can_swap = false;
        $(from_languages).each(function () {
            if (to_language === $(this).val()) {
                can_swap = true;
            }
        });
        return can_swap;
    }

    function enable_disable_swapper() {
        $("#swap").attr('disabled' , !can_swap());
    }

    enable_disable_swapper();

    $("#id_from").change(enable_disable_swapper);
    $("#id_to").change(enable_disable_swapper);

    $("#swap").click(function (e) {
        e.preventDefault();

        let from_select = $("#id_from");
        let to_select = $("#id_to");

        let from_language = from_select.val();
        let to_language = to_select.val();

        let from_languages = $('#id_from option');

        let can_swap = false;
        $(from_languages).each(function () {
            if (to_language === $(this).val()) {
                can_swap = true;
            }
        });

        if (can_swap) {
            from_select.val(to_language);
            to_select.val(from_language);
        }
    });
});
