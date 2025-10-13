function load_data( action, objectid ) {
    var verbose_action = 'Creación de Cuenta';
    document.getElementById("id_form_button").hidden = false;
    document.getElementById('id_username').removeAttribute("readonly");
    if ( action == 'edit') {
        verbose_action = 'Edición de Cuenta';
        document.getElementById("account-form").action = objectid + '/edit/'; 
        document.getElementById("id_form_button").innerText = 'Guardar';
        document.getElementById('id_username').setAttribute("readonly", "readonly");
    }
    if ( action == 'delete') {
        verbose_action = 'Eliminación de Cuenta';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("account-form").action = objectid + '/delete/'; 
        document.getElementById('id_username').setAttribute("readonly", "readonly");
    }
    if ( action == 'view') {
        verbose_action = 'Consulta de Cuenta';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("account-form").action = '.';
        document.getElementById('id_username').setAttribute("readonly", "readonly");
    }

    if ( action == 'view' || action == 'delete' ) {
        document.getElementById('id_first_name').disabled = true;
        document.getElementById('id_last_name').disabled = true;
        document.getElementById('id_address').disabled = true;
        document.getElementById('id_phone').disabled = true;
        document.getElementById('id_whatsapp').disabled = true;
        document.getElementById('genre_id').setAttribute("disabled", "disabled");
        document.getElementById('state_id').setAttribute("disabled", "disabled");
        document.getElementById('city_id').setAttribute("disabled", "disabled");
        document.getElementById('role_id').setAttribute("disabled", "disabled");
    } else {
        document.getElementById('id_first_name').disabled = false;
        document.getElementById('id_last_name').disabled = false;
        document.getElementById('id_address').disabled = false;
        document.getElementById('id_phone').disabled = false;
        document.getElementById('id_whatsapp').disabled = false;
        document.getElementById('genre_id').removeAttribute("disabled");
        document.getElementById('state_id').removeAttribute("disabled");
        document.getElementById('city_id').removeAttribute("disabled");
        document.getElementById('role_id').removeAttribute("disabled");
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if ( objectid != '') {

        var request_url = '/auth/accounts/' + objectid + '/get/' ;
    
        // First create an XMLHttprequest object 
        var ajaxRequest = new XMLHttpRequest();
        
        ajaxRequest.onreadystatechange = function() {
            if(ajaxRequest.readyState == 4){
                //the request is completed, now check its status
                if(ajaxRequest.status == 200){
                    const account_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_first_name').value = account_obj.first_name;
                    document.getElementById('id_last_name').value = account_obj.last_name;
                    document.getElementById('id_username').value = account_obj.username;
                    document.getElementById('id_address').value = account_obj.address;
                    document.getElementById('id_phone').value = account_obj.phone;
                    document.getElementById('id_whatsapp').value = account_obj.whatsapp;
                    document.getElementById('genre_id').value = account_obj.genre;
                    document.getElementById('state_id').value = account_obj.state;
                    document.getElementById('city_id').value = account_obj.city;
                    document.getElementById('role_id').value = account_obj.role;
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
