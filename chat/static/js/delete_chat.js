function deleteChat (idChat) {
    $.ajax({
        url: `/chat/api/v1/${idChat}/`,
        type: "DELETE",
        success: function (response) {
            console.log(`Чат ${idChat} удален`);
            $(`#chat-${idChat}`).remove();
        },
    });
};