/**
 * Username Requirements
 */

//Check username match
function checkUsernameMatch() {
    var username = $("#usernameRequirements").val();
    var confirmUsername = $("#confirmUsername").val();

    if (username != confirmUsername) {
        $("#CheckUsernameMatch").show();
    } else {
        $("#CheckUsernameMatch").hide();
    }
}

$(function(){

    //Check match
    $("#confirmUsername").keyup(checkUsernameMatch);

    $('#usernameRequirements').keyup(function() {
        var username = $(this).val();

        //validate length
        if ( username.length < 6 || username.length > 20 ) {
            $('#length').removeClass('valid').addClass('invalid');
        } else {
            $('#length').removeClass('invalid').addClass('valid');
        }

        //numeric and alpha characters
        if ( username.match(/[a-zA-Z0-9]/) ) {
            $('#alphanum').removeClass('invalid').addClass('valid');
        } else {
            $('#alphanum').removeClass('valid').addClass('invalid');
        }

        //check for space
        if ( !username.match(/[\s]/) ) {
            $('#space').removeClass('invalid').addClass('valid');
        } else {
            $('#space').removeClass('valid').addClass('invalid');
        }

        //valid special characters
        if ( !username.match(/[%^&*{\}[\]|]/) ) {
            $('#validChars').removeClass('invalid').addClass('valid');
        } else {
            $('#validChars').removeClass('valid').addClass('invalid');
        }

    }).focus(function() {
        $('#username_info').show();
    }).blur(function() {
        $('#username_info').hide();
    });


});
