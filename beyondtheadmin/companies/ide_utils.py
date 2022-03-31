"""
IDE: Le registre IDE tenu par l'OFS est une banque de données centrale servant exclusivement à l'identification des
entreprises. Les données qu'il contient se limitent au minimum requis pour l'identification.
"""
import re

from zeep import Client
from beyondtheadmin.companies.serializers import IDECompanySerializer

TEST_URL = 'https://www.uid-wse-a.admin.ch/V5.0/PublicServices.svc?wsdl'
PROD_URL = 'https://www.uid-wse.admin.ch/V5.0/PublicServices.svc?wsdl'

VAT_REGISTERED = '2'

# nom de l'entreprise: uidEntitySearchResultItem

def format_uid(category, uid):
    return '{}-{}'.format(category, '.'.join(re.findall('...',  str(uid))))


def convert_search_item_to_company_data(result_item):
    identification_node = result_item.organisation.organisation.organisationIdentification
    uid = format_uid(identification_node.uid.uidOrganisationIdCategorie, identification_node.uid.uidOrganisationId)
    name = identification_node.organisationName
    address_node = result_item.organisation.organisation.address[0]
    try:
        street = address_node.street
        house_number = address_node.houseNumber
        if not street:
            address = ''
        else:
            if house_number:
                address = '{} {}'.format(street, house_number)
            else:
                address = street
    except AttributeError:
        address = ''
    try:
        zip_code = address_node._value_1[0]['swissZipCode']
    except (IndexError, AttributeError):
        zip_code = ''
    try:
        city = address_node.town
    except AttributeError:
        city = ''
    vat_id = None
    try:
        vat_node = result_item.organisation.vatRegisterInformation
        if vat_node.vatStatus == VAT_REGISTERED:
            vat_id = format_uid(vat_node.uidVat.uidOrganisationIdCategorie, vat_node.uidVat.uidOrganisationId)
    except AttributeError:
        pass
    return {
        "uid": uid, "name": name, "address": address, "zip_code": zip_code, "city": city, "vat_id": vat_id
    }


def search_company(company_name, client_url=PROD_URL):
    """
    Search company by name.
    :param company_name:
    :param client_url:
    :return:
    """
    client = Client(wsdl=client_url)
    result = client.service.Search(
        searchParameters={"uidEntitySearchParameters": company_name},
        config={"maxNumberOfRecords": "10", "searchMode": "Auto", "searchNameAndAddressHistory": False}
    )
    companies = []
    if result is not None:
        companies = [convert_search_item_to_company_data(item) for item in result.uidEntitySearchResultItem]
    return companies
