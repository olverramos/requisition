$(document).ready(function() {

    $("#id_applicant_phone_number").change(function() {
        let applicant_phone_number = $(this).val();
        let request_url = APP_URL + 'base/applicant/search/?phone_number=' + applicant_phone_number;
        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function(data, textStatus) {
                if ("name" in data) {
                    $('#id_applicant_name').val(data.name);
                    $('#id_applicant_id').val(data.id);
                } else {
                    alert ("El solicitante no está registrado.")
                }
            },
            error: function(msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });
    });

    $("#ramo_id").change(function() {
        let ramo_id = $(this).val();
        var request_url = APP_URL + 'parameters/ramo/' + ramo_id + '/fields/';
        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function(data, textStatus) {
                var fields_code = "";
                for(var i=0; i<data.length; i++){
                    let field_data = data[i];
                    var field_code = '<div class="col-lg-4 col-md-12">\n';
                    field_code += '<label class="text-main align-self-center">';
                    field_code += field_data.title ;  
                    if ( field_data.mandatory )
                    {
                        field_code += ' *'     
                    }
                    field_code += '</label>';
                    if ( field_data.field_type == 'IN') {
                        field_code += '<input type="text" '
                    }
                        
                    field_code += 'class="form-control form-control-lg" placeholder=" ';
                    field_code += field_data.title;
                    field_code += '"';
                    if ( field_data.mandatory )
                    {
                        field_code += ' required '     
                    }
                    field_code += 'name="';
                    field_code += field_data.name ;
                    field_code += '" ';
                    field_code += 'id="id_';
                    field_code += field_data.name ;
                    field_code += '">';

                    field_code += "</div>\n";
                    fields_code += field_code;
                    
                }
                $('#custom_field_id').html(fields_code);
            },
            error: function(msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });

        let document_request_url = APP_URL + 'parameters/ramo/' + ramo_id + '/documents/';
        $.ajax({
            type: "GET",
            async: false,
            url: document_request_url,
            dataType: "json",
            success: function(data, textStatus) {
                var documents_code = "";
                for(var i=0; i<data.length; i++){
                    let document_data = data[i];
                    var document_code = '<div class="col-lg-6 col-md-12">\n';
                    
                    document_code += '<label class="text-main align-self-center">';
                    document_code += document_data.title ;  
                    if ( document_data.mandatory )
                    {
                        document_code += ' *'     
                    }
                    document_code += '</label>';
                    
                    document_code += '<input type="file" '
                    document_code += 'class="form-control form-control-lg" ';
                    if ( document_data.mandatory )
                    {
                        document_code += ' required '     
                    }
                    document_code += 'name="document_';
                    document_code += document_data.name ;
                    document_code += '" ';
                    document_code += 'id="id_document_';
                    document_code += document_data.name ;
                    document_code += '">';

                    document_code += "</div>\n";
                    documents_code += document_code;
                }
                $('#ramo_document_id').html(documents_code);
            },
            error: function(msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });

    });

    $("#taker_person_type_id").change(function() {
        let person_type_id = $(this).val();
        let destine_selected_val = $("#taker_document_type_id").val();
        let request_url = APP_URL + 'base/persontype/' + person_type_id + '/getdocumenttypes/';
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
                    options += '</option>';
                }
            },
            error: function(msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });
        $("#taker_document_type_id").html(options);
        if (person_type_id == '') {
            $("#taker_document_type_id").val('');
        }
    });

    $("#id_taker_identification").change(function() {
        let taker_identification = $(this).val();
        let request_url = APP_URL + 'base/taker/search/?identification=' + taker_identification;
        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function(data, textStatus) {
                if ("name" in data) {
                    $('#taker_person_type_id').val(data.person_type);
                    $('#taker_document_type_id').val(data.document_type);
                    $('#id_taker_identification').val(data.identification);
                    $('#id_taker_name').val(data.name);
                    $('#id_taker_phone_number').val(data.phone_number);
                    $('#id_taker_contact_name').val(data.contact_name);
                    $('#taker_person_type_id').change();
                }
            },
            error: function(msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });
    });

});