$.ajaxSetup ({ cache: false });

$("#remotebuttons a").live("tap", function(){ 
	$.ajax({
		type: "POST", url: "/TV/Key",
		data: { key: $(this).attr('href').substr(1) }
	}).done(function( msg ) {
		// alert( "Data Saved: " + msg );
	});
});


$(document).live('pageinit', function(){
		// alert('hi')
		$('[group-name="switch_toggle"]').on( 'slidestop', function(event){
			var lightObject = $(event.target);
			action = 'flip';
			state = $('#switch').val();
			node = lightObject.attr('device-node');
			device = lightObject.attr('device-type');
			name = lightObject.attr('device-name');
			locale = lightObject.attr('device-location');
			id = lightObject.prop('id');
			$.ajax({ cache: false, type: "POST", url: "/zwave/update", data: { id: id, action: action, node: node, name: name, locale: locale, state: state, device: device } }).done(function( msg ) { });
			// alert( device + node + state );
		});
		$('[group-name="dimmer"]').on('slidestop', function(event){
			var lightObject = $(event.target);
			action = 'dim';
			level = $('#dimmer').val();
			node = lightObject.attr('device-node');
			device = lightObject.attr('device-type');
			name = lightObject.attr('device-name');
			locale = lightObject.attr('device-location');
			id = lightObject.prop('id');
			$.ajax({ cache: false, type: "POST", url: "/zwave/update", data: { id: id, action: action, level: level, node: node, name: name, locale: locale, device: device } }).done(function( msg ) { });
			// alert( device + ' ' + node + ' to ' + level );
		});
	});
