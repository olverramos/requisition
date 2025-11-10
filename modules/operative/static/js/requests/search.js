

function loadFieldsData ( ramo_id, fields_value, action ) {
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
                    field_code += fields_value[field_data.name];
                    field_code += '" ';
                    if ( action != 'edit') {
                        field_code += ' readonly';
                    }
                    if ( field_data.field_type == 'IN') {
                        field_code += ' />';
                    }
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

function downloadFile(fileName, data, fileFormat) {
    const linkSource = 'data:'+fileFormat+';base64,'+data;
    const downloadLink = document.createElement("a");
    downloadLink.href = linkSource;
    downloadLink.download = fileName;
    downloadLink.click();
}

function loadDocumentsData ( ramo_id, documents_value ) {
    
    let document_request_url = APP_URL + 'parameters/ramo/' + ramo_id + '/documents/';

    var ajaxRequest = new XMLHttpRequest();
    ajaxRequest.onreadystatechange = function() {
        if(ajaxRequest.readyState == 4){
            //the request is completed, now check its status
            if(ajaxRequest.status == 200){
                const docuiment_data_list = JSON.parse(ajaxRequest.responseText);
                var documents_code = "";
                for(var i=0; i<docuiment_data_list.length; i++){
                    let document_data = docuiment_data_list[i];
                    var document_code = '<div class="col-lg-6 col-md-12 mb-1">\n';
                    document_code += '<label class="text-main align-self-center">';
                    document_code += document_data.title ;  
                    if ( document_data.mandatory )
                    {
                        document_code += ' *'     
                    }
                    document_code += '</label>&nbsp;&nbsp;';

                    if ( document_data.name in documents_value ) {
                        document_code += '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                        document_code += documents_value[document_data.name].filename;
                        document_code += "', '";
                        document_code += documents_value[document_data.name].content;
                        document_code += "', '";
                        document_code += documents_value[document_data.name].file_type;
                        document_code += '\')">';
                        document_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                        document_code += documents_value[document_data.name].filename;
                        document_code += '</button>'; 
                    } else {
                        document_code += '<input type="text" value="No importado" class="form-control form-control-sm" readonly />';
                    }

                    document_code += "</div>\n";
                    documents_code += document_code;
                }

                document.getElementById("ramo_document_id").innerHTML = documents_code;
            } 
            else{
                console.log("Status error: " + ajaxRequest.status);
            }
        }
        else{
            console.log("Ignored readyState: " + ajaxRequest.readyState);
        }
    }
    
    ajaxRequest.open("GET", document_request_url, true);
    ajaxRequest.send();

}


function load_data( action, objectid ) {    
    var verbose_action = 'Consulta de Solicitud';

    document.getElementById("id_form_button").hidden = false;
    document.getElementById('ramo_id').removeAttribute("readonly");

    if ( action == 'paymentregister') {
        verbose_action = 'Registro de Comprobante de Pago';
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

    if ( action == 'view' ) {
        document.getElementById('status_id').setAttribute("disabled", "disabled");
    } else {
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
                    loadFieldsData(request_obj.ramo_id, request_obj.fields,action);
                    loadDocumentsData(request_obj.ramo_id, request_obj.documents);
                
                    if ( request_obj.request_receipt ) {
                        var request_receipt_code = '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                        request_receipt_code += request_obj.request_receipt.filename;
                        request_receipt_code += "', '";
                        request_receipt_code += request_obj.request_receipt.content;
                        request_receipt_code += "', '";
                        request_receipt_code += request_obj.request_receipt.file_type;
                        request_receipt_code += '\')">';
                        request_receipt_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                        request_receipt_code += request_obj.request_receipt.filename;
                        request_receipt_code += '</button>'; 
                        document.getElementById("section_id_request_receipt").innerHTML = request_receipt_code;
                    }
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

