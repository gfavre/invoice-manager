import re

from django.conf import settings

import requests.auth


ZEFIX_SEARCH_URL = "https://www.zefix.admin.ch/ZefixPublicREST/api/v1/company/search"


def format_uid(uid):
    numbers = uid.split("CHE")[1]
    return "CHE-" + ".".join(re.findall("...", str(numbers)))


def convert_search_item_to_company_data(result_item):
    vat_id = format_uid(result_item["uid"])
    address = ""
    zip_code = ""
    city = result_item.get("legalSeat")
    print(result_item)
    if "address" in result_item:
        city = result_item["address"].get("city")
        address = (
            result_item["address"].get("street") + " " + result_item["address"].get("houseNumber")
        ).strip()
        zip_code = result_item["address"].get("swissZipCode")

    return {
        "uid": result_item.get("uid"),
        "name": result_item.get("name"),
        "address": address,
        "zip_code": zip_code,
        "city": city,
        "vat_id": vat_id,
    }


def search_zefix(company_name):
    username = settings.ZEFIX_USERNAME
    password = settings.ZEFIX_PASSWORD
    data = {
        "name": company_name,
        "activeOnly": True,
    }
    response = requests.post(
        ZEFIX_SEARCH_URL,
        json=data,
        auth=requests.auth.HTTPBasicAuth(username, password),
    )
    if response.status_code == 200:
        return [
            convert_search_item_to_company_data(result_item) for result_item in response.json()
        ]
    return []


def get_detail(company_uid):
    username = settings.ZEFIX_USERNAME
    password = settings.ZEFIX_PASSWORD
    url = f"https://www.zefix.admin.ch/ZefixPublicREST/api/v1/company/uid/{company_uid}"
    response = requests.get(url=url, auth=requests.auth.HTTPBasicAuth(username, password))
    if response.status_code == 200:
        companies_list = response.json()
        if len(companies_list) > 0:
            return convert_search_item_to_company_data(companies_list[0])

    return None
