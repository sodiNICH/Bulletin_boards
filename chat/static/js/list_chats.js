$(document).ready(function () {
    function getChat(chat_data) {
        var allChats = $("#all-chats");
        var spanChat = $("<span>").attr("class", "block-chat").attr("id", `chat-${chat_data.id}`);
        var h1Advert = $("<h1>");
        var aAdvert = $("<a>").attr("href", `/ad/${chat_data.advert.id}`).text(chat_data.advert.title);
        var imgAdvert = $("<img>").attr("src", chat_data.advert.images).attr("id", "img-advert-chat");
        h1Advert.append(aAdvert);
        var aChat = $("<a>").attr("id", `chat-a-${chat_data.id}`).attr("href", `/chat/${chat_data.id}/`);
        var deleteChat = $("<button>").text("Удалить чат").attr("id", "delete-chat-buttons").attr("onclick", `deleteChat(${chat_data.id})`);
        if (chat_data.messages !== null) {
            var lastMessage = chat_data.messages.slice(-1)[0]
            var lastMessageTag = $("<p>");
            var a = $(`<a href="/profile/${lastMessage.user_id}/"><img src="${lastMessage.avatar}" id="avatar-chat"> ${lastMessage.username}</a>: <a href="/chat/${chat_data.id}/">${lastMessage.text}</a>`);
            lastMessageTag.append(a);
            aChat.append(lastMessageTag);
        } else {
            var messageNot = $("<p>").text("Сообщений нет");
            aChat.append(messageNot);
        };
        spanChat.append(imgAdvert, h1Advert, aChat, deleteChat);
        allChats.append(spanChat);
    };

    $.ajax({
        url: "/chat/api/v1/",
        type: "GET",
        success: function (response) {
            console.log(response);
            response = response.filter(function (element) {
                return element !== null;
            });
            for (let i = 0; i < response.length; i++) {
                console.log(response[i])
                getChat(response[i]);
            };
        },
        error: function (xhr) {
            console.error(xhr);
        },
    });

    let urlListChats = `ws://${window.location.host}/ws/chat/list/`;
    const listChatsWebSocket = new WebSocket(urlListChats);

    listChatsWebSocket.onopen = function () {
        console.log("Успешное подключение")
    };

    listChatsWebSocket.onmessage = function (event) {
        var data_json = JSON.parse(event.data);
        console.log(data_json);
        getChat(data_json);
    }
});