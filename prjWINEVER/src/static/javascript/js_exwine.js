$(document).ready(function() {
	
	/*hide elements*/
	$('#info_blocks').hide();
	$('#contact_blocks').hide();
	
	/**/
	$('#info_title').click(function() {
		$('#info_blocks').slideToggle(300,function(){
			toggle_height();
		});
	});
	$('#contact_title').click(function() {
		$('#contact_blocks').slideToggle(300,function(){
			toggle_height();
		});
	});
});

function toggle_height(){
	
	var info_area_heigh = $('#info_area').css('height');
	info_area_heigh = parseInt(info_area_heigh);
	var contact_area_heigh = $('#contact_area').css('height');
	contact_area_heigh = parseInt(contact_area_heigh);
	
	if(info_area_heigh>35 || contact_area_heigh>35){
		$('#logistics_process').animate({paddingTop: '10px'},1000);
		$('#container').animate({top: '285px'},400);
	}
	else{
		$('#logistics_process').animate({paddingTop: '75px'},1000);
		$('#container').animate({top: '340px'},400);
	}
}