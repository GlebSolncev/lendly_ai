$(document).ready(function() {
    "use strict";

    var window_width = $(window).width(),
        window_height = window.innerHeight,
        header_height = $(".default-header").height(),
        header_height_static = $(".site-header.static").outerHeight(),
        fitscreen = window_height - header_height;

    $(".fullscreen").css("height", window_height);
    $(".fitscreen").css("height", fitscreen);

    if (document.getElementById("default-select")) {
        $('select').niceSelect();
    };

    //------- Lightbox js --------//

    $('.img-pop-up').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });

    $('.play-btn').magnificPopup({
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });

    //------- Initiate superfish on nav menu --------//

    $('.nav-menu').superfish({
        animation: {
            opacity: 'show'
        },
        speed: 400
    });

    //------- Accordion  js --------//  

    jQuery(document).ready(function($) {

        if (document.getElementById("accordion") && document.getElementById("accordion2")) {

            var accordion_1 = new Accordion(document.getElementById("accordion"), {
                collapsible: false,
                slideDuration: 600
            });
            var accordion_2 = new Accordion(document.getElementById("accordion2"), {
                multiple: true,
                slideDuration: 600
            });
        }
    });

    /* ---------------------------------------------
     accordion
     --------------------------------------------- */

    var allPanels = $(".accordion > dd").hide();
    allPanels.first().slideDown("easeOutExpo");
    $(".accordion").each(function() {
        $(this).find("dt > a").first().addClass("active").parent().next().css({
            display: "block"
        });
    });

    $(document).on('click', '.accordion > dt > a', function(e) {
        var current = $(this).parent().next("dd");
        $(this).parents(".accordion").find("dt > a").removeClass("active");
        $(this).addClass("active");
        $(this).parents(".accordion").find("dd").slideUp("easeInExpo");
        $(this).parent().next().slideDown("easeOutExpo");

        return false;

    });

    /* ---------------------------------------------
     toggle accordion
     --------------------------------------------- */

    var allToggles = $(".toggle > dd").hide();
    allPanels.first().slideDown("easeOutExpo");
    $(".toggle").each(function() {
        $(this).find("dt > a").first().addClass("active").parent().next().css({
            display: "block"
        });
    });

    $(document).on('click', '.toggle > dt > a', function(e) {    
        if ($(this).hasClass("active")) {
            $(this).parent().next().slideUp("easeOutExpo");
            $(this).removeClass("active");

        } else {
            var current = $(this).parent().next("dd");
            $(this).addClass("active");
            $(this).parent().next().slideDown("easeOutExpo");
        }

        return false;
    });

    //------- Tabs Js --------//  

    $('#horizontalTab').jqTabs({
        direction: 'horizontal',
        duration: 200
    });

    $('#horizontalTab2').jqTabs({
        direction: 'horizontal',
        duration: 200
    });

    jQuery(document).ready(function($) {
        // Get current path and find target link
        var path = window.location.pathname.split("/").pop();

        // Account for home page with empty path
        if (path === '') {
            path = 'index.php';
        }

        var target = $('nav a[href="' + path + '"]');
        // Add active class to target link
        target.addClass('menu-active');
    });

    $(document).ready(function() {
        if ($('.menu-has-children ul>li a').hasClass('menu-active')) {
            $('.menu-active').closest("ul").parentsUntil("a").addClass('parent-active');
        }
    });

    //------- Login and register form toggle --------//  

    $(document).ready(function(){
        $(document).on('click','.hs-btn',function(e){
            $( ".forms" ).toggle();
        });
    });


    //------- Mobile Navigation --------//  

    if ($('#nav-menu-container').length) {
        var $mobile_nav = $('#nav-menu-container').clone().prop({
            id: 'mobile-nav'
        });
        $mobile_nav.find('> ul').attr({
            'class': '',
            'id': ''
        });
        $('body').append($mobile_nav);
        $('body').prepend('<button type="button" id="mobile-nav-toggle"><i class="lnr lnr-menu"></i></button>');
        $('body').append('<div id="mobile-body-overly"></div>');
        $('#mobile-nav').find('.menu-has-children').prepend('<i class="lnr lnr-chevron-down"></i>');

        $(document).on('click', '.menu-has-children i', function(e) {
            $(this).next().toggleClass('menu-item-active');
            $(this).nextAll('ul').eq(0).slideToggle();
            $(this).toggleClass("lnr-chevron-up lnr-chevron-down");
        });

        $(document).on('click', '#mobile-nav-toggle', function(e) {
            $('body').toggleClass('mobile-nav-active');
            $('#mobile-nav-toggle i').toggleClass('lnr-cross lnr-menu');
            $('#mobile-body-overly').toggle();
        });

        $(document).on('click',function(e){
            var container = $("#mobile-nav, #mobile-nav-toggle");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                if ($('body').hasClass('mobile-nav-active')) {
                    $('body').removeClass('mobile-nav-active');
                    $('#mobile-nav-toggle i').toggleClass('lnr-menu');
                    $('#mobile-body-overly').fadeOut();
                }
            }else{
                $('#mobile-nav-toggle i').addClass('lnr-cross');
            }
        });    

    } else if ($("#mobile-nav, #mobile-nav-toggle").length) {
        $("#mobile-nav, #mobile-nav-toggle").hide();
    }

    // Smooth scroll for the menu and links with .scrollto classes
    $('.nav-menu a, #mobile-nav a, .scrollto').on('click', function() {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            var target = $(this.hash);
            if (target.length) {
                var top_space = 0;

                if ($('#header').length) {
                    top_space = $('#header').outerHeight();

                    if (!$('#header').hasClass('header-fixed')) {
                        top_space = top_space;
                    }
                }

                // $('html, body').animate({
                //     scrollTop: target.offset().top - top_space
                // }, 500, 'easeOutExpo');

                window.scrollTo({
                    top: target.offset().top - top_space,
                    behavior: 'smooth'
                });


                if ($(this).parents('.nav-menu').length) {
                    $('.nav-menu .menu-active').removeClass('menu-active');
                    $(this).closest('li').addClass('menu-active');
                }

                if ($('body').hasClass('mobile-nav-active')) {
                    $('body').removeClass('mobile-nav-active');
                    $('#mobile-nav-toggle i').toggleClass('lnr-menu');
                    $('#mobile-body-overly').fadeOut();
                }
                return false;
            }
        }
    });

    $(document).ready(function() {

        $('html, body').hide();

        if (window.location.hash) {

            setTimeout(function() {

                $('html, body').scrollTop(0).show();

                $('html, body').animate({

                    scrollTop: $(window.location.hash).offset().top - 68

                }, 1000)

            }, 0);

        } else {

            $('html, body').show();

        }

    });

    //------- Header scroll class js --------//  



    $(".scroll-down").on('click',function() {
        $('html,body').animate({
            scrollTop: $(".feature-area").offset().top},
            'slow');
        return false;
    });

    
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#header').addClass('header-scrolled');
        } else {
            $('#header').removeClass('header-scrolled');
        }
    });

    //------- Owl Carusel js --------//   

    $('.active-slider-carusel').owlCarousel({
        items: 1,
        loop: true,
        margin: 30,
        autoplayTimeout: 4500,
        autoplayHoverPause: true,        
        smartSpeed: 600,
        autoplay: true,
        animateOut: 'fadeOut',
        dots: true,
    });

    $('.active-review-carusel').owlCarousel({
        items: 3,
        loop: true,
        margin: 30,
        autoplayTimeout: 4000,
        autoplayHoverPause: true,
        smartSpeed: 800,
        autoplay: true,
        nav: true,
        navText: ["<i class='ti-shift-left'></i>", "<i class='ti-shift-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            992: {
                items: 3,
            }
        }
    });

    $('.active-latest-post-carusel').owlCarousel({
        items: 2,
        loop: true,
        margin: 30,
        autoplayTimeout: 4000,
        autoplayHoverPause: true,
        smartSpeed: 800,
        autoplay: true,
        dots: true,
        responsive: {
            0: {
                items: 1,
            },
            992: {
                items: 2,
            }
        }
    });

    $('.active-popular-post-carusel').owlCarousel({
        items: 4,
        loop: true,
        margin: 30,
        autoplay: true,
        autoplayTimeout: 4000,
        autoplayHoverPause: true,
        smartSpeed: 800,
        dots: true,
        responsive: {
            0: {
                items: 1,
            },
            768: {
                items: 2,
            },
            991: {
                items: 3,
            },
            1024: {
                items: 3,
            },
            1025: {
                items: 4,
            }
        }
    });

    $('.active-latest-widget-carusel').owlCarousel({
        items: 1,
        loop: true,
        margin: 30,
        autoplayTimeout: 4500,
        autoplayHoverPause: true,
        smartSpeed: 600,
        autoplay: true,
        dots: true,
    });


     //------- Map js  --------//   

            // When the window has finished loading create our google map below

            if(document.getElementById("map")){
            
            google.maps.event.addDomListener(window, 'load', init);
        
            function init() {
                // Basic options for a simple Google Map
                // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
                var mapOptions = {
                    // How zoomed in you want the map to start at (always required)
                    zoom: 11,

                    // The latitude and longitude to center the map (always required)
                    center: new google.maps.LatLng(40.6700, -73.9400), // New York

                    // How you would like to style the map. 
                    // This is where you would paste any style found on Snazzy Maps.
                    styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
                };

                // Get the HTML DOM element that will contain your map 
                // We are using a div with id="map" seen below in the <body>
                var mapElement = document.getElementById('map');

                // Create the Google Map using our element and options defined above
                var map = new google.maps.Map(mapElement, mapOptions);

                // Let's also add a marker while we're at it
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(40.6700, -73.9400),
                    map: map,
                    title: 'Snazzy!'
                });
            }
    }

    //------- MailChimp js  --------//   

    $(document).ready(function() {
        $('#mc_embed_signup').find('form').ajaxChimp();
        $('#footer_mc_embed_signup').find('form').ajaxChimp();
    });

});