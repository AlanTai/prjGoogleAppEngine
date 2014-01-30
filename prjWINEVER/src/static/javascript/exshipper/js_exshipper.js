/*functions for exshipper invoice handler*/

//numeric value validation
function isNumber(evt) {
	var charCode = (evt.which) ? evt.which : event.keyCode
	if (charCode > 31 && (charCode < 48 || charCode > 57))
		return false;

	return true;
}

function numberFilter(n) {
	return !isNaN(parseFloat(n) && isFinite(n));
}

// end numeric value validation

// add new items
var info_array = [];

function Add() {
	var yamato_tr_number = $('#id_yamato_tr_number').val();
	var reference_number = $('#id_reference_number').val();
	var shipper = $('#id_shipper').val();
	var consignee_en = $('#id_consignee_en').val();
	var consignee_ch = $('#id_consignee_ch').val();
	var address = $('#id_address').val();
	var phone_number = $('#id_phone_number').val();
	var size_length = $('#id_length').val();
	var size_width = $('#id_width').val();
	var size_height = $('#id_height').val();
	var weight = $('#id_weight').val();

	// check information
	if (yamato_tr_number === '') {
		$('#id_yamato_tr_number').focus();
		return true;
	} else {
		yamato_tr_number = yamato_tr_number.trim();
	}
	if (reference_number === '') {
		$('#id_reference_number').focus();
		return true;
	} else {
		reference_number = reference_number.trim();
	}
	if (shipper === '') {
		$('#id_shipper').focus();
		return true;
	} else {
		shipper = shipper.trim();
	}

	if (consignee_en === '') {
		$('#id_consignee_en').focus();
		return true;
	} else {
		consignee_en = consignee_en.trim();
	}

	if (consignee_ch === '') {
		$('#id_consignee_ch').focus();
		return true;
	} else {
		consignee_ch = consignee_ch.trim();
	}

	if (address === '') {
		$('#id_address').focus();
		return true;
	} else {
		address = address.trim();
	}
	if (phone_number === '') {
		$('#id_phone_number').focus();
		return true;
	} else {
		phone_number = phone_number.trim();
	}

	if (!numberFilter(size_length)) {
		alert('Please type in a number for the length!');
		$('#id_length').focus();
		return true;
	}
	if (!numberFilter(size_width)) {
		alert('Please type in a number for the width!');
		$('#id_width').focus();
		return true;
	}
	if (!numberFilter(size_height)) {
		alert('Please type in a number for the height!');
		$('#id_height').focus();
		return true;
	}
	if (!numberFilter(weight)) {
		alert('Please type in a number for the weight!');
		$('#id_weight').focus();
		return true;
	}
	// end of checking information

	// check yamato tracking number
	var i = info_array.length;
	while (i > 0) {
		if (info_array[i - 1].tr_number === yamato_tr_number) {
			alert('This Yamato Tracking Number Already Exist!');
			$('#id_yamato_tr_number').focus();
			return true;
		}
		if (info_array[i - 1].ref_number === reference_number) {
			alert('This Reference Number Already Exist!');
			$('#id_reference_number').focus();
			return true;
		}
		--i;
	}
	info_array.push({
		'tr_number' : yamato_tr_number,
		'ref_number' : reference_number
	});
	// end of check yamato tracking number

	
	//add the info to datastore
	$.ajax('/exshipper_invoice_info_handler',{
		type : 'POST',
		data : {
			fmt : 'json',
			valid_yamato_tr_number : yamato_tr_number,
			valid_ref_number : reference_number,
			valid_shipper : shipper,
			valid_consignee_en : consignee_en,
			valid_consignee_ch : consignee_ch,
			valid_address : address,
			valid_phone_number : phone_number,
			valid_size_length : size_length,
			valid_size_width : size_width,
			valid_size_height : size_height,
			valid_weight : weight
		},
		success : showReturnMsg,
		statusCode : {
			400: function(){
				alert('400 status code! user-side error');
			},
			500: function(){
				alert('500 status code! server-side error')
			}
		}
	});
	//end of add the info to datastore
	
	//append type-in info to html element
	$('#added_info')
			.append(
					'<form name="'
							+ yamato_tr_number
							+ '">'
							+ '<input type="button" value="Remove" onclick="selectOrRemove(this.form)" style="width: 90px; height: 40px; display: inline-block; margin: 20px; 5px;">'
							+ '<div style="width: 1000px; display: inline-block; margin: auto 5px;">'
							+ '<p style="display: inline-block; margin: 0px 5px;"> Yamato Tracking Number: '
							+ yamato_tr_number
							+ '</p>'
							+ '<p style="display: inline-block; margin: 0px 5px;"> Reference Number: '
							+ reference_number
							+ '</p>'
							+ '<p style="display: inline-block; margin: 0px 5px;"> Shipper: '
							+ shipper
							+ '</p>'
							+ '<p style="display: inline-block; margin: 0px 5px;"> Consignee (English): '
							+ consignee_en
							+ '</p>'
							+ '<p style="display: inline-block; margin: 0px 5px;"> Consignee (Chinese): '
							+ consignee_ch
							+ '</p>'
							+ '<p style="display: inline-block; margin: 0px 5px;"> Address: '
							+ address
							+ '</p>'
							+ '<p style="display: inline-block; margin: 0px 5px;"> Phone Number: '
							+ phone_number + '</p>' + '</div>' + '<br></form>');
	// change color
	$('#added_info> form:even').css('background-color', '#dedede');
	$('#added_info> form:odd').css('background-color', '#f9f9f9');
	// end change color

	$('#added_labels')
			.append(
					'<form id="label_'
							+ yamato_tr_number
							+ '" style="border: 1px solid; width: 300px; margin: 5px 5px; padding: 2px 5px; display:inline-block; text-align: left;">'
							+ '<p style="display: block; margin: 0px auto;"> 寄件者: '
							+ shipper
							+ '</p>'
							+ '<p style="display: block; margin: 0px auto;"> 地址: 1941 W Ave. 104th, San Leandro, CA 94577</p>'
							+ '<p style="display: block; margin: 0px auto;"> 電話: (510)351-8903</p>'
							+ '<hr>'
							+ '<p style="display: block; margin: 0px auto;"> 收件者: '
							+ consignee_ch
							+ '</p>'
							+ '<p style="display: block; margin: 0px auto;"> 地址: '
							+ address
							+ '</p>'
							+ '<p style="display: block; margin: 0px auto;"> 電話: '
							+ phone_number
							+ '</p>'
							+ '<hr>'
							+ '<p style="position: relative; top: 0px; left: 0px; border: 1px solid; text-align: center; padding: 2px 5px; margin: 2px 5px; display: inline-block;">易碎</p>'
							+ '<p style="position: relative; top: 0px; left: 0px; border: 1px solid; text-align: center; padding: 2px 5px; margin: 2px 5px; display: inline-block;">'+ weight +' (kg)</p>'
							+ '<p style="position: relative; top: 0px; left: 0px; border: 1px solid; text-align: center; padding: 2px 5px; margin: 2px 5px; display: inline-block;">Ref. NO. '+ reference_number +'</p>'
							+ '<hr>'
							+ '<div class="barcode_title" style="display: block; margin: 2px auto; text-align:center;">Yamato Tracking Number</div>'
							+ '<div class="barcode" id="barcode_'
							+ yamato_tr_number
							+ '" style="margin: 2px auto; text-align:center;"></div>'
							+ '</form>');

	$('#added_labels> form[id="label_' + yamato_tr_number + '"]').find(
			'div#barcode_' + yamato_tr_number).barcode(yamato_tr_number,
			'code128', {
				barWidth : 2,
				barHeight : 45,
				fontSize : 16
			});

	$('#check_list')
			.append(
					'<form id="check_list_'
							+ yamato_tr_number
							+ '" style="width: 800px; margin: 1px auto; padding: 5px auto; display:inline-block">'
							+ '<input type="checkbox" disabled="true" style="height: 100%; width: 20px; display: inline-block; margin: auto 10px;">'
							+ '<div style="width:600px; display: inline-block; text-align: left;">'
							+ '<p style="display: inline-block; margin: auto 5px; height: 30px; padding:auto 5px; vertical-align: middle; text-align: left;">Yamato Tracking Number: '
							+ yamato_tr_number
							+ '</p>'
							+ '<p style="display: inline-block; margin: auto 5px; height: 30px; padding:auto 5px; vertical-align: middle; text-align: left;"> Reference Number: '
							+ reference_number + '</p>' + '</div>'
							+ '<br></form>');
}

