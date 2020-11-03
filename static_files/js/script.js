$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });
  
  $('.back-to-top').click(function() {
    $('html, body').animate({ scrollTop: 0 }, "slow");
    return false;
  });

  (function($) {
    /*------------------
      Navigation
    --------------------*/
    $('.main-menu').slicknav({
      prependTo:'.main-navbar .container',
      closedSymbol: '<i class="flaticon-right-arrow"></i>',
      openedSymbol: '<i class="flaticon-down-arrow"></i>'
    });
  
  
    /*------------------
      ScrollBar
    --------------------*/
    $(".cart-table-warp, .product-thumbs").niceScroll({
      cursorborder:"",
      cursorcolor:"#afafaf",
      boxzoom:false
    });
  
  
    /*------------------
      Category menu
    --------------------*/
    $('.category-menu > li').hover( function(e) {
      $(this).addClass('active');
      e.preventDefault();
    });
    $('.category-menu').mouseleave( function(e) {
      $('.category-menu li').removeClass('active');
      e.preventDefault();
    });
  
  
 
  
  
  