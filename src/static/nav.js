window.onload = function () {
    var btn = document.getElementById("hamburger");
    btn.addEventListener("click", function(event){show_nav()});
}
function show_nav() {
    var children = document.getElementsByTagName("nav")[0].children;
    for (i = 1; i < children.length; i++) {
        if (children[i].style.visibility == "hidden") {
            children[i].style.visibility = "visible";
        }
        else {
            children[i].style.visibility = "hidden";
        }
    }
}