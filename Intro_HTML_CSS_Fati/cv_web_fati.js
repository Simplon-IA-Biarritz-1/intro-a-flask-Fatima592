jQuery(document).ready(function($) {
    $('header').click(function() {
        $(this).next().slideToggle('500').css('');
    });
    $('.enter').each().click(function() {
        $('.para').addClass('.active');
    });

});