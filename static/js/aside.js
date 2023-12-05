document.addEventListener("DOMContentLoaded", function () {
  const sidebarToggle = document.querySelector("#sidebar-toggle");
  const sidebar = document.querySelector("#sidebar");
  const COLLAPSED_KEY = "sidebarCollapsed";

  // Comprobar si la barra lateral estaba colapsada antes de la recarga de la página
  const isSidebarCollapsed = localStorage.getItem(COLLAPSED_KEY) === "true";

  if (isSidebarCollapsed) {
    sidebar.classList.add("collapsed");
    sidebar.style.transition = "none"; // Evitar transición al cargar la página
  }

  sidebarToggle.addEventListener("click", function () {
    const isCollapsed = sidebar.classList.contains("collapsed");

    // Habilitar la transición cuando se presiona el botón
    sidebar.style.transition = "all .2s ease-out";

    // Cambiar el estado de la barra lateral
    if (isCollapsed) {
      sidebar.classList.remove("collapsed");
      localStorage.setItem(COLLAPSED_KEY, "false");
    } else {
      sidebar.classList.add("collapsed");
      localStorage.setItem(COLLAPSED_KEY, "true");
    }
  });
});
