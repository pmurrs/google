var target_url = "https://canadiantired-207914.appspot.com/test"
var pic;

$(document).ready(function() {

       $('.button').click(take_snapshot);
	   console.log('onready');

   });

Webcam.set({
    width: window.innerWidth,
    height: window.innerHeight,
    image_format: 'jpeg',
    jpeg_quality: 90,
    constraints: {
        width: { exact: 1280 },
        height: { exact: 720 }
    }
});

Webcam.attach( '#my_camera' );

function take_snapshot() {
    // take snapshot and get image data
	console.log('fired');
    Webcam.snap( function(data_uri) {
        pic = data_uri;
        send_image(pic);
    } );
}

function send_image(img){
    $.ajax({
        traditional: true,
        type: "POST",
		crossDomain: true,
		processData: false,
        url: target_url,
        data: encodeURIComponent(img),
        success: success_response,
        dataType: "jsonp"
      });
}

function success_response(data){
    console.log("Success");
    console.log(data);
}