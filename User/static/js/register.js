$(document).ready(function () {
    $("#id_password1").on("input", handleInputPassword);
    $("#id_username").on("input", handleInputUsername);

    var disabled = {
        username: false,
        password: false,
    }

    function disabledCheck (disabled) {
        if (disabled.username && disabled.password) {
            $("#register-button").prop("disabled", false);
            console.log("Данные валидные");
        } else {
            $("#register-button").prop("disabled", true);
            console.log("Данные не валидные");
        };
    };

    function handleInputUsername () {
        var username = $("#id_username").val();
        console.log(username);

        var requestData = {
            username: username
        };

        $.ajax({
            url: '/profile/api/v1/register/validated/',
            method: 'POST',
            data: requestData,
            dataType: 'json',
            success: function(response) {
                console.log(response);
                $("#warning-valid-username").empty();
                $("#id_username").attr("class", "form-control valid_form")
                setTimeout(function () {
                    $("#id_username").attr("class", "form-control");
                }, 2000);
                disabled.username = true;
                disabledCheck(disabled);
            },
            error: function(xhr) {
                var errors_json = xhr.responseJSON;
                $("#warning-valid-username").empty();
                $("#warning-valid-username").append(`<strong style="color: #db5555">${errors_json.error.slice(2, -2)}</strong>`);
                $("#id_username").attr("class", "form-control warning-form")
                disabled.username = false;
                disabledCheck(disabled);
            }
        });
    };

    function handleInputPassword () {
        var password = $("#id_password1").val();
        console.log(password);

        var requestData = {
            password: password
        };

        $.ajax({
            url: '/profile/register/validated/api/',
            method: 'POST',
            data: requestData,
            dataType: 'json',
            success: function(response) {
                console.log(response);
                $("#warning-valid-password").empty();
                $("#id_password1").attr("class", "form-control valid_form")
                setTimeout(function () {
                    $("#id_password1").attr("class", "form-control");
                }, 2000);
                disabled.password = true;
                disabledCheck(disabled);
            },
            error: function(xhr) {
                var errors_json = xhr.responseJSON;
                $("#warning-valid-password").empty();
                $("#warning-valid-password").append(`<strong style="color: #db5555">${errors_json.error.slice(2, -2)}</strong>`);
                $("#id_password1").attr("class", "form-control warning-form")
                disabled.password = false;
                disabledCheck(disabled);
            }
        });
    };

    $('#register-form').submit(function (event) {
        event.preventDefault();
        let formData = $(this).serializeArray();
        let form = {};
        $.each(formData, function(index, field) {
            if (field.name === 'username') {
                form[field.name] = field.value;
            };
            if (field.name === 'password1') {
                form['password'] = field.value;
            };
        });
        console.log(form)

        $.ajax({
            url: "/profile/user/api/",
            type: "POST",
            dataType: 'json',
            data: JSON.stringify(form),
            contentType: 'application/json',
            success: function (data) {
                console.log('Все норм');
                window.location.href = `/profile/${data.id}/`
            },
            error: function (xhr) {
                let error = xhr.responseJSON;
                console.log(error);
            },
        });
    });
});