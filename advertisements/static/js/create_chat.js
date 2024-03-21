var userId = $.cookie("user_id");

function createChat(adId, companion) {
    data = JSON.stringify({
        "advertisement": adId,
        "companions": [userId, companion],
    });

    $.ajax({
        url: "/chat/api/v1/",
        method: "POST",
        data: data,
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
            var chatURL = `/chat/${response.id}/`;
            window.location.href = chatURL;
        },
        error: function (xhr, status, error) {
            if (status == 400) {
                window.location.href = chatURL;
            };
            console.error(xhr.responseText);
        },
    });
};
