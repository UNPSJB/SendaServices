document.addEventListener('DOMContentLoaded', (event) => {
  const url = new URL(window.location.href);
  // Obtengo "orden" de la url y prepara el array de campos que aplican el ordenamiento
  const urlOrden = url.searchParams.get("orden") || "";
  let orden = urlOrden.trim() !== "" ? urlOrden.split(",") : [];
  const ths = document.querySelectorAll('table.sortable th.sortable');

  // Iteramos sobre los th y ponemos el click
  ths.forEach(th => {
    const field = th.dataset.sField;
    const nombre = th.textContent;
    if (orden.includes(field)) {
      th.innerHTML = `${nombre}&nbsp;<i class="bi bi-arrow-up"></i>`;
    } else if (orden.includes(`-${field}`)) {
      th.innerHTML = `${nombre}&nbsp;<i class="bi bi-arrow-down"></i>`;
    }

    th.addEventListener("click", (event) => {
      const field = event.target.dataset.sField;
      if (orden.includes(field) || orden.includes("-" + field)) {
        if (orden.includes(field)) {
          orden = orden.filter(o => o !== field);
          orden.push(`-${field}`);
        } else if (orden.includes(`-${field}`)) {
          orden = orden.filter(o => o !== `-${field}`);
        }
      } else {
        orden.push(field);
      }
      url.searchParams.set('orden', orden.join(","));
      window.location.href = decodeURIComponent(url.href);
    });
  });

});
