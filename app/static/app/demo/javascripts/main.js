
/**
 * BOK Main JS File
 * Author: Pasquale Scerbo (pscerbo@extractable.com)
 */

/* Getting UserAgent so we can target IE10 */

var doc = document.documentElement;
doc.setAttribute('data-useragent', navigator.userAgent);

(function ($) {

    var $windowWidth =  $(window).width();

    //Vertical Align Content Function
    $.fn.vAlign = function() {
        return this.each(function(i){
            var ah = $(this).height();
            var ph = $(this).parent().height();
            var mh = Math.ceil((ph-ah) / 2);
            $(this).css('margin-top', mh);
        });
    };

    //Smooth Scroll to Anchor Links
    $.fn.smoothScroll = function(){
        return this.click(function(e){
            e.preventDefault();

            if($windowWidth > 1024){
                $('html,body').animate({
                    scrollTop:$(this.hash).offset().top - 130
                }, 500);
            }else {
                $('html,body').animate({
                    scrollTop:$(this.hash).offset().top - 85
                }, 500);
            }

        });
    }

})(jQuery);

$(function(){

    // HTML5 equivalent for browsers that don't recognize the 'placeholder' element
    if(!Modernizr.input.placeholder){

        $('[placeholder]').focus(function() {
            var input = $(this);
            if (input.val() == input.attr('placeholder')) {
                input.val('');
                input.removeClass('placeholder');
            }
        }).blur(function() {
            var input = $(this);
            if (input.val() == '' || input.val() == input.attr('placeholder')) {
                input.addClass('placeholder');
                input.val(input.attr('placeholder'));
            }
        }).blur();
        $('[placeholder]').parents('form').submit(function() {
            $(this).find('[placeholder]').each(function() {
                var input = $(this);
                if (input.val() == input.attr('placeholder')) {
                    input.val('');
                }
            })
        });

        $('body').on('refreshPlaceholders', function() {
            $('[placeholder]').each(function() {
                var input = $(this);
                if (input.val() == '' || input.val() == input.attr('placeholder')) {
                    input.addClass('placeholder');
                    input.val(input.attr('placeholder'));
                }

            });
        });
    }


    /**
     * Browser Detection
     */
    if( $("html").hasClass("ie8") ) {
        //alert("You're using IE8");
    };

    /**
     * Sliders
     */
    var $sliderTrigger = $(".sliderControls"),
        $sliderContent = $(".accountDetailsWrap, .paymentWrap, .alertsDetailsWrap");

    $sliderTrigger.on("click", function(){
        var $status = $(this).parents(".accountOverview, .alertOverview").next($sliderContent);
        if($status.css("display") == "block"){
            $(this).removeClass("active");
            $status.slideUp(400);
        }else {
            $(this).addClass("active");
            $status.slideDown(400);
        }
    });

    /**
     * User Account Dropdown
     */
    var $userDropdown = $(".userDropdown");

    //Hide Dropdown menu
    $userDropdown.css({
        "display" : "none"
    });

    $(".toolbar ul li.user").each(function(){
        $(this).on("mouseover", function(){
            $userDropdown.fadeIn(25);
        }).mouseleave(function(){
            $userDropdown.fadeOut(25);
        });
    });

    /**
     * Desktop Megamenu
     */
    $(".megamenu").megamenu();

    //BOKFOB-90 change request
    $(window).on("load resize",function(e){
        //Get the height of the window
        $('.accountDropdown .mm-content-base').addClass("scroll");
        $('.availableAccountsDropdown').addClass("scroll");
        var $windowHeight = $(window).height();
        if ($windowHeight <= 800) {
            $('.actionsDropdown .mm-content-base').addClass("scroll");
        } else {
            $('.actionsDropdown .mm-content-base').removeClass("scroll");
        }
    });

    /**
     * Nested Accordions (jquery.accordion.js)
     */
    $("ul.mobile").accordion();

    /**
     * Stop Page Scroll if Mobile Menu is open
     * Note:  Only need this if the menu is open, otherwise it causes issues with the smooth scroll and the html/body being set to 100%.
     */
    $(".mobileMenu").on("click", function(){
        if( $("body").hasClass("pushy-active") ){
            $("html, body").addClass('fixHeight');
            /*
            $("html, body").css({
                "overflow" : "hidden",
                "height" : "100%"
            });
            */
        }else {
            $("html, body").removeClass('fixHeight');
            /*
            $("html, body").css({
                "overflow" : "",
                "height" : ""
            });
            */
        }
    });

    $(".site-overlay").on("click", function(){
        $("html, body").removeClass('fixHeight');
        /*
        $("html, body").css({
            "overflow" : "",
            "height" : ""
        });
        */
    });

    function closeMobileMenu(){
        var win = $(this); //this = window
        if (win.width() >= 1024) {
            $('.pushy').removeClass('pushy-open');
            $('.pushy').addClass('pushy-right');
            $('body').removeClass('pushy-active');
            $('html, body').removeClass('fixHeight');
            $('header').removeClass('push-push');
            $('.main').removeClass('push-push');
            $('.main').removeClass('container-push');
            $('nav').removeClass('push-push');
            $('footer').removeClass('push-push');
        }
    }

    $(window).on('resize', function(){
        closeMobileMenu();
    });

    /**
     * Hide / Show Content
     */
    $('.actionItem a').click(function(e){
        //Grab the HREF for matching ID
        var divID = $(this).attr('href');

        //Remove the Class from .actionItem
        $(this).parent().siblings().removeClass("current");

        //Hide All Panels on page Load
        $(this).parent().siblings(".actionContent").not(divID).hide();

        //Show/Hide the proper panels
        if( $(this).parent().hasClass("current") ){
            $(this).parent().removeClass("current");
            $(divID).hide();
        }else {
            $(this).parent().addClass("current");
            $("#activitiesContent").hide();
            $(".activitiesOverview").removeClass("open");
            $(divID).show();
        }
        //Prevent Link Default Action
        e.preventDefault();
    });

    /**
     * Layout Updates
     */
    $("table.summary").find("tr:last").addClass("last");
    $(".ctaWrap .ctaBox:last-child").addClass("last");

    $(".accountInfoTable table").find("tr:last").addClass("last");
    $(".transactionHistory table").find("tr:last").addClass("last");
    $(".accountInfoTable table").find("tr td:first-child").addClass("first");

    /**
     * Update on Load and Resize
     */
    $(window).resize(function (){
        $('.valignmiddle').vAlign();
    });
    $(window).resize();

    /**
     * SmoothScroll
     */
    $('a.scroll').smoothScroll();

    /**
     * Activities Overview Slider
     */
    var $overviewTrigger = $(".activitesTrigger"),
        $activitiesContent = $(".activitiesContent"),
        $overviewTriggerBtn = $(".activitiesOverview");

    $activitiesContent.hide();

    $overviewTrigger.on("click", function(e){
        e.preventDefault();
        var $nextContent = $(this).parent(".balance").next($activitiesContent);
        if($nextContent.css("display") == "none"){
            $nextContent.slideDown();
            $(this).addClass("open");
        }else {
            $nextContent.slideUp();
            $(this).removeClass("open");
        }
    });

    $overviewTriggerBtn.on("click", function(e){
        e.preventDefault();
        var $nextContent = $(this).next($activitiesContent);
        if($nextContent.css("display") == "none"){
            $nextContent.show();
            $("#iWantTo").hide();
            $(".actionItem").removeClass("current");
            $(this).addClass("open");
        }else {
            $nextContent.hide();
            $(this).removeClass("open");
        }
    });

    /* Lightbox */
    //Inline
    $('.inline-popup').magnificPopup({
        type: 'inline'
    });

    //AJAX
    $('.ajax').magnificPopup({
        type: 'ajax'
    });

    //iFrame
    $('.iframe').magnificPopup({
        type: 'iframe'
    });

    $('.closeBtn').click(function(){
        $.magnificPopup.close();
    });

    //Calendar Popup
    $('.day .active').each(function(){
        $(this).magnificPopup({
            items: {
                src: $(this).next('.white-popup'), // should load the next popup
                type: 'inline'
            }
        })
    });

    //Calendar Tip
    /*
    $(".tipContent").hide();
    $(".tip").on("click", function(e){
        $(this).children(".tipContent").fadeIn().css({
            "position" : "fixed"

        });
        e.stopPropagation();
    });

    $(".closeTip").on("click", function(e){
        $(this).parent().fadeOut();
        e.stopPropagation();
    });
    */

    /**
     * Responsive Tooltip
     */
        // Show - Hide Tipso on Click
    $('.tipContent').tipso({
        background: '#FFF',
        position: 'bottom',
        useTitle: false,
        onShow: function(){
            $(".tipClose").on('click', function() {
                $('.tipContent').tipso('hide'); // Hide the open tip
            });
        }
    });

    $('.show-hide-tipso').on('click', function(e){
        $('.tipContent').tipso('hide');
        $(this).parent('.tipContent').tipso('show');
        e.preventDefault();
    });

    //Close Tooltip if click outside
    $(document).mouseup(function (e) {
        if ( !$('.tipContent').is(e.target) && $('.tipContent').has(e.target).length === 0) {
            $('.tipContent').tipso('hide');
        }
    });

    /**
     * Terms Acceptance Box
     */
    $("#acceptButton").attr("disabled", true);

    $("#terms").on("scroll resize", function(){
        var $contentHeight = $(".scrollTerms")[0].scrollHeight;
        $scrolledFromTop = $(this).scrollTop();
        $wrapperHeight = $(this).height() + 200;

        if( $contentHeight - $scrolledFromTop <= $wrapperHeight ){
            $("#acceptButton").removeAttr("disabled", false);
        }
    });

    /**
     * Field Formatting
     */
    //BOKFOB-90 change request
    //$("#zipcode").mask("99999?-9999");
    //$('#phone').mask('(999) 999-9999');


    /**
     * Find and Replace Selected Menu Text
     */
    $(".dropContent").each(function(){
        var $selected = $(this).find("a.selected").html();
        $(this).prev(".menuTitle").text($selected);
    });

    /**
     * Add a scroll bar if menu is taller than 300px
     */
    var $dropMenuHeight = $('.dropContent').height();
    if( $dropMenuHeight >= 301 ){
        $('.dropContent .content').addClass('addScroll');
        console.log($dropMenuHeight);
    }

    /**
     * Simple Dropdown
     */
    $('.menuTrigger').on("click", function(e){
        if( $(this).is(e.target) && !$(this).hasClass("selectAccount") ){
            $(".menuContent").hide();
            $(".menuTrigger").removeClass("selectAccount");
            //console.log('stop clicking me');
            $(this).next(".menuContent").show();
            $(this).addClass("selectAccount");
        }else {
            $(this).next(".menuContent").hide();
            $(this).removeClass("selectAccount");
        }
    });

    /**
     * Close Simple Menu on click outside
     */
    $(document).mouseup(function (e) {
        var $inlineDropdown = $(".dropdownWrap");

        if (!$inlineDropdown.is(e.target) && $inlineDropdown.has(e.target).length === 0) {
            $(".menuContent").hide(); //Close Open panel
            $(".menuTrigger").removeClass("selectAccount");
        }
    });

    /**
     * Checkboxes
     */
    $("input[type='checkbox']").change(function () {
        $(this).siblings('ul')
            .find("input[type='checkbox']")
            .prop('checked', this.checked);
    });

    $("input[type=checkbox]").each(function () {
        var checkedValue = $(this).attr("disabled");
        if (checkedValue == "disabled") {
            $(this).next('label').addClass('disabled').unbind();
        }
    });


    // Handled disabling of submit button on form submit
    //BOKFOB-90 change request
    $('form').on('submit', function (e, obj) {
        $('input:submit').css('background', '#AEACAC');
        $('input:submit').attr('disabled', true);
        var oldHandler = $('form').prop("onsubmit");
        var result = oldHandler.call(this, e);
        if (result == false) {
            $('input:submit').css('background', '#007db1');
            $('input:submit').attr('disabled', false);
        }
    });
    
    /**
     * Request Checks / Statement Options
     */
    $('#requestOption').change(function(){
        if($('#requestOption').val() == 'check') {
            $('#checkRequest').show();
            $('#statementRequest').hide();
        } else if ($('#requestOption').val() == 'statement') {
            $('#checkRequest').hide();
            $('#statementRequest').show();
        }else {
            $('#checkRequest').hide();
            $('#statementRequest').hide();
        }

        $("#checkAmount").keydown(function (event) {
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

        $("#checkNumber").keydown(function (event) {
            if ((event.keyCode >= 48 && event.keyCode <= 57) || (event.keyCode >= 96 && event.keyCode <= 105)
                    //Allow Only: backspace, tab, left arrow, right arrow
                || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 37 || event.keyCode == 39
                    //Allow Only: delete, home, end
                || event.keyCode == 46 || event.keyCode == 36 || event.keyCode == 35
            ) {
                // Do what's needed
            } else {
                // Prevent the rest
                event.preventDefault();
            }
        });

    });

});


