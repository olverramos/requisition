$(document).ready(function () {

    $("#id_applicant_phone_number").change(function () {
        let applicant_phone_number = $(this).val();
        let request_url = APP_URL + 'base/applicant/search/?phone_number=' + applicant_phone_number;
        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function (data, textStatus) {
                if ("name" in data) {
                    $('#id_applicant_name').val(data.name);
                    $('#id_applicant_id').val(data.id);
                } else {
                    alert("El solicitante no está registrado.")
                }
            },
            error: function (msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });
    });

    $("#ramo_id").change(function () {
        let ramo_id = $(this).val();
        var request_url = APP_URL + 'parameters/ramo/' + ramo_id + '/fields/';
        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function (data, textStatus) {
                var fields_code = "";
                for (var i = 0; i < data.length; i++) {
                    let field_data = data[i];
                    var field_code = '<div class="col-lg-4 col-md-12">\n';
                    field_code += '<label class="text-main align-self-center">';
                    field_code += field_data.title;
                    if (field_data.mandatory) {
                        field_code += ' *'
                    }
                    field_code += '</label>';
                    if (field_data.field_type == 'IN') {
                        field_code += '<input type="text" '
                    }

                    field_code += 'class="form-control form-control-lg" placeholder=" ';
                    field_code += field_data.title;
                    field_code += '"';
                    if (field_data.mandatory) {
                        field_code += ' required '
                    }
                    field_code += 'name="';
                    field_code += field_data.name;
                    field_code += '" ';
                    field_code += 'id="id_';
                    field_code += field_data.name;
                    field_code += '">';

                    field_code += "</div>\n";
                    fields_code += field_code;

                }
                $('#custom_field_id').html(fields_code);
            },
            error: function (msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });
    });

    $("#taker_person_type_id").change(function () {
        let person_type_id = $(this).val();
        let destine_selected_val = $("#taker_document_type_id").val();
        let request_url = APP_URL + 'base/persontype/' + person_type_id + '/getdocumenttypes/';
        var options = "";

        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function (data, textStatus) {
                options += '<option value="">---------</option>';
                for (var i = 0; i < data.length; i++) {
                    options += '<option value="';
                    options += data[i]['id'];
                    options += '" ';
                    if (destine_selected_val == data[i]['id']) {
                        options += 'selected="selected"';
                    }
                    options += '>';
                    options += data[i]['name'];
                    options += '</option>';
                }
            },
            error: function (msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });
        $("#taker_document_type_id").html(options);
        if (person_type_id == '') {
            $("#taker_document_type_id").val('');
        }
    });

    $("#id_taker_identification").change(function () {
        let taker_identification = $(this).val();
        let request_url = APP_URL + 'base/taker/search/?identification=' + taker_identification;
        $.ajax({
            type: "GET",
            async: false,
            url: request_url,
            dataType: "json",
            success: function (data, textStatus) {
                if ("name" in data) {
                    $('#taker_person_type_id').val(data.person_type);
                    $('#taker_document_type_id').val(data.document_type);
                    $('#id_taker_identification').val(data.identification);
                    $('#id_taker_name').val(data.name);
                    $('#id_taker_phone_number').val(data.phone_number);
                    $('#id_taker_contact_name').val(data.contact_name);
                    $('#taker_person_type_id').change();
                }
            },
            error: function (msg) {
                alert('Error en la transacción: ' + JSON.stringify(msg));
            }
        });
    });

    $("#id_value").mask("#,##0", { reverse: true });


    $("#addbutton_id").click(function () {
        alert("hola");

        let document_count = parseInt($("#document_count_id").val());
        document_count++;
        $("#document_count_id").val(document_count);

        let document_form = {
            document_class: $("#document_class_id").val(),
            title: $("#document_title_id").val(),
            document_file: $("#document_file_id").val()
        };

        let document_form_code = '<tr id="document_detail_' + document_count + '_id">';
        document_form_code += '<td class="text-center">';
        document_form_code += document_form.document_class;
        document_form_code += '</td>';
        document_form_code += '<td class="text-center">';
        document_form_code += document_form.title;
        document_form_code += '</td>';
        document_form_code += '<td class="text-center">';
        document_form_code += document_form.document_file;
        document_form_code += '</td>';
        document_form_code += '<td class="text-center">';
        document_form_code += '<button type="button" id="addbutton_id" class="btn btn-table w-30">+</button>';
        document_form_code += '</td>';
        document_form_code += '</tr>';

        $("#new_document_tbody_id").append(document_form_code);

        // let detail_json_text = $("#id_detail_json").val();

        // var detail_json = {};
        // if (detail_json_text != null && detail_json_text != '') {
        //     detail_json = jQuery.parseJSON(detail_json_text);
        // }

        // let combs_json_text = $("#id_combs_json").val();

        // var combs_json = {};
        // if (combs_json_text != null && combs_json_text != '') {
        //     combs_json = jQuery.parseJSON(combs_json_text);
        // }

        // let index = parseInt($("#detail_index_id").val());
        // let color = $("#detail_color_id").val();
        // let color_name = $("#detail_color_id option:selected").text();
        // let egg_type = $("#detail_eggtype_id").val();
        // let egg_type_name = $("#detail_eggtype_id option:selected").text();
        // let actual_combs = parseInt($("#detail_actualcombs_id").val());
        // let combs = parseInt($("#detail_combs_id").val());
        // let unit_price = parseInt($("#detail_unit_price_id").val());
        // let price = parseInt($("#detail_price_id").val());

        // var total_white_combs = parseInt($("#id_white_combs").val());
        // var total_red_combs = parseInt($("#id_red_combs").val());
        // var total_combs = parseInt($("#id_combs").val());
        // var total_price = parseInt($("#id_price").val());

        // if (egg_type != 'YEM') {
        //     if (color == null || color == '') {
        //         alert("Debe elegir el color del Huevo");
        //         $("#detail_color_id").focus();
        //         return;
        //     }
        // } else {
        //     color = '';
        // }

        // if (egg_type == null || egg_type == '') {
        //     alert("Debe elegir el tipo del Huevo");
        //     $("#detail_eggtype_id").focus();
        //     return;
        // }

        // if (combs == null || combs == '' || combs == 0) {
        //     alert("Debe indicar la cantidad de panales > 0");
        //     $("#detail_combs_id").focus();
        //     $("#detail_combs_id").val(0);
        //     $("#detail_price_id").val(0);
        //     return;
        // }

        // total_price += price;
        // total_combs += combs;
        // if (color == 'white') {
        //     total_white_combs += combs;
        // }
        // if (color == 'red') {
        //     total_red_combs += combs;
        // }

        // $("#id_white_combs").val(total_white_combs);
        // $("#id_red_combs").val(total_red_combs);
        // $("#id_combs").val(total_combs);
        // $("#id_price").val(total_price);

        // detail_json[index] = {
        //     'color': color,
        //     'egg_type': egg_type,
        //     'actual_combs': actual_combs,
        //     'combs': combs,
        //     'unit_price': unit_price,
        //     'price': price
        // }
        // $("#id_detail_json").val(JSON.stringify(detail_json));

        // let combs_key = color + "_" + egg_type;
        // if (!(combs_key in combs_json)) {
        //     combs_json[combs_key] = 0;
        // }
        // combs_json[combs_key] += combs;

        // $("#id_combs_json").val(JSON.stringify(combs_json));

        // var new_row = $('<tr id="rowdetail_' + index + '_id">');
        // new_row.append('<td class="text-end">' + index + '</td>');
        // new_row.append('<td class="text-start">' + egg_type_name + '</td>');
        // new_row.append('<td class="text-start">' + color_name + '</td>');
        // new_row.append('<td class="text-end">' + actual_combs + '</td>');
        // new_row.append('<td class="text-end">' + combs + '</td>');
        // new_row.append('<td class="text-end">' + unit_price + '</td>');
        // new_row.append('<td class="text-end">' + price + '</td>');
        // new_row.append('<td><button type="button" id="removebutton_' + index + '_id" name="removebutton_' + index + '" class="btn btn-table removebutton" onclick="removeItem(' + index + ');">-</button></td>');
        // new_row.append('</tr>');

        // $("#new_detail_tbody_id").append(new_row);

        // index += 1;

        // $("#detail_index_id").val(index);
        // $("#detail_color_id").val('');
        // $("#detail_eggtype_id").val('');
        // $("#detail_actualcombs_id").val(0);
        // $("#detail_combs_id").val(0);
        // $("#detail_unit_price_id").val(0);
        // $("#detail_price_id").val(0);
        // $("#detail_color_id").focus();
    });



});