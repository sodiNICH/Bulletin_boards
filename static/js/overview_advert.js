export function getAdvert(ad_data, user_data, tag) {
    var card = $('<div>').addClass(`card ad-${ad_data.id}`).css('width', '18rem');
    var carousel = $('<div>').addClass('carousel slide').attr('id', `carouselExampleIndicators${ad_data.id}`);
    var indicators = $('<div>').addClass('carousel-indicators');
    var carousel_inner = $('<div>').addClass('carousel-inner');

    // Добавляем indicators и carousel-inner в carousel
    carousel.append(indicators);
    carousel.append(carousel_inner);

    // Добавляем carousel в card
    card.append(carousel);

    // Добавляем изображения в carousel-inner
    let img = ad_data.images.slice(0, 5);
    for (let j = 0; j < img.length; j++) {
        var button = $('<button>').attr({
            'type': 'button',
            'data-bs-target': `#carouselExampleIndicators${ad_data.id}`,
            'data-bs-slide-to': j,
            'aria-label': 'Slide ' + (j + 1)
        });
        let carousel_item = $('<div>').addClass('carousel-item');
        let img_tag = $('<img>').addClass('d-block w-100').attr('src', img[j]).attr('alt', ad_data.title);
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
        'data-bs-target': `#carouselExampleIndicators${ad_data.id}`,
        'data-bs-slide': 'prev'
    });
    prevButton.append($('<span>').addClass('carousel-control-prev-icon').attr('aria-hidden', 'true'));
    prevButton.append($('<span>').addClass('visually-hidden').text('Previous'));

    var nextButton = $('<button>').addClass('carousel-control-next').attr({
        'type': 'button',
        'data-bs-target': `#carouselExampleIndicators${ad_data.id}`,
        'data-bs-slide': 'next'
    });
    nextButton.append($('<span>').addClass('carousel-control-next-icon').attr('aria-hidden', 'true'));
    nextButton.append($('<span>').addClass('visually-hidden').text('Next'));

    carousel.append(prevButton);
    carousel.append(nextButton);

    // Создаем блок card-body для каждого объявления
    var cardBody = $('<div>').addClass('card-body');
    var headerTitle = $('<h5>').addClass('card-title');
    var linkAd = $('<a>').attr("href", ad_data.url).attr("class", "link-ad").text(ad_data.title);
    headerTitle.append(linkAd);
    cardBody.append(headerTitle);

    // Добавляем card-body в card
    card.append(cardBody);

    // Создаем блок list-group для каждого объявления
    var listGroup = $('<ul>').addClass('list-group list-group-flush');
    var listItemTime = $("<li>").addClass("list-group-item time").text(`${ad_data.created_at}`);
    var listItemPrice = $("<li>").addClass("list-group-item price").text(`${ad_data.price} ₽`);
    var itemCategory = $(`<a href='/category/${ad_data.category}/'>${ad_data.category_display}</a>`).prop('outerHTML');
    var itemSubcategory = $(`<a href='/subcategory/${ad_data.subcategory}/'>${ad_data.subcategory_display}</a>`).prop('outerHTML');
    var listItemCategory = $("<li>").addClass("list-group-item").html(`${itemCategory} | ${itemSubcategory}`);

    var listItemCondition = $("<li>").addClass("list-group-item").text(`Состояние: ${ad_data.condition}`);

    var cardBody = $('<div>').addClass('card-body');
    cardBody.append($('<a>').addClass('card-link').attr("href", `/profile/${user_data.id}/`).text(user_data.username));

    if (ad_data.in_fav) {
        headerTitle.append($(`<i class='bx bxs-heart favorites-button' id='fav-${ad_data.id}' onclick="favorites(${ad_data.id})"'></i>`))
    } else {
        headerTitle.append($(`<i class='bx bx-heart favorites-button' id='fav-${ad_data.id}' onclick="favorites(${ad_data.id})"'></i>`))
    }
    listGroup.append(listItemTime, listItemPrice, listItemCategory, listItemCondition);

    var cookie = $.cookie("user_id");

    // Добавляем list-group в card
    card.append(listGroup, cardBody);

    console.log(user_data);
    if (user_data.id == cookie) {
        var panelButtons = $("<div>").attr("id", "panel-buttons");
        var editAdButtons = $("<button>").attr("id", `edit-ad-buttons`).attr("class", "btn btn-outline-info").text("Редактировать");
        var deleteAdButtons = $("<button>").attr("id", "delete-ad-buttons").attr("class", "btn btn-outline-danger").attr("onclick", `deleteAd(${ad_data.id})`).text("Удалить");
        panelButtons.append(editAdButtons, deleteAdButtons);
        card.append(panelButtons);
    };

    // Добавляем card в all_ads
    tag.append(card);
};