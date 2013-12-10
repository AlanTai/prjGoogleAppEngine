/*JS*/
console.log('Loaded js_exwine.js')

/*initiation function*/
$(document).ready(function() {
	//hide elements
	$('#container').hide();
	$('#info_blocks').hide();
	$('#contact_blocks').hide();
	
	$('#info_title').click(function() {
		$('#info_blocks').slideToggle(800);
		
		$('html, body').animate({
	        scrollTop: $("#info_title").offset().top
	    }, 800);
	});
	$('#contact_title').click(function() {
		$('#contact_blocks').slideToggle(800);
		

		$('html, body').animate({
	        scrollTop: $("#contact_title").offset().top
	    }, 800);
	});
	//end of "hide elements"
	
	//mousehover opoup txt
	/*$("#main_page, #container_toggle_btn").hover(function(e) {
		
	    $($(this).data("tooltip")).css({
	        left: e.pageX + 1,
	        top: e.pageY + 1
	    }).stop().show(100);
	}, function() {
	    $($(this).data("tooltip")).hide();
	});*/
	//end of mousehover opoup txt
	
	//toggle button for information content
	$('#container_toggle_btn').click(function() {
		$('#container').slideToggle(800,function(){
			var img_src = $('#container_toggle_btn').attr('src');
			if(img_src === '/img/arrow_down_new.png'){
				$('#container_toggle_btn').attr('src','/img/arrow_up_new.png');
			}
			else{
				$('#container_toggle_btn').attr('src','/img/arrow_down_new.png');
			}
			
			toggle_height();
		});
		

		$('html, body').animate({
	        scrollTop: $("#container_toggle_btn").offset().top
	    }, 500);
	});
	//end of "toggle button for information content"
	
	//main page link
	$('#main_page').on('click',go_to_main_page);
	
	//send email
	$('#send_email_btn').on('click',send_email);
	
	//question&answer
	$('#question_answer_main> section#購物問題').css({
		'display':'block'
	});
	$('#question_answer> div:first-child').css({
		'color':'#f00',
		'border-bottom':'solid 1px #f00'
	});
	$('#question_answer> div').on('click',show_question_answer);
	//end of question&answer
	
	
	//save like button
	$('.save_favorite_btn').on('click',handleClick);
});

/*save like record*/
function handleClick(e){
	$.ajax('/info_page_dispatcher',{
		type: 'POST',
		data: {
			fmt: 'json'
		},
		success: showData
	});
}

function showData(data){
	alert(data.submission+'!'+' This winery was saved to your favorite!');
}
/*end of save like record*/

/*send email*/
function send_email(e){
	
	//form validation
	var email_receiver = $.trim($('#send_email_btn').val());
	var email_sender = $.trim($('input#sender').val());
	var email_subject = $.trim($('input#subject').val());
	var email_body = $('textarea#body').val();
	
	if(email_sender === ''){
		alert('Sender field is blank');
		$('input#sender').focus();
		return false;
	}
	if(email_subject === ''){
		alert('Subject field is blank');
		$('input#subject').focus();
		return false;
	}
	if(email_body === ''){
		alert('Body field is blank');
		$('textarea#body').focus();
		return false;
	}
	
	//end of form validation
	
	$.ajax('/contact_page_dispatcher',{
		type: 'POST',
		data: {
			fmt: 'json',
			receiver_address: email_sender,
			sender_address: email_receiver,
			subject: email_subject,
			body: email_body
		},
		success: show_message
	});
}

function show_message(data){
	alert(data.email_confirmation);
	
	//clean fields
	$('input#sender').val('');
	$('input#subject').val('');
	$('textarea#body').val('');
}
/*end of send email*/

//question & answer
function show_question_answer(){
	var section_id = $(this).attr('title');
	$('#question_answer> div').css({
		'color':'#644901',
		'border-bottom':'solid 1px transparent'
	});
	$('#question_answer_main> section').css({
		'display':'none'
	});
	$('#question_answer_main> section#'+section_id).css({
		'display':'block'
	});
	$(this).css({
		'color':'#f00',
		'border-bottom':'solid 1px #f00'
	});
}
//end of question & answer

//go to main page
function go_to_main_page(){
	document.location.href='http://www.exwine-tw.appspot.com/exwine';
}
//end go to main page

//toggle elements' height
function toggle_height(){
	
	var info_area_heigh = $('#info_area').css('height');
	info_area_heigh = parseInt(info_area_heigh);
	var contact_area_heigh = $('#contact_area').css('height');
	contact_area_heigh = parseInt(contact_area_heigh);
	var container_heigh = $('#container').css('height');
	container_heigh = parseInt(container_heigh);
	var container_display = $('#container').css('display');
	
	var meta_page_tag = $('meta[name=page_tag]');
	var page_tag = meta_page_tag.attr('content');
	
	if(page_tag === 'link_page'){
		/*if(info_area_heigh>35 || contact_area_heigh>35){
			$('#logistics_process').animate({paddingTop: '10px'},100);
		}
		else{
			$('#logistics_process').animate({paddingTop: '20px'},100);
		}*/
	}
	else{
		if((container_display === 'block') || (info_area_heigh>35 || contact_area_heigh>35)){
			$('#logistics_process').animate({paddingTop: '10px'},1000);
			$('#main_container').animate({top: '285px'},800);
		}
		else{
			$('#logistics_process').animate({paddingTop: '85px'},1000);
			$('#main_container').animate({top: '350px'},800);
		}
	}
}