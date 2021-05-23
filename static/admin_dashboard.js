function send_remove(category, id) {
    $.ajax({
        url: "/admin_dashboard_backend",
        type: "delete",
        data: JSON.stringify({ "category": category, "id": id }),
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

function show_reply_window(record_id) {
    var reply_window = document.getElementById("reply_window");
    reply_window.children[2].children[0].id = record_id;
    reply_window.style.visibility = "visible";
}

function send_reply_record(element) {
    var parent = element.parentElement.parentElement;
    // record_id
    var record_id = element.id
    // status
    var status = parent.children[0].children[1];
    var status_id = parseInt(status.options[status.selectedIndex].value);
    // description
    var description = parent.children[1].children[2].value;
    $.ajax({
        url: "/admin_dashboard_backend",
        type: "post",
        data: JSON.stringify({ "record_id": record_id, "status_id": status_id, "description": description }),
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
