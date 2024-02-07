$(document).ready(function () {
    $.ajax({
        url: "/profile/user/favorites/api/",
        type: "GET",
        success: function (response) {
            var all_ads = $("#all-ads");
            for (let i = 0; i < response.length; i++) {
                var ad = response[i];
                var card = $('<div>').addClass('card').css('width', '18rem');
                var carousel = $('<div>').addClass('carousel slide').attr('id', `carouselExampleIndicators${ad.id}`);
                var indicators = $('<div>').addClass('carousel-indicators');
                var carousel_inner = $('<div>').addClass('carousel-inner');

                // Добавляем indicators и carousel-inner в carousel
                carousel.append(indicators);
                carousel.append(carousel_inner);

                // Добавляем carousel в card
                card.append(carousel);

                console.log(ad.images)
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

                // Создаем блок card-body для каждого объявления
                var cardBody = $('<div>').addClass('card-body');
                var headerTitle = $('<h5>').addClass('card-title');
                var linkAd = $('<a>').attr("href", `/ad/api/${ad.id}`).attr("class", "link-ad").text(ad.title);
                headerTitle.append(linkAd);
                cardBody.append(headerTitle);

                // Добавляем card-body в card
                card.append(cardBody);

                // Создаем блок list-group для каждого объявления
                var listGroup = $('<ul>').addClass('list-group list-group-flush');
                var listItemPrice = $("<li>").addClass("list-group-item price").text(`${ad.price} ₽`)
                var listItemCategory = $("<li>").addClass("list-group-item").text(`${ad.category} | ${ad.subcategory}`);
                var listItemCondition = $("<li>").addClass("list-group-item").text(`${ad.condition}`);

                var cardBody = $('<div>').addClass('card-body');
                console.log(ad);
                if (ad.in_fav) {
                    cardBody.append($(`<i class='bx bxs-heart favorites-button' id='fav-${ad.id}' onclick="favorites(${ad.id})"'></i>`))
                } else {
                    cardBody.append($(`<i class='bx bx-heart favorites-button' id='fav-${ad.id}' onclick="favorites(${ad.id})"'></i>`))
                }

                listGroup.append(listItemPrice, listItemCategory, listItemCondition);

                // Добавляем list-group в card
                card.append(listGroup, cardBody);

                // Добавляем card в all_ads
                all_ads.append(card);
            }
        },
    });
});