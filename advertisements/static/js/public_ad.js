$(document).ready(function () {
    $("#ad-create-form").submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/ad/api/',
            method: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response.message);
            },
            error: function (xhr) {
                console.log(xhr.responseJSON);
            }
        });
    });
});