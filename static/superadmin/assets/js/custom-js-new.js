

    var date = new Date();
date.setDate(date.getDate());
 $('.fc-datepicker').datepicker({
    format: "dd/mm/yyyy",
     multidate: true,
     startDate: date
 
 }).bind("change",function(){
            var minValue = $(this).val();
            minValue = $.datepicker.parseDate("yy-mm-dd", minValue);
            minValue.setDate(minValue.getDate()+1);
            $("#to").datepicker( "option", "minDate", minValue );
        })
 
 function showTestDate(){
  var value = $('.fc-datepicker').datepicker('getFormattedDate');
  var dates = $('.fc-datepicker').datepicker('getDates').length;

  $("#showDate").html(value);
$("#count").html(dates);
  //$("#showDate").val(value);  for passing  input value

}

$(function(){
        $("#to").datepicker({ dateFormat: 'yy-mm-dd' });
        $("#from").datepicker({ dateFormat: 'yy-mm-dd' }).bind("change",function(){
            var minValue = $(this).val();
            minValue = $.datepicker.parseDate("yy-mm-dd", minValue);
            minValue.setDate(minValue.getDate()+1);
            $("#to").datepicker( "option", "minDate", minValue );
        })
    });
