$(function(){

    var $alertHandle = $('.js-trigger'),
       $emailList = $('.js-panel');

    $alertHandle.on('click', function(e){

        var $thisPanel = $(this).parents('.alert_row').find('.js-panel');

        if( $thisPanel.css("display") == "block" ){
            $thisPanel.hide();
            $(this).removeClass('is-active');
        }else {
            $thisPanel.show();
            $(this).addClass('is-active');
        }

        e.preventDefault();
    });

    //Open 'Send To' Panel on focus
    var $amountThreshold = $('.amountThreshold');
    $amountThreshold.on('focus', function(){
        $(this).parents('.alert_threshold').siblings('.alert_sendto').find('.js-trigger').addClass('is-active');
        $(this).parents('.alert_threshold').siblings('.js-panel').show();
    });

    //Display 'save' and 'reset' buttons on change
    $('.saveBtn').css({
        "visibility" : "hidden"
    });
    $('.js-reset').css({
        "visibility" : "hidden"
    });

    $amountThreshold.on('change keyup', function(){
        $(this).parents('.alert_threshold').siblings('.alert_save').find('.saveBtn').css({
            "visibility" : "visible"
        });
        $(this).parents('.alert_threshold').siblings('.alert_save').find('.js-reset').css({
            "visibility" : "visible"
        });
    });

    //Check for changes to the checkboxes
    /*
    $(".alert_email_list_options").each(function(){
        if($(this).children('input[type=checkbox]').is(':checked')) {
            alert('you checked or unchecked something');
        }
    });
    */


    //Allow only number in the amount box
    $(".alert_threshold input").keydown(function (event) {
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



    //Email Validation Function
    function manageEmails(sEmail) {
        var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        if (filter.test(sEmail)) {
            return true;
        }
        else {
            return false;
        }
    }

    //Manage Contacts
    var $storedValue = $('.manage_contacts_item .storedValue');

    //
    // == Set the current value to a data attribute
    //
    $storedValue.each(function(){

        var $currentValue = $(this).val(); //Get the value
        $(this).attr('data-currentValue', $currentValue);  //Set the value

        //Compare the values
        $(this).on('change keyup blur', function(){
            var $dataValue = $(this).attr('data-currentValue'),
                value = $(this).val();

            //Match New Value against Old Value
            if( value != $dataValue ){
                //if the values don't match - show the confirm box
                $(this).siblings('.confirmChange').slideDown();
            }else {
                //otherwise hide the confirm box
                $(this).siblings('.confirmChange').slideUp();
            }

            //Validate Email Address
            if (manageEmails(value)) {
                $(this).next(".error").slideUp();
            }
            else {
                $(this).next(".error").slideDown();
            }

        });

    });

    //
    // == Confirm Email Address Match
    //
    var $confirmEmails = $('.manage_contacts_item');

    $confirmEmails.on('change blur keyup', function(){
        var emailValue = $(this).children('.storedValue').val(),
            confirmEmailValue = $(this).children('.confirmChange').find('.confirmEmail').val(),
            confirmError = $(this).find('.confirmError');

        if (emailValue != confirmEmailValue) {
            $(confirmError).slideDown();
        } else {
            $(confirmError).slideUp();
        }
    });

    //
    // == Cancel Changes
    //
    var $cancelChange = $('.manage_contacts_item .confirmChange .cancelChange');

    $cancelChange.on('click', function(){
        //Get the stored value
        var $originalValue = $(this).parents('.manage_contacts_item').children('.storedValue').attr('data-currentValue');

        //Reset the original value
        $(this).parents('.manage_contacts_item').children('.storedValue').val($originalValue);
        //Close Change Div
        $(this).parents('.confirmChange').slideUp();
        //Clear Confirm Email address
        $(this).closest('.confirmEmail').val('');

    });

    //
    // == Add New Contact Panel
    //
    var $newContactBtn = $('#addNewEmail'),
        $newContactPanel = $('#newEmailContact');

    $newContactPanel.hide();

    $newContactBtn.on('click', function(e){
        $newContactPanel.toggle();
        e.preventDefault();
    });

    //
    // == Validate New Email Contact
    //
    var $newEmailContact = $('.newEmailContact'),
        $confirmEmailContact = $('.confirmEmailContact');

    $newEmailContact.on('blur change keyup', function(){
        var luigi = $(this).val();
        //Validate Email Address
        if (manageEmails(luigi)) {
            $(this).next(".error").slideUp();
        }
        else {
            $(this).next(".error").slideDown();
        }
    });

    //
    // == Confirm New Email Contact Match
    //
    $confirmEmailContact.on('change blur keyup', function(){
        var emailValue = $newEmailContact.val(),
            confirmEmailValue = $(this).val();

        if (emailValue != confirmEmailValue) {
            $(this).next().slideDown();
        } else {
            $(this).next().slideUp();
        }
    });

    $('.cancelNewContact').on('click', function(){
        $(this).parents('.newContact').find('input[type=text]').val('');
        $(this).parents('#newEmailContact').hide();
        $(this).parent('.emailMatch').find('.confirmError').hide();
        $(this).parents('.newContact').find('.error').hide();
    });

    //
    // == Manage Alerts Options
    //
    var $alertsOptions = $('label');

    $alertsOptions.on('click', function(){
        $(this).parents('.alert_row').find('.saveBtn').css({
            "visibility" : "visible"
        });
        $(this).parents('.alert_row').find('.js-reset').css({
            "visibility" : "visible"
        });
    });

    // Threshold Original Values
    var $amountThreshold = $('.amountThreshold');

    $amountThreshold.each(function(){
        var $currentValue = $(this).val(); //Get the value
        $(this).attr('data-currentThreshold', $currentValue);  //Set the value
    });

    // Value of checked boxes
    var $checkboxState = $('input[type=checkbox]');

    $checkboxState.each(function(){
        if( $(this).is(':checked') ) {
            $(this).addClass('checkSet');
        } else {
            $(this).addClass('checkNotSet');
        }
    });

    //Reset Values to original
    var $alertsReset = $('.js-reset');

    $alertsReset.on('click', function(e){
        //Get the Value of the Threshold and....
        var $thresholdItem = $(this).parents('.alert_row').children('.alert_threshold').find('.amountThreshold');
        // ...Set it back to original
        var $originalValue = $thresholdItem.attr('data-currentThreshold');
        $($thresholdItem, this).val($originalValue);

        //Reset the checkboxes
        var checkResetValue = $(this).parents('.alert_row').find('input[type=checkbox].checkSet');

        if( $(checkResetValue).hasClass('checkSet') ){
            $(checkResetValue, this).attr('checked', 'checked');
            $(checkResetValue, this).next('label.checkbox').addClass('checkmate');
        }

        var checkResetValue = $(this).parents('.alert_row').find('input[type=checkbox].checkNotSet');

        if( $(checkResetValue).hasClass('checkNotSet') ){
            $(checkResetValue, this).removeAttr('checked', '');
            $(checkResetValue, this).next('label.checkbox').removeClass('checkmate');
        }

        //Hide the Save Buttons if you click reset
        $(this).parents('.alert_row').children('.alert_save').find('.saveBtn').css({
            "visibility" : "hidden"
        });

        $(this).css({
            "visibility" : "hidden"
        });

        e.preventDefault();
    });


    //Clear Fields
    var $clearAlert = $('.alert_clear input[type=button]');

    $clearAlert.on('click', function(){
        //Get the Value of the Threshold and....
        var $thresholdItem = $(this).parents('.alert_row').children('.alert_threshold').find('.amountThreshold');
        //...clear it
        $thresholdItem.val('');

        //Get the Checkboxes and ...
        var checkResetValue = $(this).parents('.alert_row').find('input[type=checkbox]');
        //...clear them too
        $(checkResetValue, this).removeAttr('checked', '');
        $(checkResetValue, this).next('label.checkbox').removeClass('checkmate');

        //Close the 'send to' panel
        $(this).parents('.alert_clear').siblings('.alert_sendto').find('.js-trigger').removeClass('is-active');
        $(this).parents('.alert_clear').siblings('.js-panel').hide();

    });





});
