var id = $.cookie('user_id');
console.log(id);

$(document).ready(function () {
    $.ajax({
        url: `/profile/user/api/${id}/`,
        type: "GET",
        success: function (response) {
            console.log(response);
            var dataUser = $("#data-user");
            var dataLink = $("#user-link").attr("href", `/profile/${response.id}/`);
            dataLink.append($("<img>").attr("src", response.avatar).attr("id", "user-avatar-nav").attr("title", response.username));
            dataUser.append(dataLink);
        },
        error: function(xhr) {
            console.log(xhr.error);
        },
    });
});