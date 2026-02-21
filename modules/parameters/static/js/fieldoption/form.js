function load_data(action, objectid) {
    var verbose_action = 'Creación de Opcion de Campo';
    document.getElementById("id_form_button").hidden = false;
    document.getElementById("id_form_button").innerText = 'Guardar';
    document.getElementById("ramofieldoption-form").action = 'create/';

    if (action == 'edit') {
        verbose_action = 'Edición de Opcion de Campo';
        document.getElementById("ramofieldoption-form").action = objectid + '/edit/';
        document.getElementById("id_form_button").innerText = 'Guardar';
    }
    if (action == 'delete') {
        verbose_action = 'Eliminación de Opcion de Campo';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("ramofieldoption-form").action = objectid + '/delete/';
    }
    if (action == 'view') {
        verbose_action = 'Consulta de Opcion de Campo';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("ramofieldoption-form").action = '.';
    }

    if (action == 'view' || action == 'delete') {
        document.getElementById('id_value').disabled = true;
        document.getElementById('id_title').disabled = true;
    } else {
        document.getElementById('id_value').disabled = false;
        document.getElementById('id_title').disabled = false;
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if (objectid != '') {

        var request_url = '/parameters/field/options/' + objectid + '/get/';

        // First create an XMLHttprequest object 
        var ajaxRequest = new XMLHttpRequest();

        ajaxRequest.onreadystatechange = function () {
            if (ajaxRequest.readyState == 4) {
                //the request is completed, now check its status
                if (ajaxRequest.status == 200) {
                    const ramofieldoption_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_value').value = ramofieldoption_obj.value;
                    document.getElementById('id_title').value = ramofieldoption_obj.title;
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
