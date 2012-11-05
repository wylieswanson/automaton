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
			id = lightObject.prop('id');
			$.ajax({ cache: false, type: "POST", url: "/Lights/Adjust", data: { id: id, action: action, node: node, state: state, device: device } }).done(function( msg ) { });
			// alert( device + node + state );
		});
		$('[group-name="dimmer"]').on('slidestop', function(event){
			var lightObject = $(event.target);
			action = 'dim';
			level = $('#dimmer').val();
			node = lightObject.attr('device-node');
			device = lightObject.attr('device-type');
			id = lightObject.prop('id');
			$.ajax({ cache: false, type: "POST", url: "/Lights/Adjust", data: { id: id, action: action, level: level, node: node, device: device } }).done(function( msg ) { });
			// alert( device + ' ' + node + ' to ' + level );
		});
	});
