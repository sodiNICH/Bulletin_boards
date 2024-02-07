$(document).ready(function () {
    var tag = $("#create_ad");
    var id = $.cookie('user_id');
    console.log(id);
    if (id != undefined) {
        $.ajax({
            url: `/profile/user/api/${id}/`,
            type: "GET",
            success: function (response) {
                console.log(response);
                tag.after($(`<div id="data-user">
                                <a href="" id="user-link"></a>
                            </div>
                            <button id='exit-button' class="auth-button" onclick="logout()" type='button' alt='Выйти'><i class='bx bxs-log-out'></i></button>`
                ));
                var dataUser = $("#data-user");
                var dataLink = $("#user-link").attr("href", `/profile/${response.id}/`);
                dataLink.append($("<img>").attr("src", response.avatar).attr("id", "user-avatar-nav").attr("title", response.username));
                dataUser.append(dataLink);
            },
            error: function (xhr) {
                console.log(xhr.error);
            },
        });
    } else {
        tag.after($(`
            <a href="/profile/register/">
                <button id='register-button' class="auth-button" type='button' alt='Зарегистрироваться'><i class='bx bxs-user-pin'></i></button>
            </a>
            <a href="/profile/login/">
                <button id='login-button' class="auth-button" type='button' alt='Войти'><i class='bx bxs-log-in'></i></button>
            </a>
        `))
    };
});