(function($) {
    "use strict";




    $(window).on("load", function() {

        /* ----------------------------------------------------------- */
        /*  BITCOIN PRELOADER
        /* ----------------------------------------------------------- */

        if ($("#preloader")[0]) {
            $("#preloader").delay(500).fadeTo(500, 0, function() {
                $(this).remove();
            });
        }

    });

    var is_toggled = false
    $('.navbar-toggler.customized').on('click', function(e) {
        e.preventDefault();
        if (is_toggled == false) {
            $('.sidebar').addClass('active');
            $('.navbar-toggler.customized > span ').removeClass('fa-bars').addClass('fa-times')
            is_toggled = true
        } else {
            $('.sidebar').removeClass('active');
            $('.navbar-toggler.customized > span ').removeClass('fa-times').addClass('fa-bars')
            is_toggled = false
        }



    });

    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.header').addClass("animated slideInDown header-dark"), 1000;
        } else {
            $('.header').removeClass("animated slideInDown header-dark"), 1000;
        }
    });

    /*----------------------------------------------------*/
    // Select2
    /*----------------------------------------------------*/
    $('select').select2({
        minimumResultsForSearch: Infinity,
    });
    /* ----------------------------------------------------------- */
    /* ----------------------------------------------------------- */
    /*  BOOTSTRAP CAROUSEL
		/* ---------

		$("#main-slide").carousel({
			pause: true,
			interval: 100000,
		});

    /* Set Backgrounds
		/* ----------------------------------------------------------- */
    $('.bg-parallax').each(function() {
        var bg = $(this).data('bg');
        $(this).css('background-image', 'url(' + bg + ')');

    });
    $('.set-bgwelcome').each(function() {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');

    });
    $('.set-bg').each(function() {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');

    });

    /*----------------------------------------------------*/
    // Superfish menu.
    /*----------------------------------------------------*/
    $('.sf-menu').superfish();

    /*----------------------------------------------------*/
    // Superslides
    /*----------------------------------------------------*/
    var height = $(window).height();
    $('#home-inner').height(height);

    $('#slides').superslides({
        play: 7000,
        animation: 'slide', // slide
        pagination: false,
        inherit_height_from: '#home-inner',
    });

    /*----------------------------------------------------*/
    // Fancybox
    /*----------------------------------------------------*/
    $("a.popup-link").fancybox();


    /*----------------------------------------------------*/
    // Datapicker
    /*----------------------------------------------------*/
    $(".datepicker").datepicker({
        orientation: "top"
    });





    /*----------------------------------------------------*/
    // Round animation.
    /*----------------------------------------------------*/
    $('.yjsg-round-progress').appear(function() {
        var elem = $(this);
        var animationDelay = elem.data('animation-delay');
        if (animationDelay) {
            setTimeout(function() {
                $(elem).yjsgroundprogress();
            }, animationDelay);
        } else {
            $(elem).yjsgroundprogress();
        }
    });



    /*----------------------------------------------------*/
    // MENU SMOOTH SCROLLING
    /*----------------------------------------------------*/
    $(document).on('click', ".front .navbar_ .navbar-nav a", function(event) {

        //$(".navbar_ .nav a a").removeClass('active');
        //$(this).addClass('active');
        // var headerH = $('#top1').outerHeight();
        var headerH = $('#top-inner').outerHeight();

        if ($(this).attr("href") == "#home") {
            $("html, body").animate({
                scrollTop: 0 + 'px'
                    // scrollTop: $($(this).attr("href")).offset().top + 'px'
            }, {
                duration: 1200,
                easing: "easeInOutExpo"
            });
        } else {
            $("html, body").animate({
                scrollTop: $($(this).attr("href")).offset().top - headerH + 'px'
                    // scrollTop: $($(this).attr("href")).offset().top + 'px'
            }, {
                duration: 1200,
                easing: "easeInOutExpo"
            });
        }

        $(this).blur();


        event.preventDefault();
    });


    /*----------------------------------------------------*/
    // Setting Tab
    /*----------------------------------------------------*/
    var is_active = false
    $('.setting-tab-toggler').on('click', function(event) {
        if (is_active == false) {
            $('.setting-tab').addClass('active');
            is_active = true
        } else {
            $('.setting-tab').removeClass('active');
            is_active = false
        }

    })





})(jQuery);