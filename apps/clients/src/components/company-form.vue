<template>



    <div id="div_id_company_name" class="form-group">
      <label for="id_company_name" class="requiredField">
        Nom de l'entreprise
        <span class="asteriskField">*</span>
      </label>
      <div>
        <input type="text" name="company_name" maxlength="255" data-search-url="/api/companies/"
               data-detail-url="/api/company-detail/" class="textinput textInput form-control" id="id_company_name"
               required="">
      </div>
    </div>
    <div id="div_id_address" class="form-group"><label for="id_address" class="">
      Adresse
    </label>
      <div><textarea name="address" cols="40" rows="2" class="textarea form-control" id="id_address"></textarea></div>
    </div>
    <div class="form-row ">
      <div class="col-md-4">
        <div id="div_id_country" class="form-group"><label for="id_country" class="">
          Pays
        </label>
          <div><select name="country" class="lazyselect custom-select" id="id_country">
            <option value="CH" selected="">Suisse</option>
            <option value="">---</option>
            <option value="AF">Afghanistan</option>
            <option value="ZA">Afrique du Sud</option>
            <option value="AL">Albanie</option>
            <option value="DZ">Algérie</option>
            <option value="DE">Allemagne</option>
            <option value="AD">Andorre</option>
            <option value="AO">Angola</option>
            <option value="AI">Anguilla</option>
            <option value="AQ">Antarctique</option>
            <option value="AG">Antigua-et-Barbuda</option>
            <option value="SA">Arabie Saoudite</option>
            <option value="AR">Argentine</option>
            <option value="AM">Arménie</option>
            <option value="AW">Aruba</option>
            <option value="AU">Australie</option>
            <option value="AT">Autriche</option>
            <option value="AZ">Azerbaïdjan</option>
            <option value="BS">Bahamas</option>
            <option value="BH">Bahreïn</option>
            <option value="BD">Bangladesh</option>
            <option value="BB">Barbade</option>
            <option value="BE">Belgique</option>
            <option value="BZ">Bélize</option>
            <option value="BJ">Bénin</option>
            <option value="BM">Bermudes</option>
            <option value="BT">Bhoutan</option>
            <option value="BY">Biélorussie</option>
            <option value="MM">Birmanie</option>
            <option value="BO">Bolivie</option>
            <option value="BQ">Bonaire, Saint Eustache et Saba</option>
            <option value="BA">Bosnie-Herzégovine</option>
            <option value="BW">Botswana</option>
            <option value="BR">Brésil</option>
            <option value="BN">Bruneï Darussalam</option>
            <option value="BG">Bulgarie</option>
            <option value="BF">Burkina Faso</option>
            <option value="BI">Burundi</option>
            <option value="KH">Cambodge</option>
            <option value="CM">Cameroun</option>
            <option value="CA">Canada</option>
            <option value="CV">Cap-Vert</option>
            <option value="CL">Chili</option>
            <option value="CN">Chine</option>
            <option value="CY">Chypre</option>
            <option value="CO">Colombie</option>
            <option value="KM">Comores</option>
            <option value="CG">Congo</option>
            <option value="KP">Corée du Nord</option>
            <option value="KR">Corée du Sud</option>
            <option value="CR">Costa Rica</option>
            <option value="CI">Côte d'Ivoire</option>
            <option value="HR">Croatie</option>
            <option value="CU">Cuba</option>
            <option value="CW">Curaçao</option>
            <option value="DK">Danemark</option>
            <option value="DJ">Djibouti</option>
            <option value="DM">Dominique</option>
            <option value="EG">Égypte</option>
            <option value="AE">Émirats arabes unis</option>
            <option value="EC">Équateur</option>
            <option value="ER">Érythrée</option>
            <option value="ES">Espagne</option>
            <option value="EE">Estonie</option>
            <option value="SZ">Eswatini (République d')</option>
            <option value="US">États-Unis d'Amérique</option>
            <option value="ET">Éthiopie</option>
            <option value="FJ">Fidji</option>
            <option value="FI">Finlande</option>
            <option value="FR">France</option>
            <option value="GA">Gabon</option>
            <option value="GM">Gambie</option>
            <option value="GE">Géorgie</option>
            <option value="GS">Géorgie du Sud-et-les Îles Sandwich du Sud</option>
            <option value="GH">Ghana</option>
            <option value="GI">Gibraltar</option>
            <option value="GR">Grèce</option>
            <option value="GD">Grenade</option>
            <option value="GL">Groenland</option>
            <option value="GP">Guadeloupe</option>
            <option value="GU">Guam</option>
            <option value="GT">Guatémala</option>
            <option value="GG">Guernesey</option>
            <option value="GN">Guinée</option>
            <option value="GQ">Guinée équatoriale</option>
            <option value="GW">Guinée-Bissau</option>
            <option value="GY">Guyane</option>
            <option value="GF">Guyane française</option>
            <option value="HT">Haïti</option>
            <option value="HN">Honduras</option>
            <option value="HK">Hong Kong</option>
            <option value="HU">Hongrie</option>
            <option value="BV">Île Bouvet</option>
            <option value="CX">Île Christmas</option>
            <option value="IM">Île de Man</option>
            <option value="SJ">Île Jan Mayen</option>
            <option value="NF">Île Norfolk</option>
            <option value="PN">Île Pitcairn</option>
            <option value="AX">Îles Åland</option>
            <option value="KY">Îles Caïmans</option>
            <option value="CC">Îles Cocos</option>
            <option value="CK">Îles Cook</option>
            <option value="FO">Îles Féroé</option>
            <option value="HM">Îles Heard-et-MacDonald</option>
            <option value="FK">Îles Malouines</option>
            <option value="MP">Îles Mariannes du Nord</option>
            <option value="MH">Îles Marshal</option>
            <option value="UM">Îles mineures éloignées des États-Unis</option>
            <option value="TC">Îles Turques-et-Caïques</option>
            <option value="VG">Îles Vierges britanniques</option>
            <option value="VI">Îles Vierges des États-Unis</option>
            <option value="IN">Inde</option>
            <option value="ID">Indonésie</option>
            <option value="IQ">Irak</option>
            <option value="IR">Iran (République Islamique d')</option>
            <option value="IE">Irlande</option>
            <option value="IS">Islande</option>
            <option value="IL">Israël</option>
            <option value="IT">Italie</option>
            <option value="JM">Jamaïque</option>
            <option value="JP">Japon</option>
            <option value="JE">Jersey</option>
            <option value="JO">Jordanie</option>
            <option value="KZ">Kazakhstan</option>
            <option value="KE">Kenya</option>
            <option value="KG">Kirghizistan</option>
            <option value="KI">Kiribati</option>
            <option value="KW">Koweït</option>
            <option value="LS">Lesotho</option>
            <option value="LV">Lettonie</option>
            <option value="LB">Liban</option>
            <option value="LR">Libéria</option>
            <option value="LY">Libye</option>
            <option value="LI">Liechtenstein</option>
            <option value="LT">Lituanie</option>
            <option value="LU">Luxembourg</option>
            <option value="MO">Macao</option>
            <option value="MG">Madagascar</option>
            <option value="MY">Malaisie</option>
            <option value="MW">Malawi</option>
            <option value="MV">Maldives</option>
            <option value="ML">Mali</option>
            <option value="MT">Malte</option>
            <option value="MA">Maroc</option>
            <option value="MQ">Martinique</option>
            <option value="MU">Maurice</option>
            <option value="MR">Mauritanie</option>
            <option value="YT">Mayotte</option>
            <option value="MX">Mexique</option>
            <option value="FM">Micronésie (États Fédérés de)</option>
            <option value="MD">Moldavie</option>
            <option value="MC">Monaco</option>
            <option value="MN">Mongolie</option>
            <option value="ME">Monténégro</option>
            <option value="MS">Montserrat</option>
            <option value="MZ">Mozambique</option>
            <option value="NA">Namibie</option>
            <option value="NR">Nauru</option>
            <option value="NP">Népal</option>
            <option value="NI">Nicaragua</option>
            <option value="NE">Niger</option>
            <option value="NG">Nigeria</option>
            <option value="NU">Niue</option>
            <option value="NO">Norvège</option>
            <option value="NC">Nouvelle-Calédonie</option>
            <option value="NZ">Nouvelle-Zélande</option>
            <option value="OM">Oman</option>
            <option value="UG">Ouganda</option>
            <option value="UZ">Ouzbékistan</option>
            <option value="PK">Pakistan</option>
            <option value="PW">Palaos</option>
            <option value="PS">Palestine, État de</option>
            <option value="PA">Panama</option>
            <option value="PG">Papouasie-Nouvelle-Guinée</option>
            <option value="PY">Paraguay</option>
            <option value="NL">Pays-Bas</option>
            <option value="PE">Pérou</option>
            <option value="PH">Philippines</option>
            <option value="PL">Pologne</option>
            <option value="PF">Polynésie française</option>
            <option value="PR">Porto Rico</option>
            <option value="PT">Portugal</option>
            <option value="QA">Qatar</option>
            <option value="CF">République centrafricaine</option>
            <option value="MK">République de Macédoine du Nord</option>
            <option value="CD">République démocratique du Congo</option>
            <option value="LA">République démocratique populaire lao</option>
            <option value="DO">République dominicaine</option>
            <option value="CZ">République tchèque</option>
            <option value="RE">Réunion, La</option>
            <option value="RO">Roumanie</option>
            <option value="GB">Royaume-Uni</option>
            <option value="RU">Russie</option>
            <option value="RW">Rwanda</option>
            <option value="EH">Sahara occidental</option>
            <option value="BL">Saint Barthélemy</option>
            <option value="KN">Saint-Christophe-et-Niévès</option>
            <option value="SM">Saint-Marin</option>
            <option value="MF">Saint-Martin (Antilles françaises)</option>
            <option value="SX">Saint-Martin (Royaume des Pays-Bas)</option>
            <option value="PM">Saint-Pierre-et-Miquelon</option>
            <option value="VA">Saint-Siège</option>
            <option value="VC">Saint-Vincent-et-les-Grenadines</option>
            <option value="SH">Sainte-Hélène, Ascension et Tristan da Cunha</option>
            <option value="LC">Sainte-Lucie</option>
            <option value="SB">Salomon</option>
            <option value="SV">Salvador</option>
            <option value="WS">Samoa</option>
            <option value="AS">Samoa américaines</option>
            <option value="ST">Sao Tomé-et-Principe</option>
            <option value="SN">Sénégal</option>
            <option value="RS">Serbie</option>
            <option value="SC">Seychelles</option>
            <option value="SL">Sierra Leone</option>
            <option value="SG">Singapour</option>
            <option value="SK">Slovaquie</option>
            <option value="SI">Slovénie</option>
            <option value="SO">Somalie</option>
            <option value="SD">Soudan</option>
            <option value="SS">Soudan du Sud</option>
            <option value="LK">Sri Lanka</option>
            <option value="SE">Suède</option>
            <option value="CH">Suisse</option>
            <option value="SR">Suriname</option>
            <option value="SY">Syrie</option>
            <option value="TJ">Tadjikistan</option>
            <option value="TW">Taïwan</option>
            <option value="TZ">Tanzanie</option>
            <option value="TD">Tchad</option>
            <option value="TF">Terres australes et antarctiques françaises</option>
            <option value="IO">Territoire britannique de l'océan Indien</option>
            <option value="TH">Thaïlande</option>
            <option value="TL">Timor Oriental</option>
            <option value="TG">Togo</option>
            <option value="TK">Tokelau</option>
            <option value="TO">Tonga</option>
            <option value="TT">Trinidad et Tobago</option>
            <option value="TN">Tunisie</option>
            <option value="TM">Turkménistan</option>
            <option value="TR">Turquie</option>
            <option value="TV">Tuvalu</option>
            <option value="UA">Ukraine</option>
            <option value="UY">Uruguay</option>
            <option value="VU">Vanuatu</option>
            <option value="VE">Vénézuéla (République Bolivarienne du)</option>
            <option value="VN">Viêt Nam</option>
            <option value="WF">Wallis et Futuna</option>
            <option value="YE">Yémen</option>
            <option value="ZM">Zambie</option>
            <option value="ZW">Zimbabwe</option>

          </select></div>
        </div>
      </div>
      <div class="col-md-2">
        <div id="div_id_zip_code" class="form-group"><label for="id_zip_code" class="">
          Code postal
        </label>
          <div><input type="text" name="zip_code" maxlength="10" class="textinput textInput form-control"
                      id="id_zip_code"></div>
        </div>
      </div>
      <div class="col-md ">
        <div id="div_id_city" class="form-group"><label for="id_city" class="">
          Localité
        </label>
          <div><input type="text" name="city" maxlength="255" class="textinput textInput form-control" id="id_city">
          </div>
        </div>
      </div>
    </div>
    <hr>
    <div class="form-row ">
      <div class="col-md ">
        <div id="div_id_contact_first_name" class="form-group"><label for="id_contact_first_name" class="">
          Prénom du contact
        </label>
          <div><input type="text" name="contact_first_name" maxlength="255" class="textinput textInput form-control"
                      id="id_contact_first_name"></div>
        </div>
      </div>
      <div class="col-md ">
        <div id="div_id_contact_last_name" class="form-group"><label for="id_contact_last_name" class="">
          Nom du contact
        </label>
          <div><input type="text" name="contact_last_name" maxlength="255" class="textinput textInput form-control"
                      id="id_contact_last_name"></div>
        </div>
      </div>
    </div>
    <div id="div_id_contact_email" class="form-group"><label for="id_contact_email" class="">
      E-mail de contact
    </label>
      <div><input type="email" name="contact_email" maxlength="254" class="emailinput form-control"
                  id="id_contact_email"></div>
    </div>
</template>

<script>

export default {
  name: "CompanyForm",

}
</script>

<style scoped>

</style>
