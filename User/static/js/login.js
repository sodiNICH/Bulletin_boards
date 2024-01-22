$(document).ready(function () {
    $('#login-form').submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: "/profile/login/api/",
            type: 'POST',
            data: $(this).serialize(),
            success: function (data) {
                console.log(data);
                location.href = `/profile/${data.id}/`;
            },
            error: function (error) {
                alert('Что то пошло не так');
            },
        });
    });
});