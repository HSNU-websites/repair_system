function send_remove(element) {
    var user_id = parseInt(element.parentElement.children[0].id);
    $.ajax({
        url: "/manage_user_backend",
        type: "delete",
        data: JSON.stringify({ 'user_id': user_id }),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                alert("OK");
                location.reload();
            }
            else {
                alert("Error");
            }
        })
}