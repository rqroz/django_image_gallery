$(function(){
  let pass_modal = $("#user-pass-modal")
  let pass_form = $("#user-pass-form");
  let pass_submit = $("#update-pass-btn");

  function handle_error_data(data){
    for (input_name in data){
      let curr_input = pass_form.find('input[name="'+input_name+'"]');
      let field_errors = curr_input.closest(".fieldWrapper").find(".form-errors");
      field_errors.text(data[input_name]);
    }
  }

  pass_submit.on('click', function(event){
    event.preventDefault();
    pass_submit.attr('disabled', true);
    let valid = true;
    pass_form.find('.fieldWrapper').each(function(){
      let wrapper = $(this);
      let field = wrapper.find('input')

      if(field.val().length < 8){
        valid = false;
        wrapper.find('.form-errors').text('Passwords must have at least 8 characters.')
      }
    });

    if(!valid){
      pass_submit.attr('disabled', false);
      return
    }


    openWait();
    let target = pass_submit.data('target');
    $.post("/users/"+target+"/update-pass/", pass_form.serialize(), function(result){
      console.log(result)
      if(result.success){
        pass_modal.modal('hide');

        bootbox.alert({
          title: '<center>Great!</center>',
          message: '<center>Your password has been updated.</center>',
          callback: function(){
            window.location.reload();
          }
        })
      }else{
          if(result.errors) { handle_error_data(result.errors); }
      }
    }).always(function(){
      closeWait();
      pass_submit.attr('disabled', false);
    });
  })
})
