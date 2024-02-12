$(document).ready(function () {
    console.log("Working");
    $.ajax({
        url: "/profile/user/subscriptions/api/",
        method: "GET",
        success: function (response) {
            console.log(response);
        },
        error: function (xhr) {
            console.log(xhr);
        },
    });
});