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
var selectedDevice = null;
var selectedItem = null;
var measuring = false;

function updateDeviceValue(url, index) {
	getDeviceValue(url, function(value) {
		devicesValues[index] = value;
		$('.value', $('.device')[index]).text(value);
	});
	setTimeout(function(){updateDeviceValue(url, index)}, 1000);

}


function selectFromGroup(selector, activeClass, clickedDevice) {
	var result;
	$(selector).each(function(index) {
		if($(clickedDevice)[0] == $(this)[0]) {
			if($(this).hasClass(activeClass)) {
				$(this).removeClass(activeClass);
				result = null;
			} else {
				$(this).addClass(activeClass);
				result = index;
			}
		} else {
			$(this).removeClass(activeClass);
		}
	});
	return result;
}

function initDevices() {
	$('.device').each(function(index) {
		var url = $(this).attr('url');
		updateDeviceValue(url, index);
	});
	
	$('.device').click(function() {
		selectedDevice = selectFromGroup('.device', 'deviceActive', this)
	});
	
	$('.item').click(function() {
		measuring = false;
		selectedItem = selectFromGroup('.item', 'itemActive', this)
	});
	
	$('input.measuring').click(function() {
		if((selectedDevice != null) && (selectedItem != null))
			var item = $('.item')[selectedItem]
			var setValue = $('.setValue', item)
			var realValue = $('.realValue', item)
			realValue.val(devicesValues[selectedDevice]);
			if (Math.abs(parseFloat(setValue.val()) - parseFloat(realValue.val())) <= 0.5)
				realValue.addClass('realValueOK');
			else
				realValue.removeClass('realValueOK');
	});
}
