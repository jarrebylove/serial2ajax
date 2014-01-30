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

function valueOK(index) {
	var item = $('tr.item')[index];
	var setValue = parseFloat($('input.setValue', item).val());
	var realValue = parseFloat($('input.realValue', item).val());
	var tolerance = parseFloat($('input.tolerance', item).val());
	return Math.abs(setValue - realValue) <= setValue * tolerance / 100.0;
}

function allValueOK() {
	result = true
	$('tr.item').each(function(index) {
		if(valueOK(index) == false)
			result = false;
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
	
	$('table.items tr.item').click(function() {
		selectedItem = selectFromGroup('table.items tr.item', 'active', this)
	});
	
	$('input.measuring').click(function() {
		if((selectedDevice != null) && (selectedItem != null)) {
			var item = $('tr.item')[selectedItem]
			var realValue = $('input.realValue', item)
			realValue.val(devicesValues[selectedDevice]);
			if(valueOK(selectedItem))
				realValue.addClass('realValueOK');
			else
				realValue.removeClass('realValueOK');
			if(allValueOK())
				$('input.done').addClass('show');
			else
				$('input.done').removeClass('show');
		} else {
			alert('Wybierz wage i odmirzany skladnik.')
		}
	});
}
