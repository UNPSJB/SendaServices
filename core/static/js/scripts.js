//Sidebar

const sidebarToggle = document.querySelector("#sidebar-toggle");

sidebarToggle.addEventListener("click", function () {
    const collapsibleElements = document.querySelectorAll("[data-bs-toggle='collapse']");
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

//Listado Clientes
var input = document.getElementById("exampleDataList");
var datalist = document.getElementById("datalistOptions");

input.addEventListener("input", function() {
    var searchTerm = input.value.toLowerCase();
    var options = datalist.getElementsByTagName("option");

    for (var i = 0; i < options.length; i++) {
        var option = options[i];
        var optionValue = option.value.toLowerCase();
        
        // Utilizamos una expresión regular para buscar coincidencias en CUIT, nombre y apellido
        var regex = new RegExp(searchTerm, 'i');
        if (optionValue.match(regex)) {
            option.style.display = "block";
        } else {
            option.style.display = "none";
        }
    }
});
