var ctx = $("#graph-times").get(0).getContext("2d");
var times = new Chart(ctx);
window.cache2["0,0"] = "Location Unavailable";
var throttles = [];

function searchTableGen(a, b, c) {
    var template = '<tr>\
      <td>' + a + '</td>\
      <td>' + b + '</td>\
      <td>' + c + '</td>\
    </tr>';
    return template;
}

function search() {
    try {
        var term = $("#search").val();
        var thrott = 0;
        $.getJSON('/api/search/', {
            q: term
        }, function(data) {
            $("#search-result").hide();
            $("#search-loading").show();
            var tableContents = "";
            window.tableTemplate = "";
            /*var dataarr = $.map(data, function(value, index) {
                return [data];
            });*/
            data.texts.forEach(function(el, index, ar) {
                window.elements = el.split("@@@@@SPL~T@@@@@@");
                tableContents += searchTableGen(elements[0], elements[1], elements[2]);
                console.log(tableContents);
            });
            tableTemplate = '<table class="small" style="font-size:80%">\
                   <tbody>\
                ' + tableContents + '\
                   </tbody>\
                </table>';
            $("#search-result").html(tableTemplate);
            for (var i = 0, z = throttles.length; i < z; i++)
                clearTimeout(throttles[i]);
            throttles = [];

            $(".loc").each(function(index) {
                var needful = this;
                var scoords = $(needful).text();
                if (cache2[scoords] != undefined) {
                    $(needful).html('<i class="mdi-maps-pin-drop"></i>' + cache2[scoords]);
                } else {
                    console.log("nocache");
                    throttles.push(setTimeout(function() {
                        codeLatLng(scoords, function(res) {
                            $(needful).html('<i class="mdi-maps-pin-drop"></i>' + res);
                            cache2[scoords] = res;
                        });
                    }, thrott));
                    thrott += 1200;
                }
            });
            $("#search-loading").hide();
            $("#search-result").show();
        });
    } catch (err) {
        console.log("Error: " + err);
    }
}

function refreshQuote() {
    $.ajax({
        type: "POST",
        url: "/api/v1/refresh_quote/"
    })
    .done(function(msg) {
        $("#randomQuote").html(msg);
    });
}

ctx.canvas.width = 960;
ctx.canvas.height = 400;
var times = new Chart(ctx).Bar(times_data);
