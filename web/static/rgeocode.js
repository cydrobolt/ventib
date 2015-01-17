var geocoder;
function initialize() {
    geocoder = new google.maps.Geocoder();
}
function codeLatLng(input) {
    var latlngStr = input.split(",");
    var lat = parseFloat(latlngStr[0]);
    var lng = parseFloat(latlngStr[1]);
    var latlng = new google.maps.LatLng(lat, lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
        console.log(results);
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[3]) {
                console.log(results[3].formatted_address);
                return results[3].formatted_address;
            }
        } else {
            alert("Geocoder failed due to: " + status);
        }
    });
}
google.maps.event.addDomListener(window, 'load', initialize);
