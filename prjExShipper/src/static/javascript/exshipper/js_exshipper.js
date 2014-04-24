/* General functions for ExShipper invoice handler*/

//numeric value validation
function isNumber(evt) {
	//put onkeypress="return isNumber(event)" in <input /> tag
	var charCode = (evt.which) ? evt.which : event.keyCode
	if (charCode > 31 && (charCode < 48 || charCode > 57))
		return false;

	return true;
}

function numberFilter(n) {
	return !isNaN(parseFloat(n) && isFinite(n));
}
// end numeric value validation

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

//add single quote slash
if(!String.prototype.addSlasches){
   String.prototype.addSlashes = function(){
	   return this.replace(/[\\"']/g, '\\$&').replace(/\u0000/g, '\\0');
   }
}
else{
	alert("Warning: String.addSlasches has already been declared by someone else!");
}


// send email
function send_email(e) {
	// form validation

	// end of form validation
}
// end of send email
