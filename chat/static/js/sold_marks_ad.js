function soldMarkAd (idAd) {
    $.ajax({
        url: `/api/v1/sales-mark/`,
        type: "POST",
        data: {
            "id": idAd,
        },
        success: function (response) {
            console.log("Объявление продано");
        },
    });
};