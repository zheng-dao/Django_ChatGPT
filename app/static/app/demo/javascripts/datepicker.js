/**
 * Datepicker
 * jQuery UI Datepicker
 */


$(function(){

    $(".datepicker").click(function(){

        var $calendarPopup = $(".calendar-popup");

        //Open Calendar Popup
        $(this).each(function(){
            $(this).next($calendarPopup).fadeIn();
        });

        //Close Calendar Popup if click outside
        $(document).mouseup(function (e) {
            if (!$calendarPopup.is(e.target)
                && $calendarPopup.has(e.target).length === 0) {
                $calendarPopup.fadeOut();
            }
        });

    }).datepicker("setDate", new Date());

    $(".dateRange").datepicker();

    //Block future dates in the datepicker
    $(".clearDate").datepicker({
        maxDate: '0',
        beforeShowDay: $.datepicker.noWeekends,  //Disable Weekends
        showButtonPanel: true
    });

    /* jQuery UI Datepicker */
    $( ".calendarPage" ).datepicker({
        beforeShowDay: $.datepicker.noWeekends,  //Disable Weekends
        showButtonPanel: true,
        minDate: 0, //Disable past dates
        onSelect: function(date){
            // Set Date to .datepicker field
            $(this).parent(".calendar-popup").prev(".datepicker").val(date);
            // Close .calendar-poup
            $(this).parent(".calendar-popup").fadeOut();
        }
    });


});
