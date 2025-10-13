$(document).ready(function() {
    $('.select2').select2();
    
    $('#state_id').change(function () {
        let endpoint_url = '/localization/cities/';
        let state_value = this.value;
        let city_value = $("#city_id").value;
        let options = filter_cities (state_value, city_value, endpoint_url);
        $("#city_id").html(options);
        if (state_value == '') {
            $("#city_id").value = '';
        }        
    });
});
