$(document).ajaxError(function (event, xhr, settings, thrownError) {
    if (xhr.status == 318) {
        text = xhr.responseText;
        data = JSON.parse(text);
        referer = data.referer;
        window.location.href = "/?url=" + referer
    }
});