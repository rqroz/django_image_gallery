function submit_image_form(pk, data){
  $.post('/uploads/'+pk+'/upload/', data, function(result){
    console.log(result)
    // if(result.success){
    //
    // }
  })
}

$(function(){
  let datepicker = $("input[name='date_taken']");
  datepicker.datepicker({
    maxDate: 0,
  });
  datepicker.attr("autocomplete", "off");

  // Prevent form submition when user hits Enter
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  let upload_form = $("#upload-form")
  let submit_image_btn = upload_form.find('button')
  submit_image_btn.on('click', function(event){
    event.preventDefault();
    var valid = true;

    upload_form.find('input').each(function(){
      var $this = $(this);
      if(!$this.val()){
        valid = false;
        $this.addClass('input-invalid')
      }else{
        $this.removeClass('input-invalid')
      }
    })

    if(!valid){
      upload_form.find('.form-errors').not('.field-errors').text('Please fill the form correctly.')
    }else{
      let pk = upload_form.find('#user-pk').data('pk')
      submit_image_form(pk, upload_form.serialize());
    }
  })
})
