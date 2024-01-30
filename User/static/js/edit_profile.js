var id = $.cookie('user_id');
console.log(id);

$(document).ready(function () {
    $("#avatarInput").change(function () {
        var input = this;

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $("#avatarButton").attr("style", `background-image: url('${e.target.result}')`);
            };

            reader.readAsDataURL(input.files[0]);
        };
    });
    $.ajax({
        url: `/profile/user/api/${id}/`,
        type: "GET",
        success: function (response) {
            console.log(response);
            $("title").text(response.username);
            $("#username").val(response.username);
            $("#description").val(response.description);
            $("#avatarButton").attr("style", `background-image: url('${response.avatar}')`);
        },
        error: function (error) {
            alert("Что то пошло не так");
        },
    });
    $("#profile-edit-form").submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        console.log(id);
        $.ajax({
            url: `/profile/user/api/${id}/`,
            type: 'PATCH',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response);
                location.href = `/profile/${id}`;
            },
            error: function (error) {
                alert("Что то пошло не так")
            }
        });
    });
});