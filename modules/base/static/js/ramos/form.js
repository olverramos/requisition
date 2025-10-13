function load_data( action, objectid ) {
    var verbose_action = 'Creación de Categoría';
    document.getElementById("id_form_button").hidden = false;

    if ( action == 'edit') {
        verbose_action = 'Edición de Categoría';
        document.getElementById("category-form").action = objectid + '/edit/'; 
        document.getElementById("id_form_button").innerText = 'Guardar';
    }
    if ( action == 'delete') {
        verbose_action = 'Eliminación de Categoría';
        document.getElementById("id_form_button").innerText = 'Eliminar';
        document.getElementById("category-form").action = objectid + '/delete/'; 
    }
    if ( action == 'view') {
        verbose_action = 'Consulta de Categoría';
        document.getElementById("id_form_button").hidden = true;
        document.getElementById("category-form").action = '.';
    }

    if ( action == 'view' || action == 'delete' ) {
        document.getElementById('id_name').disabled = true;
    } else {
        document.getElementById('id_name').disabled = false;
    }

    document.getElementById('title_formModal').innerText = verbose_action;

    if ( objectid != '' ) {

        var request_url = '/bussiness/categories/' + objectid + '/get/' ;
    
        // First create an XMLHttprequest object 
        var ajaxRequest = new XMLHttpRequest();
        
        ajaxRequest.onreadystatechange = function() {
            if(ajaxRequest.readyState == 4){
                //the request is completed, now check its status
                if(ajaxRequest.status == 200){
                    const category_obj = JSON.parse(ajaxRequest.responseText);
                    document.getElementById('id_name').value = category_obj.name;
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
