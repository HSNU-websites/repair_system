function doBackup() {
    $.ajax({
        url: "/backup_backend",
        type: "post",
        data: "",
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                add_msg("OK. The update will be loaded after you refesh the page.", "success");
            }
            else {
                add_msg("Error.", "alert");
            }
        })
}

function restoreTo(backup_name) {
    if (window.confirm("確認還原?")) {
        $.ajax({
            url: "/backup_backend",
            type: "put",
            data: JSON.stringify({"name": backup_name}),
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
}

function deleteBackup(backup_name, element) {
    $.ajax({
        url: "/backup_backend",
        type: "delete",
        data: JSON.stringify({"name": backup_name}),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                add_msg("OK.", "success");
                element.parentElement.parentElement.remove();
            }
            else {
                add_msg("Error.", "alert");
            }
        })
}