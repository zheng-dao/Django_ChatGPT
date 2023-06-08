/**
 * Form Field Validation
 * Using 'jquery.alphanumeric.js'
 */


$(function(){

    //Fields Restrictions
    $(".payeeName").alphanumeric();
    $(".payeeNickname").alphanumeric();
    $(".address1").alphanumeric();
    $(".address2").alphanumeric();
    $(".city").alphanumeric();

    $(".acctNumber").numeric();

    //Email Validation
    function validateEmail(sEmail) {
        var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        if (filter.test(sEmail)) {
            return true;
        }
        else {
            return false;
        }
    }

    //Email Validation On Form Submit
    $("#acceptButton, #optOut").on("click", function(e) {
        var emailAddress = $(".emailAddress").val();

        if (validateEmail(emailAddress)) {
            $(".emailAddress").next(".error").hide();
        }
        else {
            $(".emailAddress").next(".error").show();
        }

        e.preventDefault();
    });

    //Inline Email Validation
    $('.validateEmail').blur(function(){
        var emailValidation = $('.validateEmail').val();
        if (validateEmail(emailValidation)) {
            $('.validateEmail').next(".error").hide();
        }
        else {
            $('.validateEmail').next(".error").show();
        }
    });

    $('#optOut').on('click', function(){
        if( $('.acceptTerms').hasClass('checkmate') ){
            $('.checkboxError').hide();
        }else {
            $('.checkboxError').show();
        }
    });

    //Valid Characters
    var $validChars = $('.validateChars');
    $validChars.keyup(function(){
        var str = $(this).val();
        if(/^[a-zA-Z0-9- !&]*$/.test(str) == false) {
            $(this).next('.invalidChars').slideDown();
        } else {
            $(this).next('.invalidChars').slideUp();
        }
    });


});
