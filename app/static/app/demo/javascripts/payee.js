
//Format the Amount Total box
$.fn.digits = function() {
    return this.each(function () {
        $(this).text($(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
    })
}

$(function(){

    /**
     * Payment History Tab
     */
    var $singleTab = $(".singleTab"),
        $singleTabContent = $(".singleTabContent");

    $singleTab.on("click", function (e) {
        if ($(this).hasClass("current")) {
            $(this).parents(".wrap").find($singleTabContent).hide();
            $(this).removeClass("current");
        } else {
            $(this).parents(".wrap").find($singleTabContent).show();
            $(this).addClass("current");
        }
        e.preventDefault();
    });

    /** 
     * Update Payment Total
     */
    var $numOfRecurringpaymentsCount = 0; //BOKFOB-91 update request
    var $amount = $(".amt"),
        $sumTotal = $("#sumTotal"),
        $numOfPayments = $("#numOfPayments"),
        $numOfPayees = $("#numOfPayees");
        $confirmation = $("#confirmation");

    function updatePaymentTotal() {
        //Set Total Payments Amount
        var $totalPayment = 0.00;

        // Start Update: BOKFOB-55 (Round 2)
        $amount.keydown(function (event) {  
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
                || ((event.keyCode == 190 || event.keyCode == 110) && $(this).val().indexOf('.') < 0) 
            ) {
                // Do what's needed
            } else {  
                // Prevent the rest  
                event.preventDefault();  
            }  
        });

        $amount.each(function() {
            var i = parseFloat($(this).val(), 10);
            if (!isNaN(i)) {
                $totalPayment += i;
                $confirmation.css({
                    "visibility" : "visible"
                });
                $(this).next(".clearVal").fadeIn();
                $(this).parents(".wrap").next(".paymentDetails").find(".clearPayee").fadeIn();
            }
        });
        
        var $floatTotal = $totalPayment.toFixed(2);
        //Update Total
        $sumTotal.text($floatTotal).digits();
        // End Update: BOKFOB-55 (Round 2)   


        /* Original Code
        $amount.each(function() {
            var i = parseFloat($(this).val(), 10);
            if (!isNaN(i)) {
                $totalPayment += i;
                $confirmation.css({
                    "visibility" : "visible"
                });
            }
        });
        

        var $floatTotal = $totalPayment.toFixed(2);
        //Update Total
        $sumTotal.text($floatTotal);
        */
        
    } 

    $amount.keyup(function(){
        updatePaymentTotal();    
    });

    

    /**
     * Show Hidden Div on focus
    */ 
    $amount.focus(function(){
        $amount.each(function(){
            if ($(this).val() == "") {
                $(this).parents(".wrap").siblings(".paymentDetails").hide();
            }
        });
        $(this).parents(".wrap").siblings(".paymentDetails").show();
    });
    
    /**
     * Num of Payments + Num of Payees
     */
    function updateNumberOfPayees (){
        var $paymentCount = 0,
            $payeeCount = 0;
        $amount.each(function() {
            var i = parseFloat($(this).val(), 10);
            if (!isNaN(i)) {
                $paymentCount += 1;
                $payeeCount += 1;
            }
        });

        //Update Num of Payments
        $numOfPayments.text($paymentCount);
        //Update Num pf Payees
        $numOfPayees.text($payeeCount);
    }

    // used to calculate the number of recurring payments
    //BOKFOB-91 update request
    $("select[id^='recurringPeriod_']").change(function (e)
    {
        var divIndex = e.target.id;
        divIndex = divIndex.split('_')[1];
        var selectedVal = $(this).val();
        if (selectedVal.trim() != "") {
            $numOfRecurringpaymentsCount += 1;
        }
        else
        {
            $numOfRecurringpaymentsCount -= 1;
        }
        $("#numOfRecurringPayments").text($numOfRecurringpaymentsCount + ' of the payments are recurring. You can modify or delete any future payments.');

        // register the slideUp event only after selecting the recurring tab.
        $('#recurringPaymentPanel_' + divIndex).bind('slideUp', function () {
            var frequencyCount = $(this).find('[id$="__unlimitedPayments"]').is(':checked') ? "Unlimited" : "0";
            var frequency = $(this).find('[id^="recurringPeriod_"] option:selected').text();
            if (frequencyCount === "0") {
                frequencyCount = $(this).find('[id^="numberOfPayments_"]').val();
            }
            var displayText = "";
            if (frequency != "" && frequencyCount !=null)
            {
                displayText = "This payment will occur {0}, {1} payments total.".format(frequency, frequencyCount);
            }
            $('#recurringNotes_' + divIndex).text(displayText);

        });
    });

    $amount.keyup(function(){
        updateNumberOfPayees();    
    });

    /**
     * Show Confirmation box is amount is not empty
     * (checking on page load | refresh | post back)
     */
    $amount.each(function(){
        if($(this).val() !== "") {
            
            //Show Payment Details box
            $(this).parents(".wrap").siblings(".paymentDetails").show();

            //Show Confirmation Box
            $confirmation.css({
                "visibility" : "visible"
            });

            //Update Payees & Payments
            updateNumberOfPayees();

            //Update Total
            updatePaymentTotal();

        }
    });

    /**
     * Clearing Fields and Updating Total
     */

    $(".clearVal").on("click", function(){
        var $sub = $(this).prev("input").val().replace(/^\s+|\s+$/g, ""),
            $updateNumOfPayments,
            $updateNumOfPayees,
            $clearDate = $(".datepicker"),
            $clearMemo = $(".memo input");

        //Hide Reset Buttons
        $(this).parents(".wrap").next(".paymentDetails").find(".clearPayee").fadeOut();
        $(this).fadeOut();

        //Clear Date and Memo
        $(this).parents(".wrap").next(".paymentDetails").find(".datepicker").val("");
        $(this).parents(".wrap").next(".paymentDetails").find(".memo input").val("");

        //Hide Payment Details Box
        $(this).parents(".wrap").siblings(".paymentDetails").hide();

        //Clear Dollar Amount
        $(this).prev("input").val('');

        //Run Update Total Function
        updateOnClear($sub);

    });

    $(".clearPayee").on("click", function(){
        var $sub = $(this).closest(".paymentDetails").prev(".wrap").find("input.amt").val().replace(/^\s+|\s+$/g, ""),
            $updateNumOfPayments,
            $updateNumOfPayees,
            $clearDate = $(".datepicker"),
            $clearMemo = $(".memo input");

        //Hide Reset Buttons on click
        $(this).closest(".paymentDetails").prev(".wrap").find(".clearVal").fadeOut();
        $(this).fadeOut();

        //Clear Date and Memo
        $(this).closest(".paymentDetails").find(".datepicker").val("");
        $(this).closest(".paymentDetails").find(".memo input").val("");

        //Hide Payment Details Box
        $(this).closest(".paymentDetails").hide();

        //Clear Dollar Amount
        $(this).closest(".paymentDetails").prev(".wrap").find("input.amt").val('');

        //Run Update Total Function
        updateOnClear($sub);

    });

    //Update Total and Payee/Payments on Clear
    var updateOnClear = function update($sub){
        //On clear grab the Current SumTotal and Strip out the commas
        $sumTotalSanitized = $sumTotal.text().replace(',','');

        $updatePaymentAmount = $sumTotalSanitized - $sub;

        if( $sub !== '' ){
            $updateNumOfPayments = $numOfPayments.text() - 1;
            $updateNumOfPayees = $numOfPayees.text() - 1;
        }

        var $floatTotal = $updatePaymentAmount.toFixed(2);

        $sumTotal.text($floatTotal).digits();
        $numOfPayments.text($updateNumOfPayments);
        $numOfPayees.text($updateNumOfPayees);

        if($floatTotal == 0 || $floatTotal == 0.00) {
            $confirmation.css({
                "visibility" : "hidden"
            });
        }
    }

    /**
     * Locking / Unlocking Confirmation Container
     */
    var $placeholder = $("#confirmContainer"),
        $view = $(window); // Binding to Window Scroll and Resize

    if( $placeholder.length > 0 ){

        $view.bind("scroll resize", function(){
            /*
             Get Height of confirmationHolder to add to placeholder
             to avoid page jump (footer jump) when the confirmationHolder
             is pulled from the Document flow.
             */
            var $setHeight = $confirmation.height();
            $placeholder.css({
                "height" : $setHeight
            });

            /*
             Lock / Unlock Confirmation Container Based scroll & visibility
             Note: Using jquery.visible.min.js to get element screen offsets
             */
            if ($placeholder.visible()) {
                $confirmation.removeClass("fixed");
                $confirmation.addClass("notFixed");
            } else {
                $confirmation.addClass("fixed");
                $confirmation.removeClass("notFixed");
            }

        });
    }

    /**
     * Hidden Payee Layout
     */
    $(".payee").each(function(){
        if( $(this).hasClass("hiddenPayee")){
            $(this).children(".wrap").children().hide();
            $(this).children(".wrap").children(".payeeName").show();
            $(this).children(".wrap").children(".hiddenMessage").show();
        }
    });

    /**
     * Recurring Payment Panel
     */
    $(".recurringPaymentPicker a").each(function(){
        var $openPanel = $(this).parents(".recurringPaymentPicker").next();
        $(this).on("click", function(e){
            if( $openPanel.css("display") == "none"){
                $openPanel.slideDown();
                $(this).parent().addClass("on");
            }else {
                $openPanel.slideUp();
                $(this).parent().removeClass("on");
            }

            e.preventDefault();
        });

        $(".rpCancel").on("click", function(e){
            $(this).parents(".recurringPaymentPanel").prev(".recurringPaymentPicker").children(".rpHandle").removeClass("on");
            $(this).parents(".recurringPaymentPanel").prev(".recurringPaymentPicker").children(".rpHandle").removeClass("makeRecurring");
            $(this).parents(".recurringPaymentPanel").slideUp();
            e.preventDefault();
        });

        $(".rpSave").on("click", function(e){
            $(this).parents(".recurringPaymentPanel").prev(".recurringPaymentPicker").children(".rpHandle").removeClass("on");
            $(this).parents(".recurringPaymentPanel").prev(".recurringPaymentPicker").children(".rpHandle").addClass("makeRecurring");
            $(this).parents(".recurringPaymentPanel").slideUp();
            e.preventDefault();
        });

        //Enable & Disable 'Number of Payments' input
        $('input.rpCheck').change(function(){
            if ($(this).is(':checked') == true){
                $(this).parent(".numOfPayments").find('input.setNumPayments').prop('disabled', true);
                console.log('checked');
            } else {
                $(this).parent(".numOfPayments").find('input.setNumPayments').prop('disabled', false);
                console.log('unchecked');
            }
        });

        /**
         *  Open Recurring Payment Panel from Edit link
         */
        $(".edit").on("click", function(e){
            e.preventDefault();
            $(this).parents(".paymentDetails").find(".rpHandle").addClass("on");
            $(this).parents(".paymentDetails").find(".recurringPaymentPanel").slideDown();    
        });


        //Close Calendar Popup if click outside
        $(document).mouseup(function (e) {
            if (!$openPanel.is(e.target) && $openPanel.has(e.target).length === 0) {
                $openPanel.slideUp(200); //Close Open panel
                $openPanel.prev(".recurringPaymentPicker").children(".rpHandle").removeClass("on");
            }
        });

    });

    $(".closeCal").on("click", function(){
        $(".calendar-popup").hide();
    });

});

//BOKFOB-91 update request
$(function () {
    (function ($) {
        var orig_slideDown = $.fn.slideUp;

        $.fn.slideUp = function () {
            $(this).trigger('slideUp');
            orig_slideDown.apply(this, arguments);
        };
    })(jQuery);

});
