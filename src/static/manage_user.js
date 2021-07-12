function send_remove(element) {
    var user_id = parseInt(element.parentElement.children[0].id);
    $.ajax({
        url: "/manage_user_backend",
        type: "delete",
        data: JSON.stringify({ "type": "single", "user_id": user_id }),
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

function send_update(element) {
    var parent = element.parentElement;
    var user_id = parseInt(parent.children[0].id);
    var name = parent.children[1].value;
    var classnum = parseInt(parent.children[2].value);
    var password = parent.children[3].value;
    var email = parent.children[4].value;
    var is_admin = parent.children[5].checked;
    var is_valid = parent.children[6].checked;
    var data = { "id": user_id, "name": name, "classnum": classnum, "email": email, "is_admin": is_admin, "is_valid": is_valid }
    // validate password
    if (password != "") {
        if (password.length < 6) {
            add_msg("Password is too short (at least 6 characters).", "alert");
            return;
        }
        else {
            data.password = password;
        }
    }
    // validate email
    if (is_admin & email == "") {
        add_msg("Email is required for admin.", "alert");
        return;
    }
    $.ajax({
        url: "/manage_user_backend",
        type: "patch",
        data: JSON.stringify(data),
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

function del_all_users() {
    var cookies = document.cookie.split(';').map(function (c) {
        return c.trim().split('=').map(decodeURIComponent);
    }).reduce(function (a, b) {
        try {
            a[b[0]] = JSON.parse(b[1]);
        } catch (e) {
            a[b[0]] = b[1];
        }
        return a;
    }, {});
    var upper = cookies["upper"];
    var lower = cookies["lower"];
    if (!(upper & lower)) {
        add_msg("The range does not be provided.", "alert");
        return;
    }
    if (window.confirm("確認刪除全部使用者?")) {
        $.ajax({
            url: "/manage_user_backend",
            type: "delete",
            data: JSON.stringify({ "type": "group", "upper": upper, "lower": lower }),
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
}