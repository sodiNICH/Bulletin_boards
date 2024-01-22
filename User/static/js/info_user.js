var id = $.cookie('user_id');
console.log(id);

$(document).ready(function () {
    $.ajax({
        url: `/profile/user/api/${id}`,
        type: "GET",
        success: function (data) {
            $('title').text(data.username);
            $("#username").text(data.username);
            $("#description").text(data.description);
            var newHTML = '<img src="" alt="" id="user-avatar">' +
                '<h1 id="username">dsfdsf</h1>' +
                '<p id="description"></p>';

            $('#info-user').prepend(newHTML);

            if (data.avatar.length > 1) {
                $("#user-avatar").attr("src", data.avatar);
            } else {
                $("#user-avatar").after("<div class='empty-avatar'>👤</div>");
            };
            console.log(data);
        },
        error: function (error) {
            alert('Что то не так');
        },
    });
});