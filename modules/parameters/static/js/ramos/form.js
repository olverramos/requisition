function load_data(action, objectid) {
    var verbose_action = 'Creación de Ramo';
    document.getElementById("id_form_button").hidden = false;
    document.getElementById("id_form_button").innerText = 'Guardar';
    document.getElementById("ramo-form").action = 'create/';

    if (action == 'edit') {
        verbose_action = 'Edición de Ramo';
        document.getElementById("ramo-form").action = objectid + '/edit/';
        document.getElementById("id_form_button").innerText = 'Guardar';
    }
    if (action == 'delete') {
        verbose_action = 'Eliminación de Ramo';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("ramo-form").action = objectid + '/delete/';
    }
    if (action == 'view') {
        verbose_action = 'Consulta de Ramo';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("ramo-form").action = '.';
    }

    if (action == 'view' || action == 'delete') {
        document.getElementById('id_name').disabled = true;
        document.getElementById('fields_id').disabled = true;
        document.getElementById('document_classes_id').disabled = true;
    } else {
        document.getElementById('id_name').disabled = false;
        document.getElementById('fields_id').disabled = false;
        document.getElementById('document_classes_id').disabled = false;
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if (objectid != '') {

        var request_url = '/parameters/ramo/' + objectid + '/get/';

        // First create an XMLHttprequest object 
        var ajaxRequest = new XMLHttpRequest();

        ajaxRequest.onreadystatechange = function () {
            if (ajaxRequest.readyState == 4) {
                //the request is completed, now check its status
                if (ajaxRequest.status == 200) {
                    const ramo_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_id').value = ramo_obj.id;
                    document.getElementById('id_name').value = ramo_obj.name;

                    const selected_fields = [];
                    for (let i = 0; i < ramo_obj.fields.length; i++) {
                        const field = ramo_obj.fields[i].id;
                        selected_fields.push(field);
                    }

                    for (const option of document.getElementById('fields_id').options) {
                        if (selected_fields.includes(option.value)) {
                            option.selected = true;
                        } else {
                            option.selected = false;
                        }
                    }
                    const selected_document_classes = [];
                    for (let i = 0; i < ramo_obj.document_classes.length; i++) {
                        const document_class = ramo_obj.document_classes[i].id;
                        selected_document_classes.push(document_class);
                    }

                    for (const option of document.getElementById('document_classes_id').options) {
                        if (selected_document_classes.includes(option.value)) {
                            option.selected = true;
                        } else {
                            option.selected = false;
                        }
                    }
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
