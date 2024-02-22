$(document).ready(function () {
    $.ajax({
        url: "/profile/api/v1/favorites/",
        type: "GET",
        success: function (response) {
            import('/static/js/overview_advert.js')
                .then((module) => {
                    var getAdvert = module.getAdvert;

                    var ads = response;
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
    });
});