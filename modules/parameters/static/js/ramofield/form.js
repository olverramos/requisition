function load_data(action, objectid) {
    var verbose_action = 'Creación de Campo de Ramo';
    document.getElementById("id_form_button").hidden = false;
    document.getElementById("id_form_button").innerText = 'Guardar';
    document.getElementById("ramofield-form").action = 'create/';

    if (action == 'edit') {
        verbose_action = 'Edición de Campo de Ramo';
        document.getElementById("ramofield-form").action = objectid + '/edit/';
        document.getElementById("id_form_button").innerText = 'Guardar';
    }
    if (action == 'delete') {
        verbose_action = 'Eliminación de Campo de Ramo';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("ramofield-form").action = objectid + '/delete/';
    }
    if (action == 'view') {
        verbose_action = 'Consulta de Campo de Ramo';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("ramofield-form").action = '.';
    }

    if (action == 'view' || action == 'delete') {
        document.getElementById('id_field_type').disabled = true;
        document.getElementById('id_name').disabled = true;
        document.getElementById('id_title').disabled = true;
        document.getElementById('id_mandatory').disabled = true;
    } else {
        document.getElementById('id_field_type').disabled = false;
        document.getElementById('id_name').disabled = false;
        document.getElementById('id_title').disabled = false;
        document.getElementById('id_mandatory').disabled = false;
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if (objectid != '') {

        var request_url = '/parameters/field/' + objectid + '/get/';

        // First create an XMLHttprequest object 
        var ajaxRequest = new XMLHttpRequest();

        ajaxRequest.onreadystatechange = function () {
            if (ajaxRequest.readyState == 4) {
                //the request is completed, now check its status
                if (ajaxRequest.status == 200) {
                    const ramofield_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_name').value = ramofield_obj.name;
                    document.getElementById('id_field_type').value = ramofield_obj.field_type;
                    document.getElementById('id_title').value = ramofield_obj.title;
                    document.getElementById('id_mandatory').value = ramofield_obj.mandatory;
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
