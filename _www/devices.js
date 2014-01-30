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

function measuringOn() {
	$($('table.items tr.item')[selectedItem]).removeClass('completed');
	measuring = true;
	$('input.measuring').val('Stop');
}

function measuringOff() {
	measuring = false;
	$('input.measuring').val('Odmierzaj');
}

function onDeviceValueUpdate(index, value) {
	devicesValues[index] = value;
	$('.value', $('.device')[index]).text(value);
	if((selectedDevice != null) && (selectedItem != null) && measuring) {
		var item = $('tr.item')[selectedItem]
		var realValue = $('input.realValue', item)
		realValue.val(devicesValues[selectedDevice]);
		if(valueOk(selectedItem)) {
			$(item).addClass('realValueOK');
			$('input.measuring').val('Ok');
		} else {
			$(item).removeClass('realValueOK');
			$('input.measuring').val('Stop');
		}
	}
}

function updateDeviceValue(url, index) {
	getDeviceValue(url, function(value) {
		onDeviceValueUpdate(index, value);
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

function valueOk(index) {
	var item = $('tr.item')[index];
	var setValue = parseFloat($('input.setValue', item).val());
	var realValue = parseFloat($('input.realValue', item).val());
	var tolerance = parseFloat($('input.tolerance', item).val());
	return Math.abs(setValue - realValue) <= setValue * tolerance / 100.0;
}

function allValueOkAndCompleted() {
	result = true
	$('tr.item').each(function(index) {
		if(valueOk(index) == false)
			result = false;
		if($(this).hasClass('completed') == false)
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
		measuringOff();
		selectedDevice = selectFromGroup('.device', 'deviceActive', this)
	});
	
	$('table.items tr.item').click(function() {
		measuringOff();
		selectedItem = selectFromGroup('table.items tr.item', 'active', this)
	});
	$('input.measuring').click(function(event) {
		if((selectedDevice != null) && (selectedItem != null)) {
			if (measuring == false) {
				measuringOn();
			} else {
				measuringOff();
				if(valueOk(selectedItem)) {
					$($('table.items tr.item')[selectedItem]).addClass('completed');
				}
			}
			if(allValueOkAndCompleted()) {
				$('input.done').addClass('show');
			} else {
				$('input.done').removeClass('show');
			}
		} else {
			alert('Wybierz wage.')
		}
		event.stopPropagation();
	});
}
