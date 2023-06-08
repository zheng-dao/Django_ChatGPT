/**
 * Help With Page
 */


$(function(){

    $('.helpScreenContent').slick({
        infinite : false,
        adaptiveHeight: true,
        prevArrow: $('#slickPrev'),
        nextArrow: $('#slickNext')
    });

    var currentSlide = $('.helpScreenContent').slick('slickCurrentSlide') + 1;
    var setPosition = $('.helpScreenContent').slick('slickCurrentSlide') + 1;

    function helpWithPage(){
        var $docHeight = $(document).height();
        if( $('body').hasClass('active') ){
            $('body').removeClass('active');
            $docHeight = 0;
        }else {
            $('body').addClass('active');
            $('.helpOverlay').css({
                'height' : $docHeight
            });
        }
    }


    $('.helpTrigger').click(function (e) {
        $('.pushy').removeClass('pushy-open');
        $('.pushy').addClass('pushy-right');
        $('body').removeClass('pushy-active');
        $('html, body').removeClass('fixHeight');
        $('header').removeClass('push-push');
        $('.main').removeClass('push-push');
        $('.main').removeClass('container-push');
        $('nav').removeClass('push-push');
        $('footer').removeClass('push-push');

        helpWithPage();

        e.preventDefault();
    });

    //Close button
    var $helpClose = $('.helpScreenClose');
    $helpClose.on('click', function(e){
        helpWithPage();
        e.preventDefault();
    });

    //Count the number of help slides...
    var slideCount = $('.helpScreenContent div').length - 2; //slick slider duplicated the 1st and last slide
    //...and update the HTML
    var $availableSlides = $('.availableSliders');
    $availableSlides.text(slideCount);

    //Get the index of the active slide (zero based)
    function activeSlideCounter (){
        var activeSlide = $('.slick-active').data('slick-index') + 1,
            $slideIndex = $('.slideIndex');

        $slideIndex.text(activeSlide);

        $('html, body').animate({scrollTop : 0},800);
    }

    activeSlideCounter();
    //Update the active slide on click...
    $('.slideIndexCounter').on('click', function(){
        activeSlideCounter();
    });
    //...or on swipe
    $('.helpScreenContent').on('swipe', function(event, slick, direction){
        activeSlideCounter();
    });

    //Table of Contents
    var $toc = $('.toc');

    $toc.on('click', function(){
        if( $(this).hasClass('is-active')){
            $('#tocContent').slideUp();
            $(this).removeClass('is-active');

            $('.helpScreenHeader ul, .helpScreenClose').css({
                'visibility' : 'visible'
            });
        }else {
            $('#tocContent').slideDown();
            $(this).addClass('is-active');

            $('.helpScreenHeader ul, .helpScreenClose').css({
                'visibility' : 'hidden'
            });
        }
    });

    var $tocItem = $('a.tocItem');

    $tocItem.on('click', function(e){
        var $slideItem = $(this).data('slideitem');
        $('.helpScreenContent').slick('slickGoTo', $slideItem );

        $toc.removeClass('is-active');
        $('#tocContent').slideUp();

        $('.helpScreenHeader ul, .helpScreenClose').css({
            'visibility' : 'visible'
        });

        $('html, body').animate({scrollTop : 0},800);

        activeSlideCounter();

        e.preventDefault();
    });

});
