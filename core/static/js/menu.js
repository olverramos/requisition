
/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    sessionStorage.setItem("show_menu", "1");
}
  
  /* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    sessionStorage.setItem("show_menu", "0");
}

document.addEventListener("DOMContentLoaded", function () {
  let links = document.querySelectorAll(".sidenav a");
  links.forEach(function (link) {
      link.addEventListener("click", function () {
          closeNav(); // Cierra el menú después de hacer clic
      });
  });
});

// ✅ Cierra el menú si el usuario toca fuera del sidebar
document.addEventListener("click", function (event) {
  let sidenav = document.getElementById("mySidenav");
  let menuButton = document.querySelector(".menu-title"); // Botón ☰ Menú
  if (sidenav.style.width === "250px" && !sidenav.contains(event.target) && !menuButton.contains(event.target)) {
      closeNav();
  }
});
