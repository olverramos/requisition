function filter_cities (state_value, city_value, endpoint_url) {
    let request_url = endpoint_url + '?state=' + state_value ;
    let destine_selected_val = city_value;
    var options = "";

    $.ajax({
        type: "GET",
        async: false,
        url: request_url,
        dataType: "json",
        success: function(data, textStatus) {
            options += '<option value="">---------</option>';
            for (var i=0; i<data.length; i++) {
                options += '<option value="';
                options += data[i]['id'];
                options += '" ';
                if ( destine_selected_val == data[i]['id'] ) {
                    options += 'selected="selected"';
                }
                options +=  '>';
                options += data[i]['name'];
                options +=  '</option>';
            }
        },
        error: function(msg) {
            alert('Error de conexión al sistema.');
        }
    });
    return options;
}
