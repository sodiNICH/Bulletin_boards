$(document).ready(function () {
    $.ajax({
        url: "/chat/api/v1/list/",
        type: "GET",
        success: function (response) {
            console.log(response);
            if (response[0] !== null) {
                for (let i = 0; i < response.length; i++) {
                    console.log(response[i])
                    var chat = response[i];
                    var allChats = $("#all-chats");
                    var spanChat = $("<span>").attr("id", "block-chat");
                    var h1Advert = $("<h1>")
                    var aAdvert = $("<a>").attr("href", `/ad/${chat.advert.id}`).text(chat.advert.title);
                    var imgAdvert = $("<img>").attr("src", chat.advert.images).attr("id", "img-advert-chat");
                    h1Advert.append(aAdvert);
                    var aChat = $("<a>").attr("id", `chat-a-${chat.id}`).attr("href", `/chat/${chat.id}/`);
                    if (chat.messages !== null) {
                        var lastMessage = chat.messages.slice(-1)[0]
                        var lastMessageTag = $("<p>");
                        var a = $(`<a href="/profile/${lastMessage.id}/"><img src="${lastMessage.avatar}" id="avatar-chat"> ${lastMessage.username}</a>: <a href="/chat/${chat.id}/">${lastMessage.text}</a>`);
                        lastMessageTag.append(a);
                        aChat.append(lastMessageTag);
                    } else {
                        var messageNot = $("<p>").text("Сообщений нет");
                        aChat.append(messageNot);
                    };
                    spanChat.append(imgAdvert, h1Advert, aChat);
                    allChats.append(spanChat);
                };
            };
        },
        error: function (xhr) {
            console.error(xhr);
        },
    });
});