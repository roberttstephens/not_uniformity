$(document).ready(function() {

	/* Activate H5F */
	H5F.setup(document.getElementsByTagName('form'));

	/* style expired and expiring-soon columns. */
	$('td.expired-forms:not(:empty)').addClass('expired');
	$('td.expiring-soon-forms:not(:empty)').addClass('expiring-soon');

  /* When the 'x' of a flashed message is clicked, close the message. */
  $('a.js-close-message').click(function () {
    $(this).parent().hide();
    /* If there are no other visible messages, hide the message container. */
    var visible_messages = $('section.js-message-container div.message').filter(':visible').length;
    if (visible_messages === 0) {
      $('section.js-message-container').hide();
    }
  });
});




function eqColumn(){
//if ($(window).width() > 0){
    var serviceWrap = $(".service-wrap");
    //reset the height to auto
    serviceWrap.css("height", "auto");
    var biggest = 0;
    $(serviceWrap).each(function(){
        if ($(this).height() > biggest){
            biggest = $(this).height();
         }
    });
    serviceWrap.css("height", biggest);
}
//}

$(window).on("load resize", eqColumn);