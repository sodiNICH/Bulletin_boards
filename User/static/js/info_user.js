var url = location.href;
var match = url.match(/\/profile\/(\d+)\/$/);
var id = match[1];
console.log(id);

$(document).ready(function () {
    $.ajax({
        url: `/profile/api/v1/user/${id}`,
        type: "GET",
        success: function (response) {
            $('title').text(response.username);
            var newHTML = `<h1 id="username">${response.username}</h1>` +
                `<p id="description">${response.description}</p>`;

            $('#info-user').prepend(newHTML);

            if ("in_subs" in response) {
                var tagSubs = `<i class='bx bxs-user-plus button-subs' title="Подписаться" id='user-${response.id}' onclick='subscriptions(${response.id})'></i>`;
                var tagUnsubs = `<i class='bx bxs-user-minus button-subs' title="Отписаться" id='user-${response.id}' onclick='subscriptions(${response.id})'></i>`;
                if (response.in_subs) {
                    $('#info-user').prepend(tagUnsubs);
                } else {
                    $('#info-user').prepend(tagSubs);
                };
            };

            if (response.avatar.length > 1) {
                $("#info-user").prepend(`<img src="${response.avatar}" alt="${response.username}" id="user-avatar">`);
            } else {
                $("#info-user").prepend("<div class='empty-avatar'>👤</div>");
            };
            console.log(response);

            import('/static/js/overview_advert.js')
                .then((module) => {
                    var getAdvert = module.getAdvert;

                    var ads = response.ads;
                    var allAdsTag = $("#all-ads");
                    for (let i = 0; i < ads.length; i++) {
                        var adData = ads[i];
                        var userData = adData.owner;
                        getAdvert(adData, userData, allAdsTag);
                    }
                })
                .catch((error) => {
                    console.error('Failed to load login module:', error);
                });
        },
        error: function (error) {
            alert('Что то не так');
        },
    });
});