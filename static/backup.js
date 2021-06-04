function doBackup() {
    $.ajax({
        url: "/backup_backend",
        type: "post",
        data: "",
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

function restoreTo(backup_name) {
    if (window.confirm("確認還原?")) {
        $.ajax({
            url: "/backup_backend",
            type: "update",
            data: JSON.stringify({"name": backup_name}),
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
}

function deleteBackup(backup_name) {
    $.ajax({
        url: "/backup_backend",
        type: "delete",
        data: JSON.stringify({"name": backup_name}),
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