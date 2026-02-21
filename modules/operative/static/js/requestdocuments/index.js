function load_data(action, objectid) {
    var verbose_action = 'Consulta de Documento';
    document.getElementById("id_form_button").hidden = false;
    document.getElementById('id_document_class').removeAttribute("disabled");
    document.getElementById('id_title').removeAttribute("readonly");
    document.getElementById('id_document_file').removeAttribute("readonly");

    if (action == 'view') {
        verbose_action = 'Consulta de Documento';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("request-form").action = '.';
    }
    if (action == 'delete') {
        verbose_action = 'Eliminación de Documento';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("request-form").action = objectid + '/delete/';
    }
    if (action == 'edit') {
        verbose_action = 'Edición de Documento';
        document.getElementById("id_form_button").innerText = 'Guardar';
        document.getElementById("request-form").action = objectid + '/edit/';
    }

    if (action == 'view' || action == 'delete') {
        document.getElementById('id_document_class').setAttribute("disabled", "disabled");
        document.getElementById('id_title').setAttribute("readonly", "readonly");
        document.getElementById('id_document_file').setAttribute("readonly", "readonly");
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if (objectid != '') {

        var request_url = '/operative/requests/documents/' + objectid + '/get/';

        var ajaxRequest = new XMLHttpRequest();

        ajaxRequest.onreadystatechange = function () {
            if (ajaxRequest.readyState == 4) {
                //the request is completed, now check its status
                if (ajaxRequest.status == 200) {
                    const request_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_document_class').value = request_obj.document_class;
                    document.getElementById('id_title').value = request_obj.title;

                    var document_file_code = '<button type="button" class="btn btn-link" onclick="downloadFile(\'';
                    document_file_code += request_obj.filename;
                    document_file_code += "', '";
                    document_file_code += request_obj.content;
                    document_file_code += "', '";
                    document_file_code += request_obj.file_type;
                    document_file_code += '\')">';
                    document_file_code += '<i class="fa-solid fa-download"></i>&nbsp;';
                    document_file_code += request_obj.filename;
                    document_file_code += '</button>';
                    document.getElementById("section_id_document_file").innerHTML = document_file_code;
                    document.getElementById("section_id_document_file").hidden = false;
                    document.getElementById("label_id_document_file").hidden = false;
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

