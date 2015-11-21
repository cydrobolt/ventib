function get_coordinates(callback) {
    if (!navigator.geolocation) {
        // unsupported
        callback('0,0');
    }

    function success(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        console.log('Succeessfully located!');
        callback(latitude + ',' + longitude);
    }

    function error() {
        callback('0,0');
    }
    navigator.geolocation.getCurrentPosition(success, error);
}

var mic = new Wit.Microphone(document.getElementById("microphone"));

mic.onready = function () {
    console.info("Microphone is ready to record");
};
mic.onaudiostart = function () {
    console.info("Recording started");
    setTimeout(function () {
        mic.stop();
        console.log("Autoending...");
    }, 10000);
};
mic.onaudioend = function () {
    console.info("Recording stopped, processing started");
};
mic.onresult = function (intent, entities, fullText) {
    console.log(fullText);

    // TODO perform analysis on intent as well
    setTimeout(function () {
        mic.start();
        console.log("Audio starting...");
    }, 1500);

    var location = get_coordinates(function (location) {
        var request = $.ajax({
            url: "/api/v1/submit_speech/",
            method: "POST",
            data: {
                key: api_key,
                text: fullText,
                location: location
            },
            dataType: "html"
        });

        request.done(function( msg ) {
            console.log("Successfully sent!");
        });
    });
};
mic.onerror = function (err) {
    console.error("Error: " + err);
    setTimeout(function () {
        mic.start();
        console.log("Audio starting...");
    }, 1500);
};
mic.onconnecting = function () {
    console.info("Microphone is connecting");
};
mic.ondisconnected = function () {
    console.info("Microphone is not connected");
};

mic.connect("DUITT7WYHWSDI27QX43GBWHMFVJ37ZKM");
