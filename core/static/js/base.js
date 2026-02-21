$(document).on('focus', 'input[readonly]', function () {
    this.blur();
});

function toggleMenu() {
    document.querySelector('.nav ul').classList.toggle('active');
}

function base_ayax_fill_combobox (filter_field_id_list, destine_field_id, base_request_url) {
    let filter_id_list = [ ]
    var can_doit = true;
    for (var i=0; i<filter_field_id_list.length; i++) {
        var filter_id = $("#" + filter_field_id_list[i]).val();
        if (filter_id != null && filter_id != "" ) {
            filter_id_list.push(filter_id);
        } else {
            can_doit = false;
        }
    }

    let destine_field_val = $("#" + destine_field_id).val();
    
    if ( can_doit ) {
        var request_url = base_request_url;
        for (var i=0; i<filter_id_list.length; i++) {
            request_url += filter_id_list[i] + '/';
        }

        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function(data, textStatus) {
                var options = "";
                options += '<option value="">---------</option>';
                for (var i=0; i<data.length; i++) {
                    options += '<option value="';
                    options += data[i]['id'];
                    options += '" ';
                    if ( destine_field_val == data[i]['id'] ) {
                        options += 'selected="selected"';
                    }
                    options +=  '>';
                    options += data[i]['description'];
                    options +=  '</option>';
                }
                $("#" + destine_field_id).html(options);    
            },
            error: function(msg) {
                alert('Error en la transacción: ' + msg);
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener("focus", function () {
            this.select();
        });
    });
});
