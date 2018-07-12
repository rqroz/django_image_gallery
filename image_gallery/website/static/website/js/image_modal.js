$(function(){
  let image_modal = $("#image-modal"),
      modal_body = image_modal.find('.modal-body'),
      modal_dialog = image_modal.find('.modal-dialog');

  $('.zoom-container').each(function(){
    var zoom_container = $(this);
    zoom_container.on('click', function(event){
      event.preventDefault();
      let parent = zoom_container.parent(),
          target = parent.data('target'),
          width = parent.data('width'),
          height = parent.data('height');

      let max_width = 800;
      let ratio = Math.min(max_width/width, max_width/height)
      let width_used = parseInt(width*ratio)
      let height_used = parseInt(height*ratio)

      var body_css = {
        'background-image': 'url("'+target+'")',
        'background-position': 'center',
        'background-repeat': 'no-repeat',
        'background-size': 'cover',
        'width': width_used+'px',
        'height': height_used+'px',
      }

      $('.modal-dialog').width(width_used);
      $('.modal-dialog').height(height_used);

      modal_body.css(body_css);
      image_modal.modal('show');
    });
  });

  image_modal.on('hide.bs.modal', function(event){
    image_modal.css('background-image', 'none');
  })
})
