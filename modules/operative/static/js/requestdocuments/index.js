

function load_data(action, objectid) {
    var verbose_action = 'Consulta de Solicitud';
    document.getElementById("id_form_button").hidden = false;
    document.getElementById('ramo_id').removeAttribute("disabled");
    document.getElementById('status_id').removeAttribute("disabled");
    document.getElementById('label_id_validated_at').hidden = false;
    document.getElementById('id_validated_at').hidden = false;
    document.getElementById('label_id_validated_by').hidden = false;
    document.getElementById('id_validated_by').hidden = false;

    if (action == 'view') {
        verbose_action = 'Consulta de Solicitud';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("request-form").action = '.';
    }
    if (action == 'delete') {
        verbose_action = 'Eliminación de Solicitud';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("request-form").action = objectid + '/delete/';
    }
    if (action == 'edit') {
        verbose_action = 'Edición de Solicitud';
        document.getElementById("id_form_button").innerText = 'Guardar';
        document.getElementById("request-form").action = objectid + '/edit/';
    }
    if (action == 'assign') {
        verbose_action = 'Asignación de Solicitud';
        document.getElementById("id_form_button").innerText = 'Asignar';
        document.getElementById("request-form").action = objectid + '/assign/';
    }
    if (action == 'loaddocuments') {
        verbose_action = 'Cargue de Documentos Solicitud';
        document.getElementById("id_form_button").innerText = 'Cargar';
        document.getElementById("request-form").action = objectid + '/loaddocuments/';
    }
    if (action == 'validate') {
        verbose_action = 'Validación de Solicitud';
        document.getElementById("id_form_button").innerText = 'Validar';
        document.getElementById("request-form").action = objectid + '/validate/';
    }

    if (action == 'edit') {
        document.getElementById('ramo_id').removeAttribute("disabled");
        document.getElementById('status_id').removeAttribute("disabled");
        document.getElementById('taker_person_type_id').removeAttribute("disabled");
        document.getElementById('taker_document_type_id').removeAttribute("disabled");
        document.getElementById('id_taker_name').removeAttribute("readonly");
        document.getElementById('id_taker_phone_number').removeAttribute("readonly");
        document.getElementById('id_taker_contact_name').removeAttribute("readonly");
        document.getElementById('id_value').removeAttribute("readonly");
        document.getElementById('assigned_to_id').removeAttribute("disabled");
        document.getElementById('id_request_receipt').removeAttribute("disabled");
        document.getElementById('id_request_rc_receipt').removeAttribute("disabled");
        document.getElementById('id_request_police').removeAttribute("disabled");
        document.getElementById('id_request_rc_police').removeAttribute("disabled");
        document.getElementById('id_observations').removeAttribute("readonly");
        document.getElementById('id_request_receipt').hidden = false;
        document.getElementById('id_request_rc_receipt').hidden = false;
        document.getElementById('id_request_police').hidden = false;
        document.getElementById('id_request_rc_police').hidden = false;
        document.getElementById('label_id_request_receipt').hidden = false;
        document.getElementById('label_id_request_rc_receipt').hidden = false;
        document.getElementById('label_id_request_police').hidden = false;
        document.getElementById('label_id_request_rc_police').hidden = false;
    } else {
        document.getElementById('ramo_id').setAttribute("disabled", "disabled");
        document.getElementById('status_id').setAttribute("disabled", "disabled");
        document.getElementById('taker_person_type_id').setAttribute("disabled", "disabled");
        document.getElementById('taker_document_type_id').setAttribute("disabled", "disabled");
        document.getElementById('id_taker_name').setAttribute("readonly", "readonly");
        document.getElementById('id_taker_phone_number').setAttribute("readonly", "readonly");
        document.getElementById('id_taker_contact_name').setAttribute("readonly", "readonly");
        document.getElementById('id_value').setAttribute("readonly", "readonly");
        document.getElementById('assigned_to_id').setAttribute("disabled", "disabled");
        document.getElementById('id_request_receipt').setAttribute("disabled", "disabled");
        document.getElementById('id_request_rc_receipt').setAttribute("disabled", "disabled");
        document.getElementById('id_request_police').setAttribute("disabled", "disabled");
        document.getElementById('id_request_rc_police').setAttribute("disabled", "disabled");
        document.getElementById('id_observations').setAttribute("readonly", "readonly");
        document.getElementById('id_request_receipt').hidden = false;
        document.getElementById('id_request_rc_receipt').hidden = false;
        document.getElementById('id_request_police').hidden = false;
        document.getElementById('id_request_rc_police').hidden = false;
        document.getElementById('label_id_request_receipt').hidden = false;
        document.getElementById('label_id_request_rc_receipt').hidden = false;
        document.getElementById('label_id_request_police').hidden = false;
        document.getElementById('label_id_request_rc_police').hidden = false;
    }

    if (action == 'assign') {
        document.getElementById('assigned_to_id').removeAttribute("disabled");
        document.getElementById('label_id_validated_at').hidden = true;
        document.getElementById('id_validated_at').hidden = true;
        document.getElementById('label_id_validated_by').hidden = true;
        document.getElementById('id_validated_by').hidden = true;
    }

    if (action == 'loaddocuments') {
        document.getElementById('label_id_validated_at').hidden = true;
        document.getElementById('id_validated_at').hidden = true;
        document.getElementById('label_id_validated_by').hidden = true;
        document.getElementById('id_validated_by').hidden = true;
        document.getElementById('id_request_receipt').removeAttribute("disabled");
        document.getElementById('id_request_rc_receipt').removeAttribute("disabled");
        document.getElementById('id_request_police').removeAttribute("disabled");
        document.getElementById('id_request_rc_police').removeAttribute("disabled");
    }

    if (action == 'validate') {
        document.getElementById('label_id_validated_at').hidden = true;
        document.getElementById('id_validated_at').hidden = true;
        document.getElementById('label_id_validated_by').hidden = true;
        document.getElementById('id_validated_by').hidden = true;
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if (objectid != '') {

        var request_url = '/operative/requests/' + objectid + '/get/';

        var ajaxRequest = new XMLHttpRequest();

        ajaxRequest.onreadystatechange = function () {
            if (ajaxRequest.readyState == 4) {
                //the request is completed, now check its status
                if (ajaxRequest.status == 200) {
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
                    document.getElementById('assigned_to_id').value = request_obj.assigned_to_id;
                    document.getElementById('id_value').value = request_obj.value;
                    document.getElementById('id_observations').value = request_obj.observations;
                    document.getElementById('status_id').value = request_obj.status_id;
                    document.getElementById('id_created_at').value = request_obj.created_at;
                    document.getElementById('id_validated_at').value = request_obj.validated_at;
                    document.getElementById('id_validated_by').value = request_obj.validated_by;

                    if (request_obj.request_receipt) {
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
                        document.getElementById("section_id_request_receipt").hidden = false;
                        document.getElementById("label_id_request_receipt").hidden = false;
                    } else if (action != 'loaddocuments') {
                        document.getElementById("section_id_request_receipt").hidden = true;
                        document.getElementById("label_id_request_receipt").hidden = true;
                    }

                    if (request_obj.request_rc_receipt) {
                        var request_rc_receipt_code = '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                        request_rc_receipt_code += request_obj.request_rc_receipt.filename;
                        request_rc_receipt_code += "', '";
                        request_rc_receipt_code += request_obj.request_rc_receipt.content;
                        request_rc_receipt_code += "', '";
                        request_rc_receipt_code += request_obj.request_rc_receipt.file_type;
                        request_rc_receipt_code += '\')">';
                        request_rc_receipt_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                        request_rc_receipt_code += request_obj.request_rc_receipt.filename;
                        request_rc_receipt_code += '</button>';
                        document.getElementById("section_id_request_rc_receipt").innerHTML = request_rc_receipt_code;
                        document.getElementById("section_id_request_rc_receipt").hidden = false;
                        document.getElementById("label_id_request_rc_receipt").hidden = false;
                    } else if (action != 'loaddocuments') {
                        document.getElementById("section_id_request_rc_receipt").hidden = true;
                        document.getElementById("label_id_request_rc_receipt").hidden = true;
                    }

                    if (request_obj.request_police) {
                        var request_police_code = '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                        request_police_code += request_obj.request_police.filename;
                        request_police_code += "', '";
                        request_police_code += request_obj.request_police.content;
                        request_police_code += "', '";
                        request_police_code += request_obj.request_police.file_type;
                        request_police_code += '\')">';
                        request_police_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                        request_police_code += request_obj.request_police.filename;
                        request_police_code += '</button>';
                        document.getElementById("section_id_request_police").innerHTML = request_police_code;
                        document.getElementById("section_id_request_police").hidden = false;
                        document.getElementById("label_id_request_police").hidden = false;
                    } else if (action != 'loaddocuments') {
                        document.getElementById("section_id_request_police").hidden = true;
                        document.getElementById("label_id_request_police").hidden = true;
                    }

                    if (request_obj.request_rc_police) {
                        var request_rc_police_code = '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                        request_rc_police_code += request_obj.request_rc_police.filename;
                        request_rc_police_code += "', '";
                        request_rc_police_code += request_obj.request_rc_police.content;
                        request_rc_police_code += "', '";
                        request_rc_police_code += request_obj.request_rc_police.file_type;
                        request_rc_police_code += '\')">';
                        request_rc_police_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                        request_rc_police_code += request_obj.request_rc_police.filename;
                        request_rc_police_code += '</button>';
                        document.getElementById("section_id_request_rc_police").innerHTML = request_rc_police_code;
                        document.getElementById("section_id_request_rc_police").hidden = false;
                        document.getElementById("label_id_request_rc_police").hidden = false;
                    } else if (action != 'loaddocuments') {
                        document.getElementById("section_id_request_rc_police").hidden = true;
                        document.getElementById("label_id_request_rc_police").hidden = true;
                    }

                    if (request_obj.payment_receipt) {
                        var payment_receipt_code = '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                        payment_receipt_code += request_obj.payment_receipt.filename;
                        payment_receipt_code += "', '";
                        payment_receipt_code += request_obj.payment_receipt.content;
                        payment_receipt_code += "', '";
                        payment_receipt_code += request_obj.payment_receipt.file_type;
                        payment_receipt_code += '\')">';
                        payment_receipt_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                        payment_receipt_code += request_obj.payment_receipt.filename;
                        payment_receipt_code += '</button>';
                        document.getElementById("section_id_payment_receipt").innerHTML = payment_receipt_code;
                        document.getElementById("section_id_payment_receipt").hidden = false;
                        document.getElementById("label_id_payment_receipt").hidden = false;
                    } else {
                        document.getElementById("section_id_payment_receipt").hidden = true;
                        document.getElementById("label_id_payment_receipt").hidden = true;
                    }

                    if (request_obj.payment_rc_receipt) {
                        var payment_rc_receipt_code = '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                        payment_rc_receipt_code += request_obj.payment_rc_receipt.filename;
                        payment_rc_receipt_code += "', '";
                        payment_rc_receipt_code += request_obj.payment_rc_receipt.content;
                        payment_rc_receipt_code += "', '";
                        payment_rc_receipt_code += request_obj.payment_rc_receipt.file_type;
                        payment_rc_receipt_code += '\')">';
                        payment_rc_receipt_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                        payment_rc_receipt_code += request_obj.payment_rc_receipt.filename;
                        payment_rc_receipt_code += '</button>';
                        document.getElementById("section_id_payment_rc_receipt").innerHTML = payment_rc_receipt_code;
                        document.getElementById("section_id_payment_rc_receipt").hidden = false;
                        document.getElementById("label_id_payment_rc_receipt").hidden = false;
                    } else {
                        document.getElementById("section_id_payment_rc_receipt").hidden = true;
                        document.getElementById("label_id_payment_rc_receipt").hidden = true;
                    }


                    loadFieldsData(request_obj.ramo_id, request_obj.fields, action);
                    loadDocumentsData(request_obj.ramo_id, request_obj.documents);
                }
                else {
                    console.log("Status error: " + ajaxRequest.status);
                }
            }
            else {
                console.log("Ignored readyState: " + ajaxRequest.readyState);
            }
        }

        ajaxRequest.open("GET", request_url, true);
        ajaxRequest.send();
    }
}

