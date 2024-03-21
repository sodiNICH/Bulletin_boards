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
            if (messages !== null) {
                messages.forEach(function (message) {
                    var messageDiv = $("<div>").addClass("message").attr("id", `message-${message.id}`);
                    var avatarImg = $("<img>").addClass("avatar").attr("src", message.avatar).attr("alt", message.username);
                    var messageContentDiv = $("<div>").addClass("message-content");
                    var usernameDiv = $("<div>").addClass("username").text(message.username);
                    var textDiv = $("<div>").addClass("text").text(message.text);
                    var createdAtDiv = $("<div>").addClass("created-at").text(message.created_at);
                    console.log(message);
                    messageContentDiv.append(usernameDiv, textDiv, createdAtDiv);
                    if (message.images !== null) {
                        var divImages = $("<div>").attr("id", "images");
                        message.images.forEach(function (image) {
                            var imageTag = $("<img>").attr("src", image).attr("class", "image-message").attr("onclick", "fullImage(this)");
                            divImages.append(imageTag);
                        });
                        textDiv.after(divImages);
                    };
                    if ($.cookie('user_id') == message.user_id) {
                        var deleteButton = $("<button>").attr("id", "delete-button").text("Удалить").attr("onclick", `deleteMessage(${message.id})`);
                        // var editButton = $("<button>").attr("id", "edit-button").text("Редактировать").on("click", function () {
                        //     editMessage(message.id);
                        // });
                    };
                    messageDiv.append(avatarImg, messageContentDiv, deleteButton);
                    chatMessagesDiv.append(messageDiv);
                });
            };
        },
        error: function (xhr) {
            console.error(xhr);
        },
    });

    let urlNewNot = `ws://${window.location.host}/ws/chat/${id}/`;
    const messageSocket = new WebSocket(urlNewNot);

    $('#message-input').on('input', function () {
        if ($(this).val().trim() !== '') {
            var data = {
                "typing": true,
                "user_id": $.cookie('user_id'),
            };
            messageSocket.send(JSON.stringify(data));
        };
    });

    $('#message-input').on('blur', function () {
        // Проверяем, содержит ли поле ввода текст
        if ($(this).val().trim() !== '') {
            $("#pritypingnts").empty();
        }
    });

    messageSocket.onopen = function () {
        console.log("Соединение установлено");
    };

    messageSocket.onmessage = function (event) {
        var jsonData = JSON.parse(event.data)
        console.log(jsonData);
        if ("message" in jsonData) {
            $("#typing").find('#typing-compaion').remove();
            var message_data = jsonData.message;
            var chatMessagesDiv = $("#all-messages");

            var messageDiv = $("<div>").addClass("message").attr("id", `message-${message_data.id}`);;
            var avatarImg = $("<img>").addClass("avatar").attr("src", message_data.avatar).attr("alt", message_data.username);
            var messageContentDiv = $("<div>").addClass("message-content");
            var usernameDiv = $("<div>").addClass("username").text(message_data.username);
            var textDiv = $("<div>").addClass("text").text(message_data.text);
            var createdAtDiv = $("<div>").addClass("created-at").text(message_data.created_at);
            messageContentDiv.append(usernameDiv, textDiv, createdAtDiv);
            if (message_data.images !== null) {
                var divImages = $("<div>").attr("id", "images");
                message_data.images.forEach(function (image) {
                    var imageTag = $("<img>").attr("src", image).attr("class", "image-message");
                    divImages.append(imageTag);
                });
                textDiv.after(divImages);
            };
            if ($.cookie('user_id') == message_data.user_id) {
                var deleteButton = $("<button>").attr("id", "delete-button").text("Удалить").attr("onclick", `deleteMessage(${message_data.id})`);
            };
            messageDiv.append(avatarImg, messageContentDiv, deleteButton);
            chatMessagesDiv.append(messageDiv);
            console.log(message_data);
        } else if ("typing" in jsonData) {
            console.log(jsonData.user_id, $.cookie('user_id'));
            if (jsonData.user_id !== $.cookie('user_id')) {
                var printTag = $("<h3>").attr("id", "typing-compaion").text("Печатает");
                if ($('#typing').children().length === 0) {
                    $("#typing").append(printTag);
                    setTimeout(function () {
                        $("#typing").find('#typing-compaion').remove();
                    }, 1200);
                };
            } else {
                $("#pritypingnts").empty();
            };
        } else if ("delete_message" in jsonData) {
            console.log(jsonData);
            $(`#message-${jsonData.delete_message.id}`).remove();
        };
    };

    $("#message-form").submit(function (event) {
        event.preventDefault();
        var formData = new FormData();  // Создаем объект FormData
        var messageInput = $("#message-input").val();
        var imagesInput = $("#images-message")[0].files;
        formData.append("text", messageInput);  // Добавляем данные в FormData
        for (var i = 0; i < imagesInput.length; i++) {
            formData.append("images", imagesInput[i]);
        }
        formData.append("chat", id);  // Добавляем данные в FormData
        formData.append("owner", $.cookie('user_id'));  // Добавляем данные в FormData

        $.ajax({
            url: "/chat/message/api/v1/",
            type: "POST",
            data: formData,  // Используем объект FormData
            processData: false,  // Не обрабатываем данные
            contentType: false,  // Устанавливаем автоматический тип контента
            success: function (response) {
                console.log(response);
                $("#message-input").val("");
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            },
        });
    });

    $("#image").click(function () {
        $("#fullscreen-container").fadeIn();
    });

    // Закрытие изображения при нажатии на кнопку "Закрыть"
    $("#close-button").click(function () {
        $("#fullscreen-container").fadeOut();
    });
});