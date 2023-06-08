$(function(){

    /**
     * Enable Submit Button if Fields are not Empty
     */
    $('#submit').attr('disabled', 'disabled');
    $('#btnSubmit').attr('disabled', 'disabled');

    //Run Function on page load
    notEmpty();

    function notEmpty(){

        var empty = false;
        $('.notEmpty').each(function() {
            if ($(this).val() == '') {
                empty = true;
            }
        });

        if (empty) {
            $('#submit').attr('disabled', 'disabled');
        } else {
            $('#submit').removeAttr('disabled');
        }
    }

    //Run noEmpty function on keyup
    $('.notEmpty').on('keyup change', function() {
        notEmpty();
    });

    //Request a Statement
    selectEmpty();

    function selectEmpty(){

        var empty = false;
        $('.selectEmpty').each(function() {
            if ($(this).val() == '') {
                empty = true;
            }
        });

        if (empty) {
            $('#btnSubmit').attr('disabled', 'disabled');
        } else {
            $('#btnSubmit').removeAttr('disabled');
        }
    }

    //Run noEmpty function on keyup
    $('.selectEmpty').on('keyup change', function() {
        selectEmpty();
    });


    /**
     * Terms of Use for Overdraft Protection
     */
    $('.optinCheck').on('click', function(){
        if( $('.optinCheck').hasClass('checkmate') ){
            $('#termsofuse').show();
        } else {
            $('#termsofuse').hide();
        }
    });

    $('.enableSubmit').on('click', function(){
        if( $('.enableSubmit').hasClass('checkmate') ){
            $('#optOut').removeAttr('disabled');
        } else {
            $('#optOut').attr('disabled', 'disabled');
        }
    });

});


