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

// Btn day/night mode

const dayNightBtn = document.getElementById("day-night");

if (dayNightBtn) {

    dayNightBtn.onclick = function () {
        this.classList.toggle("day-night-active")
    }

    const icon = dayNightBtn.querySelector("i");

    if (icon.classList.contains("night")) {
        dayNightBtn.classList.add("day-night-active")
    } else {
        dayNightBtn.classList.remove("day-night-active")
    }

}

// Widget Season

const season = document.getElementById("data_season");
const seasonWidget = document.getElementById("season");


if (season && seasonWidget) {
    const seasonIcon = seasonWidget.querySelector(".type");
    const seasonText = season.textContent.replace(/"/g, "");

    const seasonData = {
        printemps: {
            color: "#2ecc71",
            icon: '<i class="fa-solid fa-seedling fa-sm"></i>'
        },
        été: {
            color: "#1abc9c",
            icon: '<i class="fa-solid fa-umbrella-beach fa-sm"></i>'
        },
        automne: {
            color: "brown",
            icon: '<i class="fa-solid fa-leaf fa-sm"></i>'
        },
        default: {
            color: "#2c3e50",
            icon: '<i class="fa-solid fa-snowflake fa-sm"></i>'
        }
    }

    const chosenSeason = seasonData[seasonText] || seasonData.default
    seasonWidget.style.backgroundColor = chosenSeason.color
    seasonIcon.innerHTML = chosenSeason.icon
}
















