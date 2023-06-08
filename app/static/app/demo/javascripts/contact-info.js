$(function(){
    /**
     * Select All Accounts Checkbox
     */

    //Add 'checkmate' class to all labels that follow a checkbox
    $("input[type='checkbox']:checked").each(function(){
        $(this).next('label.checkbox').addClass('checkmate');
    });
    
    $('label.checkbox').on('click', function(){
        if( $(this).hasClass('checkmate') ){
            $(this).prev('input[type=checkbox]').removeAttr('checked', 'checked');
            $(this).removeClass('checkmate');
        }else {
            $(this).prev('input[type=checkbox]').attr('checked', 'checked');
            $(this).addClass('checkmate');
        }
    });
    
    $('a.selectAllAccounts').on('click', function(e){
        if( $(this).hasClass('selectAll') ){
            $(this).removeClass('selectAll');
            $(this).text('Deselect All');
            $('.checkboxes').find(':checkbox').attr('checked', 'checked');
            $(this).parent().next('.checkboxes').find('label').addClass('checkmate');
        }else {
            $(this).addClass('selectAll');
            $(this).parent().next('.checkboxes').find('label').removeClass('checkmate');
            $(this).text('Select All');
            $('.checkboxes').find(':checkbox').removeAttr('checked', 'checked');
        }
        
        e.preventDefault();
    });

    /**
     * Additional Mailing Address
     */
    $('.mailingAddressdiv').hide();

    if( $('#mailingAddressCheck').hasClass('checkmate') ){
        $('.mailingAddressdiv').show();
    }

    $('#mailingAddressCheck').on('click', function(){
        if( $('#mailingAddressCheck').hasClass('checkmate') ){
            $('.mailingAddressdiv').slideDown();
        }else {
            $('.mailingAddressdiv').slideUp();
        }
    });
    
    /**
     * Address Change Request
     */
    $('.addressChanges').hide();
    $('.doNotApplyToAll').on('click', function(){
        $('.addressChanges').slideDown();
    });
    $('.applyToAll').on('click', function(){
        $('.addressChanges').slideUp();
    });
    
    /**
     * Character Count
     */
    $('.optionalComments').keyup(function(){
        var $totalChars = 3000,
            $charCounter = $("#charCounter"),
            $chars = $(this).val().length;
        
        $charCounter.text($chars);
        
        if( $chars > $totalChars ){
            $(this).val($(this).val().substr(0, $totalChars));
        }
        
    });
    
    
    
    
});


