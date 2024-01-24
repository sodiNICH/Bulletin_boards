var url = location.href;
var match = url.match(/\/profile\/(\d+)\/$/);
var id = match[1];
console.log(id);

$(document).ready(function () {
    $.ajax({
        url: `/profile/user/api/${id}`,
        type: "GET",
        success: function (data) {
            $('title').text(data.username);
            var newHTML = '<img src="" alt="" id="user-avatar">' +
                `<h1 id="username">${data.username}</h1>` +
                `<p id="description">${data.description}</p>`;

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