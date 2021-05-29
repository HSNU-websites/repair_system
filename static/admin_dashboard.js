function send_remove(element, category, id) {
    $.ajax({
        url: "/admin_dashboard_backend",
        type: "delete",
        data: JSON.stringify({ "category": category, "id": id }),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                alert("OK");
                if (category == "revision") {
                    element.parentElement.remove();
                }
                if (category == "record") {
                    element.parentElement.parentElement.remove();
                }
            }
            else {
                alert("Error");
            }
        })
}

function show_reply_window(element, record_id) {
    var tbody = document.querySelector("body > div > table > tbody")
    for (i = 0; i < tbody.children.length; i++) {
        // return to original status
        tbody.children[i].removeAttribute("style");
    }
    // change color because the one is chosen to reply
    element.parentElement.parentElement.style.backgroundColor = "rgba(255, 255, 255, 0.5)";
    var reply_window = document.getElementById("reply_window");
    reply_window.children[2].children[0].id = record_id;
    reply_window.style.display = "block";
}

function hide_reply_window() {
    var reply_window = document.getElementById("reply_window");
    reply_window.style.display = "none";
    var tbody = document.querySelector("body > div > table > tbody")
    for (i = 0; i < tbody.children.length; i++) {
        tbody.children[i].removeAttribute("style");
    }
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
                window.location.reload()
            }
            else {
                alert("Error");
            }
        })
}
