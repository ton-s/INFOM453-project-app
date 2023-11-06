window.onload = function () {
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

    if (dayNightBtn) {
        dayNightBtn.onclick = function () {

            const content = dayNightBtn.querySelector("i");

            if (!dayNightBtn.classList.toggle("day-night-active")) {
                content.outerHTML = "<i class=\"fa-solid fa-sun fa-xl\"></i>";
            } else {
                content.outerHTML = "<i class=\"fa-regular fa-moon fa-xl\"></i>";
            }

        }
    }
}










