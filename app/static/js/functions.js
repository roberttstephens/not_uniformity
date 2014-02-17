$(document).ready(function() {
	
	/* Activate H5F */
	H5F.setup(document.getElementsByTagName('form'));

	/* style expired and expiring-soon columns. */
	$('td.expired:not(:empty)').addClass('red-cell');
	$('td.expiring-soon:not(:empty)').addClass('yellow-cell');
   
});
