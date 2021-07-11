function hide(obj) {
    obj.style.opacity = "0";
    setTimeout(() => {
        obj.style.display = "none";
    }, 300);
}

function add_msg(msg, category) {
    var container = document.getElementById("messages");
    var message = document.createElement("div");
    var closebtn = document.createElement("span");
    closebtn.innerText = "×";
    closebtn.classList.add("closebtn");
    message.appendChild(closebtn);
    var content = document.createElement("span");
    content.innerText = msg;
    message.appendChild(content);
    message.classList.add("flash-message");
    message.classList.add(category);
    container.appendChild(message);
    closebtn.addEventListener("click", function (event) { hide(closebtn.parentElement) })
}