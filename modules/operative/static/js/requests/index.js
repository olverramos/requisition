

function change_ramo ( ramo_id, field_value, action ) {
    var request_url = APP_URL + 'parameters/ramo/' + ramo_id + '/fields/';

    var ajaxRequest = new XMLHttpRequest();
    ajaxRequest.onreadystatechange = function() {
        if(ajaxRequest.readyState == 4){
            //the request is completed, now check its status
            if(ajaxRequest.status == 200){
                const field_data_list = JSON.parse(ajaxRequest.responseText);
                var fields_code = "";
                for(var i=0; i<field_data_list.length; i++){
                    let field_data = field_data_list[i];
                    var field_code = '<div class="col-lg-3 col-md-12 mb-1">\n';
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
                    field_code += '" ';
                    field_code += ' value="';
                    field_code += field_value[field_data.name];
                    field_code += '" ';
                    if ( action != 'edit') {
                        field_code += ' readonly';
                    }
                    field_code += '>';

                    field_code += "</div>\n";
                    fields_code += field_code;
                }

                document.getElementById("custom_field_id").innerHTML = fields_code;
            } 
            else{
                console.log("Status error: " + ajaxRequest.status);
            }
        }
        else{
            console.log("Ignored readyState: " + ajaxRequest.readyState);
        }
    }
    
    ajaxRequest.open("GET", request_url, true);
    ajaxRequest.send();
}

function load_data( action, objectid ) {    
    var verbose_action = 'Edición de Solicitud';

    document.getElementById("id_form_button").hidden = false;
    document.getElementById('ramo_id').removeAttribute("readonly");

    if ( action == 'edit') {
        document.getElementById('ramo_id').setAttribute("readonly", "readonly");
    }

    if ( action == 'delete') {
        verbose_action = 'Eliminación de Solicitud';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("request-form").action = objectid + '/delete/'; 
        document.getElementById('ramo_id').setAttribute("readonly", "readonly");
    }
    if ( action == 'view') {
        verbose_action = 'Consulta de Solicitud';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("request-form").action = '.';
        document.getElementById('ramo_id').setAttribute("readonly", "readonly");
    }

    if ( action == 'view' || action == 'delete' ) {
        document.getElementById('id_taker_name').disabled = true;
        document.getElementById('id_taker_phone_number').disabled = true;
        document.getElementById('id_taker_contact_name').disabled = true;
        document.getElementById('id_value').disabled = true;
        document.getElementById('id_observations').disabled = true;
        document.getElementById('ramo_id').setAttribute("disabled", "disabled");
        document.getElementById('taker_person_type_id').setAttribute("disabled", "disabled");
        document.getElementById('taker_document_type_id').setAttribute("disabled", "disabled");
        document.getElementById('status_id').setAttribute("disabled", "disabled");
    } else {
        document.getElementById('id_taker_name').disabled = false;
        document.getElementById('id_taker_phone_number').disabled = false;
        document.getElementById('id_taker_contact_name').disabled = false;
        document.getElementById('id_value').disabled = false;
        document.getElementById('id_observations').disabled = false;
        document.getElementById('ramo_id').removeAttribute("disabled");
        document.getElementById('taker_person_type_id').removeAttribute("disabled");
        document.getElementById('taker_document_type_id').removeAttribute("disabled");
        document.getElementById('status_id').removeAttribute("disabled");
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if ( objectid != '') {

        var request_url = '/operative/requests/' + objectid + '/get/' ;
    
        var ajaxRequest = new XMLHttpRequest();
        
        ajaxRequest.onreadystatechange = function() {
            if(ajaxRequest.readyState == 4){
                //the request is completed, now check its status
                if(ajaxRequest.status == 200){
                    const request_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_number').value = request_obj.number;
                    document.getElementById('id_applicant_phone_number').value = request_obj.applicant_phone_number;
                    document.getElementById('id_applicant_name').value = request_obj.applicant_name;
                    document.getElementById('id_taker_identification').value = request_obj.taker_identification;
                    document.getElementById('id_taker_name').value = request_obj.taker_name;
                    document.getElementById('taker_person_type_id').value = request_obj.taker_person_type_id;
                    document.getElementById('taker_document_type_id').value = request_obj.taker_document_type_id;
                    document.getElementById('id_taker_phone_number').value = request_obj.taker_phone_number;
                    document.getElementById('id_taker_contact_name').value = request_obj.taker_contact_name;
                    document.getElementById('ramo_id').value = request_obj.ramo_id;
                    document.getElementById('id_value').value = request_obj.value;
                    document.getElementById('id_observations').value = request_obj.observations;
                    document.getElementById('status_id').value = request_obj.status_id;
                    change_ramo(request_obj.ramo_id, request_obj.fields, action);
                }
                else{
                    console.log("Status error: " + ajaxRequest.status);
                }
            }
            else{
                console.log("Ignored readyState: " + ajaxRequest.readyState);
            }
        }
        
        ajaxRequest.open("GET", request_url, true);
        ajaxRequest.send();
    }
}

