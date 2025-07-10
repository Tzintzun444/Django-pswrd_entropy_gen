document.getElementById("userButton").addEventListener("click", function() {
    let menu = document.getElementById("menuDropdown");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
});

document.addEventListener("click", function(event) {
    let menu = document.getElementById("menuDropdown");
    let button = document.getElementById("userButton");

    if (!menu.contains(event.target) && !button.contains(event.target)) {
        menu.style.display = "none";
    }
});