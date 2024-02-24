var url = location.href;
var match = url.match(/\/chat\/(\d+)\/$/);
var id = match[1];
console.log(id);

$(document).ready(function () {
    $.ajax({
        url: `/chat/api/v1/${id}/`,
        type: "GET",
        success: function (response) {
            console.log(response);
            var messages = response.messages
            var chatMessagesDiv = $("#all-messages");

            // Перебираем сообщения и добавляем их в чат
            messages.forEach(function (message) {
                var messageHtml = `
            <div class="message">
                <img class="avatar" src="${message.avatar}" alt="${message.username}">
                <div class="message-content">
                    <div class="username">${message.username}</div>
                    <div class="text">${message.text}</div>
                    <div class="created-at">${message.created_at}</div>
                </div>
            </div>
        `;

                chatMessagesDiv.append(messageHtml);
            });
        },
        error: function (xhr) {
            console.error(xhr);
        },
    });

    let urlNewNot = `ws://${window.location.host}/ws/chat/${id}/`;
    const notificationSocket = new WebSocket(urlNewNot);
    notificationSocket.onopen = function () {
        console.log("Соединение установлено");
    }
    notificationSocket.onmessage = function (event) {
        var message_data = JSON.parse(event.data);
        var chatMessagesDiv = $("#all-messages");

        var messageHtml = `
            <div class="message">
                <img class="avatar" src="${message_data.avatar}" alt="${message_data.username}">
                <div class="message-content">
                    <div class="username">${message_data.username}</div>
                    <div class="text">${message_data.text}</div>
                    <div class="created-at">${message_data.created_at}</div>
                </div>
            </div>
        `;
        chatMessagesDiv.append(messageHtml);
        console.log(message_data);
    };

    $("#message-form").submit(function (event) {
        event.preventDefault();
        var formData = new FormData();  // Создаем объект FormData

        var messageInput = $("#message-input").val();
        formData.append("text", messageInput);  // Добавляем данные в FormData
        formData.append("chat", id);  // Добавляем данные в FormData
        formData.append("owner", $.cookie('user_id'));  // Добавляем данные в FormData

        $.ajax({
            url: "/chat/api/v1/message/create/",
            type: "POST",
            data: formData,  // Используем объект FormData
            processData: false,  // Не обрабатываем данные
            contentType: false,  // Устанавливаем автоматический тип контента
            success: function (response) {
                console.log(response);
            },
            error: function (xhr) {
                console.error(xhr);
            },
        });
    });
});