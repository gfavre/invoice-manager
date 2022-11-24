import pandas

from beyondtheadmin.companies.models import Bank


URL = "https://www.mepa.ch/support/tools/schweizer-banken-bankleitzahlen-adressen-swift/"

dfs = pandas.read_html(URL)
# there is only one table on the page
df = dfs[0]
created_count = 0
update_count = 0

for elem in df.to_dict(orient="records"):
    # {'BLZ': 9000, 'Bank/Institut': 'PostFinance AG', 'Domizil': 'Mingerstrasse 20', 'Postadresse': nan,
    # 'PLZ': '3030', 'Ort': 'Bern', 'Landcode': nan, 'Postkonto': nan, 'SWIFT': 'POFICHBEXXX'}
    bank, created = Bank.objects.update_or_create(
        code=elem["BLZ"],
        defaults={
            "name": elem["Bank/Institut"],
            "address": elem["Domizil"],
            "zip_code": elem["PLZ"],
            "city": elem["Ort"],
            "country": elem["Landcode"] if str(elem["Landcode"]) != "nan" else "CH",
            "swift": elem["SWIFT"],
        },
    )
    if created:
        created_count += 1
    else:
        update_count += 1


print(f"Created {created_count} banks; updated {update_count} banks.")
