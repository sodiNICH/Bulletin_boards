var PRODUCT_CATEGORIES = {
    "personal_effects": "Личные вещи",
    "electronics": "Электроника",
    "hobbies_and_recreation": "Хобби и отдых",
    "for_home_and_cottage": "Для дома и дачи"
};
var PRODUCT_SUBCATEGORIES = {
    "personal_effects": {
        "clothes_shoes_accessories": "Одежда, обувь, аксессуары",
        "watches_and_jewelry": "Часы и украшения",
        "beauty_and_health": "Красота и здоровье",
    },
    "for_home_and_cottage": {
        "household_appliances": "Бытовая техника",
        "furniture_and_interior": "Мебель и интерьер",
        "cookware_and_kitchenware": "Посуда и товары для кухни",
        "foodstuffs": "Продукты питания",
    },
    "electronics": {
        "audio_and_video": "Аудио и видео",
        "games_consoles_programs": "Игры, приставки и программы",
        "PC": "ПК",
        "laptops": "Ноутбуки",
        "tablets_and_e-books": "Планшеты и электронные книги",
        "Phones": "Телефоны",
        "PC_Products": "Товары для ПК",
        "photographic_equipment": "Фототехника",
    },
    "hobbies_and_recreation": {
        "bicycles": "Велосипеды",
        "books_and_magazines": "Книги и журналы",
        "collecting": "Коллекционирование",
        "musical_instruments": "Музыкальные инструменты",
        "sports_and_recreation": "Спорт и отдых",
    },
};
$(document).ready(function () {
    var $categories = $('#categories-form');
    var $subcategories = $('#subcategories');

    $.each(PRODUCT_CATEGORIES, function (key, value) {
        $categories.append('<option value="' + key + '">' + value + '</option>');
    });

    $('#title').on('input', function () {
        var inputText = $(this).val();
        var charCount = inputText.length;
        var remainingChars = 50 - charCount;

        if (remainingChars >= 0) {
            $('#counter-title').html('Символов: <span id="charCount">' + charCount + '</span>/50');
        } else {
            var limitedText = inputText.slice(0, 50);
            $(this).val(limitedText);
            $('#counter-title').html('Символов: <span id="charCount">50</span>/50');
        }
    });

    $('#description').on('input', function () {
        var inputText = $(this).val();
        var charCount = inputText.length;
        var remainingChars = 1000 - charCount;

        if (remainingChars >= 0) {
            $('#counter-desc').html('Символов: <span id="charCount">' + charCount + '</span>/1000');
        } else {
            var limitedText = inputText.slice(0, 1000);
            $(this).val(limitedText);
            $('#counter-desc').html('Символов: <span id="charCount">1000</span>/1000');
        }
    });

    $categories.change(function () {
        var selectedCategory = $(this).val();
        $subcategories.empty();
        if (selectedCategory in PRODUCT_SUBCATEGORIES) {
            $.each(PRODUCT_SUBCATEGORIES[selectedCategory], function (subkey, subvalue) {
                $subcategories.append('<option value="' + subkey + '">' + subvalue + '</option>');
            });
            $('#subcategoryField').show();
        } else {
            $('#subcategoryField').hide();
        }
    });
});