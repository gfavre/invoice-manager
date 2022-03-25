"""
IDE: Le registre IDE tenu par l'OFS est une banque de données centrale servant exclusivement à l'identification des
entreprises. Les données qu'il contient se limitent au minimum requis pour l'identification.
"""
import re

from zeep import Client


TEST_URL = 'https://www.uid-wse-a.admin.ch/V5.0/PublicServices.svc?wsdl'
PROD_URL = 'https://www.uid-wse.admin.ch/V5.0/PublicServices.svc?wsdl'

VAT_REGISTERED = '2'

# nom de l'entreprise: uidEntitySearchResultItem

def format_uid(category, uid):
    return '{}-{}'.format(category, '.'.join(re.findall('...',  str(uid))))


def uidEntitySearchResultItemToCompany(result_item):
    identification_node = result_item.organisation.organisation.organisationIdentification
    uid = format_uid(identification_node.uid.uidOrganisationIdCategorie, identification_node.uid.uidOrganisationId)
    name = identification_node.organisationName
    address_node = result_item.organisation.organisation.address[0]
    address = address_node.street + address_node.houseNumber
    zip_code = address_node._value_1.swissZipCode
    city = address_node.town
    vat_id = None
    try:
        vat_node = result_item.organisation.vatRegisterInformation
        if vat_node.vatStatus == VAT_REGISTERED:
            vat_id = format_uid(vat_node.uidVat.uidOrganisationIdCategorie, vat_node.uidVat.uidOrganisationId)
    except AttributeError:
        pass




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
    companies = result.uidEntitySearchResultItem
    return result

client = Client(wsdl=PROD_URL)
client.service.Search(
    searchParameters={"uidEntitySearchParameters": "Beyond the wall"},
    config={"maxNumberOfRecords": "10", "searchMode": "Auto", "searchNameAndAddressHistory": False})


ns3_factory = client.type_factory("ns0")
        payments = []
        booking_entries = booking.entries.all().exclude(
            status__in=[BookingEntry.STATUS.sent, BookingEntry.STATUS.lt_min_amount]
        )
        for booking_entry in booking_entries:
            payment_vat = None
            payments.append(
                ns3_factory.PaymentV3(
                    None,
                    booking_entry.credited_account_number,
                    booking_entry.debited_account_number,
                    None,  # transaction_hash
                    DEFAULT_PAYMENT_TYPE,  # PaymentType
                    truncate(booking_entry.amount, 4),  # FIXME: 4 should be a setting
                    booking_entry.currency.code,
                    None,
                    None,
                    payment_vat,
                )
            )
        payment_array = ns3_factory.ArrayOfPaymentV3(payments)
        logger.info("Sending Booking: {}".format(payment_array))
        results = client.service.SavePayments(
            callContext={"Mandator": settings.FINSTAR_API_MANDATOR},
            payments=payment_array,
        )