function showReturnMsg(return_msg){
	alert(return_msg.invoice_info_submission);
}

function selectOrRemove(elem) {
	var select_status = $(elem).find('input').attr('value');
	var elem_name = $(elem).attr('name');
	if (select_status === 'Remove') {
		$(elem).find('input').val('Select');
		$('#added_labels> form[id="label_' + elem_name + '"]').css({
			'display' : 'none'
		});
		$('#check_list> form[id="check_list_' + elem_name + '"]').css({
			'display' : 'none'
		});
	} else {
		$(elem).find('input').val('Remove');
		$('#added_labels> form[id="label_' + elem_name + '"]').css({
			'display' : 'inline-block'
		});
		$('#check_list> form[id="check_list_' + elem_name + '"]').css({
			'display' : 'inline-block'
		});
	}

	/* remove element */
	// $(elem).remove();
}

/**/
// convert content to image
function convertContentToImage() {
	$src = $('#added_labels');
	var divContent = $('#printed_labels').append($src.clone());
	divContent.width($src.width());
	divContent.height($src.height());

	html2canvas(divContent, {
		onrendered : function(canvas) {
			divContent.empty();
			var imgURL = canvas.toDataURL();
			var img = new Image();
			$('#printed_labels').append(img);
			img.src = imgURL;
		}
	});
}

