$(document).ready(function () {

    /* Activate H5F */
    H5F.setup(document.getElementsByTagName('form'));

    /* style expired and expiring-soon columns. */
    $('td.expired-forms').each(function () {
        if ($(this).html() != '0') {
            $(this).addClass('expired');
        }
    });
    $('td.expiring-soon-forms').each(function () {
        if ($(this).html() != '0') {
            $(this).addClass('expiring-soon');
        }
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




    function eqColumn() {
        //if ($(window).width() > 0){
        var serviceWrap = $(".service-wrap"),
            biggest = 0;
        //reset the height to auto
        serviceWrap.css("height", "auto");
        
        $(serviceWrap).each(function () {
            if ($(this).height() > biggest) {
                biggest = $(this).height();
            }
        });
        serviceWrap.css("height", biggest);
    }
    //}

    $(window).on("load resize", eqColumn);




    $("#validate").click(function () {
        $('#fullname').closest('li').addClass('error');
    });




    $.fn.slideFadeToggle = function (speed, easing, callback) {
        return this.animate({
            opacity: 'toggle',
            height: 'toggle',
            padding: 'toggle'
        }, speed, easing, callback);
    };


    
    $('#add-new-instance-form tbody').hide();

    $('a[href="#add-instance"]').click(function () {
        $('#add-new-instance-form tbody').slideFadeToggle();
        $('a[href="#add-instance"]').fadeToggle();
    });

    $('.add-instance .add-form-toggle').click(function () {
        $('#add-new-instance-form tbody').slideFadeToggle();
        $('a[href="#add-instance"]').fadeToggle();
    });
    
    
    
    $('div.edit-form').hide();
    var cancelButtonWidth = $('.cancel-edit-form-button').outerWidth();
    $('td:not(.add-instance) .cancel-edit-form-button').hide();

    $('.edit-toggle').click(function () {
        var editToggle = $(this),
            allEditToggles = $('.edit-toggle'),
            editThisForm = $(this).next('div.edit-form'),
            editButton = $(this).find('.edit-form-button'),
            editButtonWidth = $(this).find('.edit-form-button').outerWidth(),
            cancelButton = $(this).find('.cancel-edit-form-button');

        // Untoggle everything except this one
        $('.edit-form[toggled="1"]').not(editThisForm).prevAll('.edit-toggle').children('.edit-form-button, .cancel-edit-form-button').fadeToggle();
        $('.edit-form[toggled="1"]').not(editThisForm).removeAttr('toggled').slideFadeToggle();

        if ($(editThisForm).attr('toggled')) {
            // If this one is toggled, untoggle it
            $(editThisForm).removeAttr('toggled').slideFadeToggle();
            $(editButton).fadeToggle();
            $(cancelButton).fadeToggle();
        } else {
            // If this one isn't toggled, toggle it
            $(editThisForm).attr('toggled', '1').slideFadeToggle();
            $(editButton).fadeToggle();
            $(cancelButton).fadeToggle();
        }
    });


    $('.edit-form .checkbox :checkbox, .add-form-instance .checkbox :checkbox').each(function () {
        var receivedDateWrap = $(this).closest('label').siblings('.received-date'),
            receivedDateInput = $(receivedDateWrap).find('input');

        if (this.checked) {
            $(receivedDateWrap).removeClass('disabled');
            $(receivedDateInput).prop('disabled', false);
        } else {
            $(receivedDateWrap).addClass('disabled');
            $(receivedDateInput).val("").prop('disabled', true);
        }

        $(this).change(function () {

            if (this.checked) {
                $(receivedDateWrap).removeClass('disabled');
                $(receivedDateInput).prop('disabled', false);
            } else {
                $(receivedDateWrap).addClass('disabled');
                $(receivedDateInput).val("").prop('disabled', true);
            }
        });
    });
    
    
    
    
    // Login form float labels
    // Float label if input already has value
    $('.login-form input').each(function () {
        var text_value = $(this).val();
        if (text_value != '') {
            $(this).parent().addClass('float-label');
        }
    });
    
    $('.login-form input[type=text], .login-form input[type=password]').focus(function () {
        $(this).parent().addClass('float-label');
    });
    
    $('.login-form input[type=text], .login-form input[type=password]').blur(function () {
        if ($(this).val() == '') { $(this).parent().removeClass('float-label'); }
    });
    
    // Login form password hide/shoe
    $('input[type="password"]').after('<span class="password-toggle">Show<i class="fa fa-eye"></i></span>');

    $('.password-toggle').on('click', function () {
        var $this = $(this),
            $password = $this.prev('input');

        ('password' == $password.attr('type')) ? $password.attr('type', 'text') : $password.attr('type', 'password');
        ('Hide' == $this.text()) ? $this.html('Show<i class="fa fa-eye"></i>') : $this.html('Hide<i class="fa fa-eye-slash"></i>');
        $password.focus();
    });


});