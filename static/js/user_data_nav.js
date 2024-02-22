$(document).ready(function () {
    var nav = $(`<nav id="navbar">
                <a href="/">
                    <img src="/static/img/logo_boards.png" alt="Main Page" id="mainpage-img">
                </a>
                <a href="/profile/favorites/" class="links"><i class='bx bxs-heart' style="color: red"></i> Избранные</a>
                <a href="#" class="links"><i class='bx bxs-conversation'></i> Чат</a>
                <button type="button" class="btn btn-primary notification">
                    <i class='bx bx-bell'></i> <span class="badge text-bg-secondary"></span>
                </button>
                <button id="create_ad">
                    <a href="/create/ad/" target="_blank" rel="noopener noreferrer">Создать объявление</a>
                </button>
            </nav>`);
    $("body").prepend(nav);
    var tag = $("#create_ad");
    var id = $.cookie('user_id');
    console.log(id);
    if (id != undefined) {
        $.ajax({
            url: `/profile/api/v1/user/${id}/`,
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