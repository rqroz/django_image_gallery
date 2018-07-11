function openWait(){
  var wait = $('#wait-modal');
  wait.modal({backdrop: 'static', keyboard: false});
  $("#wait-modal").modal('show');
}

function closeWait(){
  $("#wait-modal").modal('hide');
}

function scrollTo(target){
  $('html, body').animate({
      scrollTop: $(target).offset().top
  }, 1000);
}

$(function(){
  var csrftoken = getCookie('csrftoken');

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  $('.scroll-btn').each(function(){
    let btn = $(this);
    btn.on('click', function(event){
      event.preventDefault();
      let target = btn.data('target');
      scrollTo(target);
    });
  });

  let status_form = $("#status-form");
  status_form.find("select[name='status']").change(function(){
    if($(this).val() !== "-1"){
        status_form.trigger('submit');
    }
  });

  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover();
})
