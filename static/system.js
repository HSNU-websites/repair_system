function send_remove(element) {
    var info = element.parentElement.id.split("_");
    var category = info[0];
    var id = parseInt(info[1]);
    $.ajax({
        url: "/system_modification",
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

function send_add(element) {
    var category = element.parentElement.id;
    var input_list = element.parentElement.getElementsByTagName("INPUT")
    var value = input_list[input_list.length - 1].value;
    var office = element.parentElement.getElementsByTagName("select");
    // check whether empty
    if (value == "" || office == "") {
        alert("Empty value is invalid.");
        return;
    }

    if (office.length != 0) {
        var data = JSON.stringify({ "category": category, "value": value, "office": parseInt(office[0].value) });
    }
    else {
        var data = JSON.stringify({ "category": category, "value": value });
    }
    console.log(data)
    $.ajax({
        url: "/system_modification",
        type: "post",
        data: data,
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

function send_update(element) {
    var category = element.parentElement.id;
    var info = element.parentElement.children;
    var result = [{ "category": category }];
    for (var i = 0; i < info.length; i++) {
        if (info[i].tagName == "DIV") {
            var description = info[i].children[0].value;
            var sequence = parseInt(info[i].children[1].value);
            // check whether empty
            if (description == "") {
                alert("Empty value is invalid.");
                return;
            }
            result.push({
                id: parseInt(info[i].id.split("_")[1]),
                description: description,
                sequence: i
            })
        }
    }
    $.ajax({
        url: "/system_modification",
        type: "update",
        data: JSON.stringify(result),
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

// drag effect
$(function() {
    $( ".container div" ).sortable({
        items: "div",
        cursor: "move",
        opacity: 0.6,
        containment: "parent",   
    });
});