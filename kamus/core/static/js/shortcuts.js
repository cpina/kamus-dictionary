document.addEventListener("keydown", function(event) {
    if (event.altKey && (event.key === 'c' || event.key === 'C'))
    {
        event.preventDefault();
        swap_languages();
    }
});

document.addEventListener("keydown", function(event) {
    if (event.altKey && (event.key === 'w' || event.key === 'W'))
    {
        event.preventDefault();
        $('#id_word').select2('open');
    }
});
