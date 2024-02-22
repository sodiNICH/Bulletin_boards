$(document).ready(function () {
    console.log("Working");
    $.ajax({
        url: "/profile/api/v1/subscriptions/",
        method: "GET",
        success: function (response) {
            console.log(response);
        },
        error: function (xhr) {
            console.log(xhr);
        },
    });
});