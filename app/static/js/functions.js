$(document).ready(function() {

	/* Activate H5F */
	H5F.setup(document.getElementsByTagName('form'));

	/* style expired and expiring-soon columns. */
	$('td.expired-forms').each(function() {
        if ($(this).html() != '0') {
            $(this).addClass('expired');
        };
    });
	$('td.expiring-soon-forms').each(function() {
        if ($(this).html() != '0') {
            $(this).addClass('expiring-soon');
        };
    });

  /* When the 'x' of a flashed message is clicked, close the message. */
  $('a.js-close-message').click(function () {
    $(this).parent().hide();
    /* If there are no other visible messages, hide the message container. */
    var visible_messages = $('section.js-message-container div.message').filter(':visible').length;
    if (visible_messages === 0) {
      $('section.js-message-container').hide();
    }
  });
    
    //fade slide effect
    $.fn.slideFadeToggle  = function(speed, easing, callback) {
        return this.animate({opacity: 'toggle', height: 'toggle'}, speed, easing, callback);
    };
        
    //Edit button on role form instances
    /*$('table.form-record td.edit a').css({position:"absolute", right:-4000, opacity:"hide"}).hide();
    $('table.form-record tr').css.hover(
         function () {
           $(this).find('a').animate({right:0, opacity:"show"}, 1000);
         }, 
         function () {
           $(this).find('a').animate({right:-4000, opacity:"hide"}, 1000);
         }
     );*/
    
    
    
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

// Float Label (slightly modified) based on version by Aaron Barker www.codepen.io/aaronbarker/
$(function(){  
  var activeClass = "active",
      showClass = "show";
  
  $("input, select").bind("checkval",function(){
    var label = $(this).prevAll("label");
    if(this.value !== ""){
      label.addClass(showClass);
    } else {
      label.removeClass(showClass);
    }
  })
  .on("keyup",function(){
    $(this).trigger("checkval");
  })
  .on("focus",function(){
    $(this).prevAll("label").addClass("active show");
  })
  .on("blur",function(){
		$(this).prevAll("label").removeClass(activeClass);
  })
  .trigger("checkval");
});


// Helper Label by Chase Whiteside www.codepen.io/chasebank/
$(function(){
  var hideClass = "hide";
  
  $('.helper').hide().addClass('hide');
  
  $("input").bind("checkval",function(){
    var label = $(this).prevAll("label"),
        labelMargin = label.width(),
        helper = $(this).nextAll(".helper");
    if(this.value !== ""){
      helper.css("margin-left",labelMargin+10);
    } else {
      helper.removeAttr('style');
    }
  })
  .on("keyup",function(){
    $(this).trigger("checkval");
  })
  .on("focus",function(){
    $(this).trigger("checkval").nextAll(".helper").removeClass(hideClass);
  })
  .on("blur",function(){
		$(this).nextAll(".helper").removeAttr('style').addClass(hideClass);
  }).trigger("checkval");
});


$("#validate").click(function(){
    $('#fullname').closest('li').addClass('error');
});


});
