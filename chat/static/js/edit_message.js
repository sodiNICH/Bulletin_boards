function editChat (idChat) {
    $.ajax({
        url: `/chat/api/v1/${idChat}/`,
        type: "PATCH",
        success: function (response) {
            console.log(`Чат ${idChat} удален`);
            $(`#chat-${idChat}`).remove();
        },
    });
};