function deleteAd (id) {
    let elem = $(`.card.ad-${id}`);
    elem.remove();

    $.ajax({
        url: `/api/v1/advert/${id}/`,
        method: "DELETE",
        success: function (data) {
            console.log(`Ads with id ${id} deleted`);
        },
        error: function (xhr, status, error) {
            alert('Something has gone wrong');
        },
    });
}