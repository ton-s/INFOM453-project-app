// Burger menu

var menu = document.getElementById("menu");
var openBtn = document.getElementById("burger-menu-open");
var closeBtn = document.getElementById("burger-menu-close");

openBtn.onclick = openNav;
closeBtn.onclick = closeNav;

function openNav() {
  menu.classList.add("active");
}

function closeNav() {
  menu.classList.remove("active");
}

