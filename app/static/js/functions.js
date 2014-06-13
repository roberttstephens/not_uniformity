$(document).ready(function() {

	/* Activate H5F */
	H5F.setup(document.getElementsByTagName('form'));

	/* style expired and expiring-soon columns. */
	$('td.expired:not(:empty)').addClass('red-cell');
	$('td.expiring-soon:not(:empty)').addClass('yellow-cell');

  /* When the 'x' of a flashed message is clicked, close the message. */
  $('a.js-close-message').click(function () {
    $(this).parent().hide();
  });
});
