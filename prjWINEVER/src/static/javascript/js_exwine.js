$(document).ready(function() {
	
	/*hide elements*/
	$('#info_blocks').hide();
	$('#contact_blocks').hide();
	
	/**/
	$('#info_title').click(function() {
		$('#info_blocks').slideToggle(500);
	});
	$('#contact_title').click(function() {
		$('#contact_blocks').slideToggle(500);
	});
});