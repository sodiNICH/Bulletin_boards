var url = location.href;
var subcategory = url.match(/subcategory\/(.+)/)[1];

$(document).ready(function () {
    $.ajax({
        url: `/api/v1/subcategory/${subcategory}`,
        type: "GET",
        success: function (response) {
            console.log(response);
            $("title").text(subcategory.slice(0, -1));
            import('/static/js/overview_advert.js')
                .then((module) => {
                    var getAdvert = module.getAdvert;
                    var allAdsTag = $("#all-ads");
                    for (let i = 0; i < response.length; i++) {
                        var adData = response[i];
                        var userData = adData.owner;
                        getAdvert(adData, userData, allAdsTag);
                    }
                })
                .catch((error) => {
                    console.error('Failed to load login module:', error);
                });
        },
        error: function (xhr) {
            console.error(xhr);
        },
    });
});