$(document).ready(function () {
    $.ajax({
        url: "/api/v1/advert/",
        type: "GET",
        success: function (response) {
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
    });
});
