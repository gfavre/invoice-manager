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
    switch ($(this).val()) {
      case 'company':
        $('#person_infos').addClass('d-none');
        $('#company_infos').removeClass('d-none');
        break
      case 'person':
        $('#person_infos').removeClass('d-none');
        $('#company_infos').addClass('d-none');
        break
    }
  }


  let clientRadios = document.querySelectorAll("input[name='client_type']");
  Array.prototype.forEach.call(clientRadios, function (radio){
    radio.addEventListener('change', toggleForm)
  })

  // initial setup
  $("#id_client_type_0").change()

})(jQuery); // End of use strict;
