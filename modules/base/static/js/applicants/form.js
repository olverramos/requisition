function load_data( action, objectid ) {
    var verbose_action = 'Creación de Solicitante';
    document.getElementById("id_form_button").hidden = false;
    if ( action == 'edit') {
        verbose_action = 'Edición de Solicitante';
        document.getElementById("applicants-form").action = objectid + '/edit/'; 
        document.getElementById("id_form_button").innerText = 'Guardar';
    }
    if ( action == 'delete') {
        verbose_action = 'Eliminación de Solicitante';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("applicants-form").action = objectid + '/delete/'; 
    }
    if ( action == 'view') {
        verbose_action = 'Consulta de Solicitante';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("applicants-form").action = '.';
    }

    if ( action == 'view' || action == 'delete' ) {
        document.getElementById('id_identification').disabled = true;
        document.getElementById('id_name').disabled = true;
        document.getElementById('id_email').disabled = true;
        document.getElementById('id_phone_number').disabled = true;
    } else if ( action == 'edit' ) {
        document.getElementById('id_identification').disabled = false;
        document.getElementById('id_name').disabled = false;
        document.getElementById('id_email').disabled = true;
        document.getElementById('id_phone_number').disabled = false;
    } else {
        document.getElementById('id_identification').disabled = false;
        document.getElementById('id_name').disabled = false;
        document.getElementById('id_email').disabled = false;
        document.getElementById('id_phone_number').disabled = false;
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if ( objectid != '' ) {

        var request_url = '/base/applicant/' + objectid + '/get/' ;
    
        // First create an XMLHttprequest object 
        var ajaxRequest = new XMLHttpRequest();
        
        ajaxRequest.onreadystatechange = function() {
            if(ajaxRequest.readyState == 4){
                //the request is completed, now check its status
                if(ajaxRequest.status == 200){
                    const applicants_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_identification').value = applicants_obj.identification;
                    document.getElementById('id_name').value = applicants_obj.name;
                    document.getElementById('id_email').value = applicants_obj.email;
                    document.getElementById('id_phone_number').value = applicants_obj.phone_number;
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
