/**
 * Locations Page
 */


$(function(){

	//Hours Trigger
	$hoursTrigger = $('.hoursTrigger')	
	$hoursContent = $('.hoursContent')	

	$hoursTrigger.on('click', function(){
		var self = $(this);

		if( self.hasClass('active') ){
			self.removeClass('active');
			self.next($hoursContent).slideUp(100);
		}else {
			self.addClass('active');
			self.next($hoursContent).slideDown(100);	
		}
	});

	$(window).load(function(){
		$('#mapView').hide();
	});

	$('.viewToggle ul li a').on("click load", function(e){

		//Hide all views
		$('.view').hide(); 
		
		//Get URL of clicked element and display the appropriate content
		var toggleURL = $(this).attr('href');
		var activeDiv = toggleURL.substring(1, toggleURL.length); //Remove the # from URL
		console.log(toggleURL);

		//Remove the '.activeView' class from all
		$('.viewToggle ul li a').removeClass('activeView');
		
		//Add the '.activeView' to the clicked link
		$(this).addClass('activeView');

		//Show the view with the matching ID
		$(toggleURL).show();

		e.preventDefault();

	});

	$('#locationSearchOptions').change(function(){
		if($('#locationSearchOptions').val() == 'address') {
            $('#addressField').show();
        } else {
            $('#addressField').hide();
        }

	});
        


});










