function favorites (id) {
    let elem = document.getElementById(`fav-${id}`);
    console.log(12);
    if (elem.classList.contains('bx-heart')) {
        elem.classList.remove('bx-heart');
        elem.classList.add('bxs-heart');
        elem.title = 'Удалить из избранного';
        var method = "POST";
    } else {
        elem.classList.remove('bxs-heart');
        elem.classList.add('bx-heart');
        elem.title = 'Добавить в избранное';
        var method = "DELETE";
    }
    console.log(method);

    $.ajax({
        url: '/profile/user/favorites/api/',
        method: method,
        datatype: 'json',
        data: {
            'ad': id,
        },
        success: function (data) {
            console.log(data.message);
        },
        error: function (xhr, status, error) {
            alert('Something has gone wrong');
        },
    });
}