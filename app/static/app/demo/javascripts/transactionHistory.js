$(function(){

	$('.optionButton a').click(function(e){
        //Grab the HREF for matching ID
        var divID = $(this).attr('href');

        //Remove the Class from .actionItem
        $(this).parent().siblings().removeClass("current");

        //Hide All Panels on page Load
        $(this).parents(".historySearch").siblings(".historySearchOptions").not(divID).hide();

        //Show/Hide the proper panels
        if( $(this).parent().hasClass("current") ){
            $(this).parent().removeClass("current");
            $(divID).hide();
        }else {
            $(this).parent().addClass("current");
            $(divID).show();
        }
        //Prevent Link Default Action
        e.preventDefault();
    });

    //Clear Fields
    var $clear = $(".clear");

    $clear.on("click", function(e){
        $(this).parents(".flexContent").children(".flex").find("input").val('');
        e.preventDefault();
    });



});






