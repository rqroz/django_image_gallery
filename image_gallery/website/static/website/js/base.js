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

  let imediate_form = $(".imediate-form");
  imediate_form.find("select").change(function(){
    if($(this).val() !== "-1"){
        imediate_form.trigger('submit');
    }
  });

  $(".free-wall").each(function(){
    let wall = new Freewall($(this));
    wall.reset({
      selector: '.item',
      cellW: function(container) {
        var cellWidth = 250;
        return cellWidth;
      },
      cellH: function(container) {
        var cellHeight = 250;
        return cellHeight;
      },
      fixSize: 0,
      gutterY: 20,
      gutterX: 20,
      onResize: function() {
        wall.fitWidth();
      }
    })
    wall.fitWidth();
  })

  $(window).trigger("resize");

  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover();
})
