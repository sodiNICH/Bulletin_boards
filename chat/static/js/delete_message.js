function deleteMessage (idMessage) {
    $.ajax({
        url: `/chat/message/api/v1/${idMessage}/`,
        type: "DELETE",
        success: function (response) {
            console.log(`Сообщение ${idMessage} удалено`);
            $(`#message-${idMessage}`).remove();
        },
    });
};