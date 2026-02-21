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

    $('#filter_state_id').change(function () {
        let endpoint_url = '/localization/cities/';
        let state_value = this.value;
        let city_value = $("#filter_city_id").value;
        let options = filter_cities (state_value, city_value, endpoint_url);
        $("#filter_city_id").html(options);
        if (state_value == '') {
            $("#filter_city_id").value = '';
        }
    });
});

function load_setpassword_data(account_id) {
    document.getElementById('account_id').value = account_id;
}
