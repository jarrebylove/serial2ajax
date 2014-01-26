function getMDValue(url, callback) {
	$.ajax({
		url: url,
		type: 'GET',
		dataType: 'jsonp',
		success: function(data){
			callback(data);
		}
	});
}

var MDvalues = [];

function updateMDValue(url, index) {
	getMDValue(url, function(value){
		MDvalues[index] = value;
		$('.value', $('.measurningDevice')[index]).text(value);
	});
}

function initMD() {
	$('.measurningDevice').each(function(index){
		var url = $(this).attr('url');
		setInterval(function(){updateMDValue(url, index)}, 1000);
	});
}
