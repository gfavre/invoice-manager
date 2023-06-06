from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile

import factory.fuzzy
from faker import Faker
from PIL import Image

from ..models import Company


fake = Faker(locale="fr_CH")


def create_fake_image(width=300, height=300):
    fake = Faker()
    image = Image.new("RGB", (width, height), fake.safe_hex_color())
    image_io = BytesIO()
    image.save(image_io, format="JPEG")
    image_io.seek(0)
    return image_io


class CompanyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company", locale="fr_CH")
    address = factory.Faker("street_address", locale="fr_CH")
    zip_code = factory.Faker("postcode", locale="fr_CH")
    city = factory.Faker("city", locale="fr_CH")
    country = "CH"

    phone = factory.Faker("phone_number", locale="fr_CH")
    additional_phone = factory.Faker("phone_number", locale="fr_CH")

    email = factory.Faker("email", locale="fr_CH")
    website = factory.Faker("url", locale="fr_CH")
    vat_id = factory.Faker("uid", locale="fr_CH")

    name_for_bank = factory.LazyAttribute(lambda o: o.name)
    bank = factory.Faker("company", locale="fr_CH")
    bic = factory.Faker("swift11", locale="fr_CH")
    iban = factory.Faker("iban", locale="fr_CH")

    signature_text = factory.Faker("name", locale="fr_CH")
    signature_image = factory.LazyFunction(lambda: create_fake_image())
    invoice_note = factory.Faker("text", locale="fr_CH")

    from_email = factory.Faker("email", locale="fr_CH")
    thanks = factory.Faker("text", locale="fr_CH")

    class Meta:
        model = Company

    @factory.lazy_attribute
    def email_signature(self):
        fake = Faker(locale="fr_CH")
        company = fake.company()
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        website = fake.url()
        return f"{company}\n{name}\n{email}\nTel: {phone}\nWebsite: {website}"

    @factory.lazy_attribute
    def logo(self):
        image = create_fake_image()
        return InMemoryUploadedFile(
            image, None, fake.file_name(extension="jpg"), "image/jpeg", image.tell(), None
        )

    @factory.lazy_attribute
    def signature_image(self):
        image = create_fake_image()
        return InMemoryUploadedFile(
            image, None, fake.file_name(extension="jpg"), "image/jpeg", image.tell(), None
        )
