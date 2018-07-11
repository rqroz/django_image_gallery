$(function(){
  let datepicker = $("input[name='date_taken']");
  datepicker.datepicker({
    maxDate: 0,
  });
  datepicker.attr("autocomplete", "off");

  let status_form = $("#status-form");
  status_form.find("select[name='status']").change(function(){
    if($(this).val() !== "-1"){
        status_form.trigger('submit');
    }
  });
})
