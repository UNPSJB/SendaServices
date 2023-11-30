const updateElementIndex = function (el, prefix, ndx) {
    const id_regex = new RegExp('(' + prefix + '-(\\d+|__prefix__))');
    const replacement = prefix + '-' + ndx;
    if ($(el).prop('for')) {
      $(el).prop('for', $(el).prop('for').replace(id_regex, replacement));
    }
    if (el.id) {
      el.id = el.id.replace(id_regex, replacement);
    }
    if (el.name) {
      el.name = el.name.replace(id_regex, replacement);
    }
  };
  
  const getQuitarButton = function (){
    button = document.createElement('a')
    button.classList.add('quitar')
    button.setAttribute('href', '#')
    button.appendChild(document.createTextNode('Quitar'))
    return button
  }
  
  const addInlineDeleteButton = function (row, prefix) {
    fila = row[0]
    hijos = Array.from(fila.childNodes)
    td_quitar = hijos.filter(n => n.id?.includes("DELETE"))[0]
    td_quitar.appendChild(getQuitarButton())
  
    row.find('a.quitar').on('click', function (event) {
      inlineDeleteHandler(event, prefix);
    });
    
  };
  
  
  const inlineDeleteHandler = function (e1, prefix) {
    e1.preventDefault();
    const deleteButton = $(e1.target);
    const row = deleteButton.closest('tr');
    const tbody = deleteButton.closest('tbody');
    const trs = $('tr', tbody);
    row.remove();
    
    $('#id_' + prefix + '-TOTAL_FORMS').val(trs.length);
  
    $('tr', tbody).each(function (i, tr) {
      updateElementIndex($(tr), prefix, i - 1);
      $(tr)
        .find('*')
        .each(function (j, e) {
          updateElementIndex(e, prefix, i - 1);
        });
    });
  };
  
  const inlineFormset = function ($context) {
    const prefix = $context.data('formset');
    
    const row = $('.d-none.empty-form', $context).clone(true);
    const table = $('.d-none.empty-form', $context).parents('table');
    const tbody = $('tbody', table);
    
    const agregarRenglon = $('<tfoot><tr><td colspan="4"><a class="btn btn-sm btn-outline-primary ">Agregar</a></td></tr></tfoot>');
    
    $('a', agregarRenglon).click(() => {
      const totalForms = document.querySelector('input[name$=-TOTAL_FORMS]'); //.prop('autocomplete', 'off');
      let nextIndex = Number($(totalForms).val());
      const newRow = row.clone(true);
  
      addInlineDeleteButton(newRow, prefix);
      newRow.removeClass('d-none empty-form');
      newRow.find('*').each(function (index, el) {
        updateElementIndex(el, prefix, nextIndex);
      });
  
      $(tbody).append(newRow);
      const trs = $('tr', tbody);
      console.log(trs);
  
      $('#id_' + prefix + '-TOTAL_FORMS').val(trs.length);
    });
    
    table.append(agregarRenglon);
    return prefix
  };
  
  const addQuitarButton = (prefix) => {    
    
    // Agrego los botones a los tds correspondientes
    const tds = document.querySelectorAll('[id$=DELETE]')
    let index = 0
    for (let td of tds) {
      if (td.id.includes(prefix) && !td.id.includes('__prefix__')) {
        index !== 0 ? td.appendChild(getQuitarButton()) : index++
      }
    }
  
    // Agrego funcionalidad a los botones agregados
    const botones = document.querySelectorAll('a.quitar')
    for (let b of botones){
      b.addEventListener('click', (e) => {
        e.preventDefault()
        b.parentElement.parentElement.remove()
      })
    }
  }
  
  const bindFormSet =function (context) {
    $('[data-formset]', context).each(function (index, el) {
        $('.checkboxinput',context).remove(); // quita el checkbox 
        
        const prefix = inlineFormset($(el));
        addQuitarButton(prefix)
    });
  };
  // Go bitch!
  $(document).ready(() => {
    bindFormSet(document);
    
  });
  