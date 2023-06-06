from datetime import timedelta

from django.utils.timezone import now

import factory.fuzzy

from ..models import Invoice, InvoiceLine


class InvoiceFactory(factory.django.DjangoModelFactory):
    company = factory.SubFactory("beyondtheadmin.companies.tests.factories.CompanyFactory")
    client = factory.SubFactory("beyondtheadmin.clients.tests.factories.ClientFactory")

    due_date = factory.Faker("date_between", start_date="+10d", end_date="+60d")
    displayed_date = factory.LazyAttribute(lambda o: now().date())
    title = factory.Faker("bs")
    description = factory.Faker("text")
    period_start = factory.Faker("date_between", start_date="-1y", end_date="-1m")
    period_end = factory.LazyAttribute(lambda o: o.period_start + timedelta(days=30))
    created_by = factory.SubFactory("beyondtheadmin.users.tests.factories.UserFactory")

    class Meta:
        model = Invoice

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = model_class(**kwargs)
        instance.save(generate_code=True)
        return instance


class InvoiceLineFactory(factory.django.DjangoModelFactory):
    invoice = factory.SubFactory(InvoiceFactory)
    description = factory.Faker("bs")
    quantity = factory.fuzzy.FuzzyDecimal(1, 10)
    unit = factory.fuzzy.FuzzyChoice(["h", "nb"])
    price_per_unit = factory.fuzzy.FuzzyInteger(50, 1000)

    class Meta:
        model = InvoiceLine
