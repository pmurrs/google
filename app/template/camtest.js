var target_url = "http://127.0.0.1:5000/test"
var pic;

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
        dataType: "json"
      });
}

function success_response(data){
    console.log("Success");
    console.log(data);
}