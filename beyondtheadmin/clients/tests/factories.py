from django.utils.text import slugify

import factory.fuzzy

from ..models import Client


class ClientFactory(factory.django.DjangoModelFactory):
    company_name = factory.Faker("company", locale="fr_CH")

    contact_first_name = factory.Faker("first_name", locale="fr_CH")
    contact_last_name = factory.Faker("last_name", locale="fr_CH")
    contact_email = factory.Faker("email", locale="fr_CH")

    address = factory.Faker("street_address", locale="fr_CH")
    zip_code = factory.Faker("postcode", locale="fr_CH")
    city = factory.Faker("city", locale="fr_CH")
    country = "CH"

    language = factory.fuzzy.FuzzyChoice(["fr", "de", "it", "en"])
    currency = factory.fuzzy.FuzzyChoice(["CHF", "EUR"])

    default_hourly_rate = factory.fuzzy.FuzzyDecimal(50, 300, 2)
    slug = factory.LazyAttribute(lambda o: slugify(o.company_name or o.contact_last_name)[:15])

    company = factory.SubFactory("beyondtheadmin.companies.tests.factories.CompanyFactory")

    class Meta:
        model = Client
