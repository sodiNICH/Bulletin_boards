$(document).ready(function () {
    $("#ad-create-form").submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/api/v1/ad/',
            method: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response, textStatus, xhr) {
                window.location.href = "";
            },
            error: function (xhr) {
                console.log(xhr.responseJSON);
            }
        });
    });
});