//Sidebar

const sidebarToggle = document.querySelector("#sidebar-toggle");

sidebarToggle.addEventListener("click", function () {
    const collapsibleElements = document.querySelectorAll("[data-bs-toggle='collapse']");
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

//Listado Clientes
var input = document.getElementById("exampleDataList");
var datalist = document.getElementById("datalistOptions");

var desde = document.getElementById('id_desde');
desde.addEventListener('input', fechamin);

function fechamin() {
    var desde = document.getElementById('id_desde');
    var hasta = document.getElementById('id_hasta');

    // Obtener la fecha seleccionada en 'desde'
    var fechaDesde = new Date(desde.value);

    // Incrementar la fecha en un día para obtener la nueva fecha mínima para 'hasta'
    fechaDesde.setDate(fechaDesde.getDate() + 7);

    // Formatear la nueva fecha como 'YYYY-MM-DD' (formato de fecha aceptado por input type="date")
    var nuevaFechaMinima = fechaDesde.toISOString().split('T')[0];

    // Establecer la nueva fecha mínima en 'hasta'
    hasta.min = nuevaFechaMinima;
}

function eventual() {
    // Obtener el valor actual del input
    var valorSeleccionado = desde.value;
    var hasta = document.getElementById('id_hasta');

    // Mostrar el valor en la consola
    console.log('Se seleccionó la fecha: ' + valorSeleccionado);
    hasta.value = valorSeleccionado;
}


function comprobar() {
    var chec = document.getElementById('chec');
    var desde = document.getElementById('id_desde');
    var hasta = document.getElementById('id_hasta');
    var hastaLabel = document.querySelector('label[for="id_hasta"]');
    var dias = document.getElementById('id_diasSemana');
    var diasLabel = document.querySelector('label[for="id_diasSemana"]');

    if (chec.checked) {
        dias.value = 1;
        hasta.min = desde.value;
        hasta.value = desde.value;

        //Se desactiva la fecha hasta
        hastaLabel.style.display = 'none';
        hasta.style.display = 'none';

        //Se desactiva la cantidad de dias
        diasLabel.style.display = 'none';
        dias.style.display = 'none';

        //Se agrega
        desde.removeEventListener('input', fechamin);
        desde.addEventListener('input', eventual);
    } else {


        //Activo la fecha hasta
        hasta.style.display = '';
        hastaLabel.style.display = '';
        hasta.value = "";

        //Activo los dias
        dias.style.display = '';
        diasLabel.style.display = '';
        dias.value = "";
        
        //Se elimina el evento eventual
        desde.addEventListener('input', fechamin);
        fechamin();
        desde.removeEventListener('input', eventual);
    }
}






