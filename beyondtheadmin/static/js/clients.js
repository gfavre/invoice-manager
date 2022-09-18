/* Project specific Javascript goes here. */
(function ($) {
  "use strict"; // Start of use strict

  let $companyField = $('#id_company_name');
  $companyField.autoComplete({
    resolverSettings: {
      url: $companyField.data('url'),
    },
    formatResult: function (company) {
      return {id: company.uid, text: company.name + ', ' + company.city};
    }
  });

  $companyField.on('autocomplete.select', function (evt, item) {
    evt.preventDefault();
    $('#id_company_name').val(item.name);
    $('#id_address').val(item.address);
    $('#id_city').val(item.city);
    $('#id_zip_code').val(item.zip_code);
    $('#id_country').val('CH');
  });

  let toggleForm = function (){
    switch ($("input[name=client_type]:checked").val()) {
      case 'company':
        $('#person_infos').addClass('d-none');
        $('#company_infos').removeClass('d-none');
        $('#company_infos #id_company_name').prop('required', true);
        $('#company_infos label[for=id_company_name]').addClass('requiredField');
        $('<span class="asteriskField">*</span>').appendTo($('#company_infos label[for=id_company_name]'));

        $('#person_infos #id_first_name').prop('required', false);
        $('#person_infos label[for=id_first_name]').removeClass('requiredField');
        $('#person_infos label[for=id_first_name] .asteriskField').remove();
        $('#person_infos #id_last_name').prop('required', false);
        $('#person_infos label[for=id_last_name]').removeClass('requiredField');
        $('#person_infos label[for=id_last_name] .asteriskField').remove();
        break
      case 'person':
        $('#person_infos').removeClass('d-none');
        $('#company_infos').addClass('d-none');
        $('#person_infos #id_first_name').prop('required', true);
        $('#person_infos label[for=id_first_name]').addClass('requiredField');
        $('<span class="asteriskField">*</span>').appendTo($('#person_infos label[for=id_first_name]'));
        $('#person_infos #id_last_name').prop('required', true);
        $('#person_infos label[for=id_last_name]').addClass('requiredField');
        $('<span class="asteriskField">*</span>').appendTo($('#person_infos label[for=id_last_name]'));

        $('#company_infos #id_company_name').prop('required', false);
        $('#company_infos label[for=id_company_name]').removeClass('requiredField');
        $('#company_infos label[for=id_company_name] .asteriskField').remove();
        break
    }
  }

  let clientRadios = document.querySelectorAll("input[name='client_type']");
  Array.prototype.forEach.call(clientRadios, function (radio){
    radio.addEventListener('change', toggleForm)
  })

  // initial setup
  toggleForm();
})(jQuery); // End of use strict;
