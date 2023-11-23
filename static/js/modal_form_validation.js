const update_csrf_tokens = (new_csrf_token_value) => {
  const token_inputs = $('input[name=csrfmiddlewaretoken]', 'form');
  $.each(token_inputs, (idx, el) => {
    $(el).val(new_csrf_token_value);
  });
}

const display_field_errors = (data, config) => {
  let new_csrf_token_value;
          
  $.each(config, (content_wrapper, html_content) => {
    // Si hay errores, reemplazamos el contenido del form, por el form con los errores            
    $(content_wrapper).html(data[html_content]); //data['form_html']);

    // Debemos actualizar todos los csrf tokens en el form con el nuevo.
    if (!new_csrf_token_value) {
    const new_csrf_token_input = $(content_wrapper).find('input[name=csrfmiddlewaretoken]');
    new_csrf_token_value = $(new_csrf_token_input).val();
  }});
  
  // Por cada instancia, reemplazamos los value en los inputs correspondientes
  update_csrf_tokens(new_csrf_token_value);

  // Debemos añadir footer con botones al formset para poder añadir nuevos items dinámicamente.
  // usamos bindFormSet, definido en custom-inlines.js
  bindFormSet($('#modal'));
}

const handle_modal_validation = (url, form_data, config) => {
  /* Esta función hace un request asíncrono mediante ajax a la 'url' indicada, 
    enviando los datos en 'form_data' y modificando el DOM mediante valores indicados en 'config' */

  $.ajax({
    url: url,
    type: "POST",
    data: form_data,
    processData: false, // Se le indica a JQuery que no intente convertir 'form_data' a querystring
    contentType: false,
    success: function(data) {
    if (!(data['success'])) {
      // Si el servidor responde puede que success sea false. 
      // Es decir, el form contiene errores:
      display_field_errors(data, config);
    } else {
      // Si el/los formularios pasan la validación:
      // 1- Ocultamos los mensajes de error
      $.each(config, (content_wrapper, html_content) => {
          $(content_wrapper).find('.error-message').hide();
          //$(content_wrapper).find('.success-message').show(); // Opcionalmente, podemos mostrar un mensaje exitoso en el modal pero quizás convenga hacerlo usando django messages.
      });

      // 2 - hacemos submit del form a la URL de modificación original.
      $(".modal form").submit();

      // 3 - cerramos el modal.
      $('#modal').modal('hide');
      }
    },
    error: function () {
      // Si ocurre un error con el POST, se muestran los mensajes de error.
      $.each(config, (content_wrapper, html_content) => {
        $(content_wrapper).find('.error-message').show();
      });
    }
});
}