function logout () {
    $.ajax({
        url: `/profile/api/v1/logout/`,
        method: 'DELETE',
        success: function (data) {
            console.log('Выход выполнен');
            location.href = "/profile/login/";
        },
        error: function (error) {
            alert('Что то не так');
        }
    });
};