// Burger menu

const menu = document.getElementById("menu");
const openBtn = document.getElementById("burger-menu-open");
const closeBtn = document.getElementById("burger-menu-close");

openBtn.onclick = function () {
    menu.classList.add("active");
}

closeBtn.onclick = function () {
    menu.classList.remove("active");
}

// Btn day/night

const dayNightBtn = document.getElementById("day-night");

dayNightBtn.onclick = function () {

    // Get content of btn
    let content = dayNightBtn.firstElementChild

    if(!dayNightBtn.classList.contains("day-night-active")) {
        dayNightBtn.classList.add("day-night-active")
        content.textContent = "Nuit"
    } else {
        dayNightBtn.classList.remove("day-night-active")
        content.textContent = "Jour"
    }

}







