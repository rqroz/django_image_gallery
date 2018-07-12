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
})
