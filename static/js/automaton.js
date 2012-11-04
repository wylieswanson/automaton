$.ajaxSetup ({ cache: false });

$("#remotebuttons a").live("tap", function(){ 
	$.ajax({
		type: "POST", url: "/TV/Key",
		data: { key: $(this).attr('href').substr(1) }
	}).done(function( msg ) {
		// alert( "Data Saved: " + msg );
	});
});

$('#_switch').live('pageinit',function(event){
	$('[data-role="slider"]').on('slidestop', function(evt){
		var sliderObject = $(evt.target);
		$.ajax({ 
			url: '/_switch', type: 'POST', 
			data: { id: sliderObject.prop('id'), val: sliderObject.val() }, 
			success: function(data){ }, 
			error: function(){ } 
		});
	});
});

