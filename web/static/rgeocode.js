var geocoder;
function initialize() {
    geocoder = new google.maps.Geocoder();
}
function codeLatLng(input, fn) {
    var latlngStr = input.split(",");
    var lat = parseFloat(latlngStr[0]);
    var lng = parseFloat(latlngStr[1]);
    var latlng = new google.maps.LatLng(lat, lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            console.log("STEP 1");
            if (results[3]) {
                console.log("RESULT 3 ACCEPTED");
                var rgc = results[3].formatted_address;
                fn(rgc);
            }
        } else {
            alert("Geocoder failed due to: " + status);
        }
    });
}
google.maps.event.addDomListener(window, 'load', initialize);
