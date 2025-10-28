function load_data( action, objectid ) {
    var verbose_action = 'Creación de Tomador';
    document.getElementById("id_form_button").hidden = false;
    if ( action == 'edit') {
        verbose_action = 'Edición de Tomador';
        document.getElementById("takers-form").action = objectid + '/edit/'; 
        document.getElementById("id_form_button").innerText = 'Guardar';
    }
    if ( action == 'delete') {
        verbose_action = 'Eliminación de Tomador';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("takers-form").action = objectid + '/delete/'; 
    }
    if ( action == 'view') {
        verbose_action = 'Consulta de Tomador';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("takers-form").action = '.';
    }

    if ( action == 'view' || action == 'delete' ) {
        document.getElementById('id_identification').disabled = true;
        document.getElementById('id_name').disabled = true;
        document.getElementById('id_email').disabled = true;
        document.getElementById('id_phone_number').disabled = true;
        document.getElementById('state_id').disabled = true;
        document.getElementById('city_id').disabled = true;
    } else if ( action == 'edit' ) {
        document.getElementById('id_identification').disabled = false;
        document.getElementById('id_name').disabled = false;
        document.getElementById('id_email').disabled = true;
        document.getElementById('id_phone_number').disabled = false;
        document.getElementById('state_id').disabled = false;
        document.getElementById('city_id').disabled = false;
    } else {
        document.getElementById('id_identification').disabled = false;
        document.getElementById('id_name').disabled = false;
        document.getElementById('id_email').disabled = false;
        document.getElementById('id_phone_number').disabled = false;
        document.getElementById('state_id').disabled = false;
        document.getElementById('city_id').disabled = false;
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if ( objectid != '' ) {

        var request_url = '/base/taker/' + objectid + '/get/' ;
    
        // First create an XMLHttprequest object 
        var ajaxRequest = new XMLHttpRequest();
        
        ajaxRequest.onreadystatechange = function() {
            if(ajaxRequest.readyState == 4){
                //the request is completed, now check its status
                if(ajaxRequest.status == 200){
                    const takers_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_identification').value = takers_obj.identification;
                    document.getElementById('id_name').value = takers_obj.name;
                    document.getElementById('id_email').value = takers_obj.email;
                    document.getElementById('id_phone_number').value = takers_obj.phone_number;
                    document.getElementById('state_id').value = takers_obj.state;
                    document.getElementById('city_id').value = takers_obj.city;
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
