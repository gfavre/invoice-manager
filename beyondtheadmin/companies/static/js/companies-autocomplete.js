 $(document).ready(function () {
      $('#id_name').autoComplete({
        resolverSettings: {
          url: $('#app').data('autocompleteUrl'),
        },
        formatResult: function (company) {
          return {id: company.uid, text: company.name + ', ' + company.city};
        },

      });

      $('#id_name').on('autocomplete.select', function (evt, item) {
        evt.preventDefault();
        $.ajax({
          headers: {"X-CSRFToken": "{{ csrf_token }}"},
          url: $('#app').data('companyDetailUrl'),
          data: {uid: item.uid},
          type: 'GET',
          success: function (companyDetail) {
            $('#id_name').val(companyDetail.name);
            $('#id_vat_id').val(companyDetail.vat_id);
            $('#id_address').val(companyDetail.address);
            $('#id_city').val(companyDetail.city);
            $('#id_zip_code').val(companyDetail.zip_code);
            $('#id_country').val('CH');
            if ($('#id_name_for_bank').val() === '') {
              $('#id_name_for_bank').val(companyDetail.name);
            }
          },
        })
      });
    });
