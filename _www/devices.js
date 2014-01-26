function getDeviceValue(url, callback) {
	$.ajax({
		url: url,
		type: 'GET',
		dataType: 'jsonp',
		success: function(data){
			callback(data);
		}
	});
}

var devicesValues = [];

function updateDeviceValue(url, index) {
	getDeviceValue(url, function(value){
		devicesValues[index] = value;
		$('.value', $('.device')[index]).text(value);
	});
}

function initDevices() {
	$('.device').each(function(index){
		var url = $(this).attr('url');
		setInterval(function(){updateDeviceValue(url, index)}, 1000);
	});
}