// main function of printing
function PrintElem(elem, title) {
	Popup($(elem).html(), title);
}

function Popup(data, page_title) {
	var mywindow = window.open("", 'my div', 'toolbar = no, status = no');
	mywindow.document.write('<html><head><title>' + page_title + '</title>');
	mywindow.document
			.write('<link type="text/css" rel="stylesheet" media="print" href="/css/exshipper/css_exshipper.css"/>');
	mywindow.document.write('</head><body>');
	mywindow.document.write(data);
	mywindow.document.write('</body></html>');

	mywindow.document.close();
	mywindow.focus();
	mywindow.print();
	mywindow.close();
	return true;
}
// end main function of printing

// test function of printing div iwth jquery plug-in
function printDiv(myDiv) {
	$(myDiv).jqprint();
}

// test function of printing
function printContent(div_id) {
	var DocumentContainer = document.getElementById(div_id);
	var html = '<html><head>' + '</head><body">' + DocumentContainer.innerHTML
			+ '</body></html>';

	var WindowObject = window.open("", "PrintWindow",
			"toolbars=no,scrollbars=yes,status=no,resizable=yes");
	WindowObject.document.writeln(html);
	WindowObject.document.close();
	WindowObject.focus();
	WindowObject.print();
	WindowObject.close();
}
// end

// test function of printing text
function displayHTML(form) {
	var inf = form.shipper.value + '\n' + form.consignee_en.value + '\n'
			+ form.consignee_ch.value;
	win = window.open(", ", 'popup', 'toolbar = no, status = no');
	win.document.write('<title> Label Layout </title>');
	win.document
			.write('<h1>ExShipper Test:</h1><br style="height:1000px;"><hr>'
					+ inf + '<hr><p>End</p>');
}

// send email
function send_email(e) {
	// form validation

	// end of form validation
}
// end of send email
