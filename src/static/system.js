function send_remove(element) {
    var info = element.parentElement.id.split("_");
    var category = info[0];
    var id = parseInt(info[1]);
    $.ajax({
        url: "/system_backend",
        type: "delete",
        data: JSON.stringify({ "category": category, "id": id }),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                add_msg("OK.", "success");
                element.parentElement.remove();
            }
            else {
                add_msg("Error.", "alert");
            }
        })
}

function send_add(element) {
    var category = element.parentElement.id;
    var input_list = element.parentElement.getElementsByTagName("INPUT")
    var value = input_list[input_list.length - 1].value;
    // check whether empty
    if (value == "") {
        add_msg("Empty value is invalid.", "alert");
        return;
    }

    if (category == "items") {
        var office = element.parentElement.getElementsByTagName("select");
        office = office[office.length - 1]
        var data = JSON.stringify({ "category": category, "value": value, "office": parseInt(office[office.selectedIndex].value) });
    }
    else {
        var data = JSON.stringify({ "category": category, "value": value });
    }
    console.log(data)
    $.ajax({
        url: "/system_backend",
        type: "post",
        data: data,
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                send_add_message("OK.", "success");
                window.location.reload();
            }
            else {
                add_msg("Error.", "alert");
            }
        })
}

function send_update(element) {
    var category = element.parentElement.id;
    var info = element.parentElement.children;
    var result = [{ "category": category }];
    for (var i = 0; i < info.length; i++) {
        if (info[i].tagName == "DIV") {
            var description = info[i].children[1].value;
            // check whether empty
            if (!description) {
                add_msg("Empty value is invalid.", "alert");
                return;
            }
            var data = {
                id: parseInt(info[i].id.split("_")[1]),
                description: description,
                sequence: i
            }
            if (category == "items") {
                var office = info[i].children[2];
                var office_id = office[office.selectedIndex].value;
                data.office_id = parseInt(office_id);
            }
            result.push(data)
        }
    }
    $.ajax({
        url: "/system_backend",
        type: "patch",
        data: JSON.stringify(result),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                add_msg("OK.", "success");
            }
            else {
                add_msg("Error.", "alert");
            }
        })
}

// drag effect
$(function () {
    $(".container div").sortable({
        items: "div",
        cursor: "move",
        opacity: 0.6,
        containment: "parent",
    });
});
