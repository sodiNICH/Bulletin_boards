function subscriptions (id) {
    let elem = document.getElementById(`user-${id}`);
    if (elem.classList.contains('bxs-user-minus')) {
        elem.classList.remove('bxs-user-minus');
        elem.classList.add('bxs-user-plus');
        elem.title = 'Отписаться';
        var method = "DELETE";
    } else {
        elem.classList.remove('bxs-user-plus');
        elem.classList.add('bxs-user-minus');
        elem.title = 'Подписаться';
        var method = "POST";
    }
    console.log(method);

    $.ajax({
        url: '/profile/user/subscriptions/api/',
        method: method,
        datatype: 'json',
        data: {
            'seller_id': id,
        },
        success: function (data) {
            console.log(data.message);
        },
        error: function (xhr, status, error) {
            alert('Something has gone wrong');
        },
    });
}