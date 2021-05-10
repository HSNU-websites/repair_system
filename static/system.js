function send_remove(element) {
    var info = element.parentElement.id.split("_");
    var category = info[0];
    var id = parseInt(info[1]);
    $.ajax({
        url: "/system_modification",
        type: "delete",
        data: JSON.stringify({ 'category': category, 'id': id }),
        dataType: "json",
        success: function (data) {
            alert("data");
        },
        error: function (e) {
            alert("e");
        },
    })
}

function send_add(element) {
    var category = element.parentElement.id;
    // pending
}

function send_update(element) {
    var category = element.parentElement.id;
    var info = element.parentElement.children;
    var result = [];
    for (var i = 0; i< info.length;i++) {
        if (info[i].tagName == "DIV") {
            result.push({
                id: parseInt(info[i].id.split("_")[1]),
                description: info[i].children[0].value,
                sequence: parseInt(info[i].children[1].value)
            })
        }
    }
    $.ajax({
        url: "/system_modification",
        type: "delete",
        data: JSON.stringify(result),
        dataType: "json",
        success: function (data) {
            alert("data");
        },
        error: function (e) {
            alert("e");
        },
    })
}