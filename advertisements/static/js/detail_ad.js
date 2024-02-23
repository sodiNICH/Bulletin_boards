var url = location.href;
var match = url.match(/\/ad\/(\d+)\/$/);
var id = match[1];
console.log(id);

$(document).ready(function () {
    $.ajax({
        url: `/api/v1/advert/${id}/`,
        type: "GET",
        success: function (ad) {
            console.log(ad);
            $("title").text(ad.title);
            var adImg = $("#ad-img");

            $("#title-ad").text(ad.title);
            $("#created-at").text(ad.created_at);

            if (ad.in_fav != undefined) {
                if (ad.in_fav) {
                    $("#created-at").after($(`<i class='bx bxs-heart favorites-button' id='fav-${ad.id}' onclick="favorites(${ad.id})"></i>`))
                } else {
                    $("#created-at").after($(`<i class='bx bx-heart favorites-button' id='fav-${ad.id}' onclick="favorites(${ad.id})"></i>`))
                }
            };

            var card = $('<div>').addClass('card').css('width', '18rem');
            var carousel = $('<div>').addClass('carousel slide').attr('id', `carouselExampleIndicators${ad.id}`);
            var indicators = $('<div>').addClass('carousel-indicators');
            var carousel_inner = $('<div>').addClass('carousel-inner');

            // Добавляем indicators и carousel-inner в carousel
            carousel.append(indicators);
            carousel.append(carousel_inner);

            // Добавляем carousel в card
            card.append(carousel);

            // Добавляем изображения в carousel-inner
            let img = ad.images.slice(0, 5);
            for (let j = 0; j < img.length; j++) {
                var button = $('<button>').attr({
                    'type': 'button',
                    'data-bs-target': `#carouselExampleIndicators${ad.id}`,
                    'data-bs-slide-to': j,
                    'aria-label': 'Slide ' + (j + 1)
                });
                let carousel_item = $('<div>').addClass('carousel-item');
                let img_tag = $('<img>').addClass('d-block w-100').attr('src', img[j]).attr('alt', ad.title);
                if (j === 0) {
                    button.addClass('active').attr('aria-current', 'true');
                    carousel_item.addClass('active')
                }

                // Создаем блок carousel-item для каждого изображения
                carousel_item.append(img_tag);
                carousel_inner.append(carousel_item);
                indicators.append(button);
            }

            // Добавляем кнопки управления в carousel
            var prevButton = $('<button>').addClass('carousel-control-prev').attr({
                'type': 'button',
                'data-bs-target': `#carouselExampleIndicators${ad.id}`,
                'data-bs-slide': 'prev'
            });
            prevButton.append($('<span>').addClass('carousel-control-prev-icon').attr('aria-hidden', 'true'));
            prevButton.append($('<span>').addClass('visually-hidden').text('Previous'));

            var nextButton = $('<button>').addClass('carousel-control-next').attr({
                'type': 'button',
                'data-bs-target': `#carouselExampleIndicators${ad.id}`,
                'data-bs-slide': 'next'
            });
            nextButton.append($('<span>').addClass('carousel-control-next-icon').attr('aria-hidden', 'true'));
            nextButton.append($('<span>').addClass('visually-hidden').text('Next'));

            carousel.append(prevButton);
            carousel.append(nextButton);

            adImg.append(card);

            $("#price-ad").text(`${ad.price} ₽`);
            $("#text-desc").text(ad.description);

            var ownerInfo = $("#owner-info");
            ownerInfo.append($("<img>").attr("src", ad.owner.avatar).attr("id", "owner-avatar"));
            var header = $("<h2>");
            header.append($("<a>").text(ad.owner.username).attr("id", "owner-username").attr("href", `/profile/${ad.owner.id}`).attr("target", "_blank"));
            ownerInfo.append(header);
            var sendMessage = $("<button>").attr("id", "send-message").addClass("btn btn-primary").text("Написать сообщение");
            ownerInfo.append(sendMessage);

            import('/static/js/overview_advert.js')
                .then((module) => {
                    var getAdvert = module.getAdvert;
                    var similarAdsTag = $("#similar-ads");
                    var similarAds = ad.similar_ads;
                    for (let i = 0; i < similarAds.length; i++) {
                        var adData = similarAds[i];
                        var userData = adData.owner;
                        getAdvert(adData, userData, similarAdsTag);
                    }
                })
                .catch((error) => {
                    console.error('Failed to load login module:', error);
                });
        },
        error: function (xhr) {
            console.log(xhr);
        },
    });
});