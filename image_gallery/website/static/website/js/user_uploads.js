$(function(){
  let datepicker = $("input[name='date_taken']");
  datepicker.datepicker({
    maxDate: 0,
  });
  datepicker.attr("autocomplete", "off");
})
