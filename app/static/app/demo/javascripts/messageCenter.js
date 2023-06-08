//Message Center
$(function(){
	var $replyBtn = $('#replyBtn'),
		$cancelMessage = $('#cancelMessage'),
		$replyMessage = $('.replyMessage');

	$replyMessage.hide(); //Hide Reply box on load
	//Show Reply Box on Click
	$replyBtn.on('click', function(e){
		$replyMessage.show();
		e.preventDefault();
	});

	/**
     * Message Character Count
     */
    $charCounter = $("#charCounter")
    $('#messageText').keyup(function(){
        var $totalChars = 3500,
            $chars = $(this).val().length;
        
        $charCounter.text($chars);
        
        if( $chars > $totalChars ){
            $(this).val($(this).val().substr(0, $totalChars));
        }
        
    });

	//Clear Fields and Close Reply box on 'cancel'
	$cancelMessage.on('click', function(){
		$('#messageText').val('');
		$charCounter.text('0'); //Rest Counter
		$replyMessage.hide();	
	});

	//Enable Delete Button if checkbox is checked
	$('#submitDelete').attr('disabled', 'disabled');

	var $checkboxes = $(".deleteCheck"),
    	$submitButt = $("#submitDelete");

	$checkboxes.on('click', function() {
	    $submitButt.attr("disabled", !$checkboxes.is(":checked"));
	});

	//Check all button
    $('#deleteAll').on('click', function(event) {  //on click 
        if(this.checked) { // check select status
            $('.deleteCheck').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "deleteCheck"  
                $('#submitDelete').removeAttr('disabled'); //Enable the delete button            
            });
        }else{
            $('.deleteCheck').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "deleteCheck"  
                $('#submitDelete').attr('disabled', 'disabled'); //Disable the delete button                     
            });         
        }
    });



	
});
