$(document).ready(function () {
    $('#login-form').submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: "/profile/api/v1/login/",
            type: 'POST',
            data: $(this).serialize(),
            success: function (data) {
                console.log(data);
                location.href = `/profile/${data.id}/`;
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log(xhr.status);
                if (xhr.status === 400) {
                    $(".form-text").text("Неверно введен пароль или логин");
                } else {
                    $(".form-text").text("Произошла ошибка. Пожалуйста, попробуйте еще раз.");
                };
            },
        });
    });
});