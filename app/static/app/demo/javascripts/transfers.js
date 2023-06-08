/**
 * Transfers
 */


$(function(){

    var $selectOptions = $(".selectedOption"),
        $customSelectContent = $(".customSelectContent");


    $selectOptions.on("click", function(e){
        //Close all other opened menus
        $customSelectContent.hide();
        //Open the one that's clicked
        $(this).next($customSelectContent).show();
        //This is where we stop this click event
        e.stopPropagation();
    });

    $(document).on("click", function(el){
        //If this dropdown is not the target - close it
        if( !$customSelectContent.is(el.target) ){
            $customSelectContent.hide();
        }
    });

    $(".transfer input").keydown(function (event) {
        // Prevent shift key since its not needed
        if (event.shiftKey == true) {
            event.preventDefault();
        }

        // Allow Only: keyboard 0-9, numpad 0-9
        if ((event.keyCode >= 48 && event.keyCode <= 57) || (event.keyCode >= 96 && event.keyCode <= 105)
                //Allow Only: backspace, tab, left arrow, right arrow
            || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 37 || event.keyCode == 39
                //Allow Only: delete, home, end
            || event.keyCode == 46 || event.keyCode == 36 || event.keyCode == 35
                //Allow Only: .(full stop [keyboar, numpad]) and check if there is more than one .(full stop)
            || ((event.keyCode == 190 || event.keyCode == 110) && $(this).val().indexOf('.') < 1)
                //Allow Only 1 comma
            || (event.keyCode == 188 && $(this).val().indexOf(',') < 1)
        ) {
            // Do what's needed
        } else {
            // Prevent the rest
            event.preventDefault();
        }
    });

    $(".payment input").keydown(function (event) {
        // Prevent shift key since its not needed
        if (event.shiftKey == true) {
            event.preventDefault();
        }

        // Allow Only: keyboard 0-9, numpad 0-9
        if ((event.keyCode >= 48 && event.keyCode <= 57) || (event.keyCode >= 96 && event.keyCode <= 105)
                //Allow Only: backspace, tab, left arrow, right arrow
            || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 37 || event.keyCode == 39
                //Allow Only: delete, home, end
            || event.keyCode == 46 || event.keyCode == 36 || event.keyCode == 35
                //Allow Only: .(full stop [keyboar, numpad]) and check if there is more than one .(full stop)
            || ((event.keyCode == 190 || event.keyCode == 110) && $(this).val().indexOf('.') < 1)
                //Allow Only 1 comma
            || (event.keyCode == 188 && $(this).val().indexOf(',') < 1)
        ) {
            // Do what's needed
        } else {
            // Prevent the rest
            event.preventDefault();
        }
    });

    //Select Option and Close dropdown
    $customSelectContent.each(function(){
        //Add a class on the clicked even and replace the original
        $('ul li.option').on('click', function (e) {
            $("ul li.option").removeClass("customSelected");
            $(this).addClass('customSelected');

            if(  $(this).hasClass("loan") ){
                $(this).parents(".customSelectContent").prev(".selectedOption").addClass("loanOption");
            }else {
                $(this).parents(".customSelectContent").prev(".selectedOption").removeClass("loanOption");
            }

            if( $(".loanOption")[0] ){
                $(".principal").show();
                $(".transferAmount").hide();
                $(".transferBtn").hide();
                $(".paymentBtn").show();
                $(".pageTitle").text("Payment");
            }else {
                $(".principal").hide();
                $(".transferAmount").show();
                $(".transferBtn").show();
                $(".paymentBtn").hide();
                $(".pageTitle").text("Transfer Funds");
            }

            var $selectedAccount = $("span.accountName", this).text();
            var $selectedAmount = $("span.sum", this).text();
                $(this).parents(".customSelectContent").prev(".selectedOption").html("<span class='accountName'>" + $selectedAccount + "</span>" + "<span class='sum'>" + $selectedAmount + "</span>");

            e.preventDefault();
        });

    });


    //Edit Recurring Payment Link
    $(".editRecurring").on("click", function(e){
        $(this).parent().prev(".recurringPaymentPanel").slideDown();
        $(this).parents(".fieldWrap").find(".recurringPaymentPicker").children(".rpHandle").addClass("on");
        e.preventDefault();
    });


    //Cancel Button Options
    $(".cancel").on("click", function(e){
        
        if( $(this).next(".cancelOptions").css("display") == "none" ){
            $(this).addClass("cSelected");
            $(this).next(".cancelOptions").show();
        }else {
            $(this).removeClass("cSelected");
            $(this).next(".cancelOptions").hide();
        }

        e.preventDefault();
    });

    //Close Cancel Options if click outside
    $(document).mouseup(function (e) {
        if (!$(".cancelWrap").is(e.target) && $(".cancelWrap").has(e.target).length === 0) {
            $(".cancelOptions").hide(); //Close Open panel
            $("a.cancel").removeClass("cSelected");
        }
    });




});
