$(function(){
  $('.like-container').each(function(){
    var like_container = $(this);
    like_container.on('click', function(event){
      event.preventDefault();

      let pk = like_container.parent().data('pk');
      $.post('/gallery/like/', {'pk': pk}, function(result){
          if(result.liked){
            like_container.addClass('user-liked')
          }else{
            like_container.removeClass('user-liked')
          }
          like_container.find('.likes-text').text(result.likes)
      });
    });
  });


  let order_label = $("#gallery-filter-form").find('.order-label');
  let order_input = order_label.find('input[type="checkbox"]');
  let order_icon = order_label.find('i');
  order_input.on('change', function(){
    if(this.checked){
      order_icon.addClass('fa-sort-up');
      order_icon.removeClass('fa-sort-down');
    }else{
      order_icon.addClass('fa-sort-down');
      order_icon.removeClass('fa-sort-up');
    }
  });
})
