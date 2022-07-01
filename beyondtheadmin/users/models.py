from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import stripe


class User(AbstractUser):
    """Default user for beyondtheadmin."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    companies = models.ManyToManyField(verbose_name=_("Companies"), to='companies.Company',
                                       related_name='users')
    clients = models.ManyToManyField(verbose_name=_("Clients"), to='clients.Client', related_name='users')
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    def create_stripe_customer(self):
        """Create stripe customer for user.

        Returns:
            str: Stripe customer id.

        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_customer = stripe.Customer.create(
            email=self.email, name=f"{self.first_name} {self.last_name}", description=str(self.id)
        )
        self.stripe_customer_id = stripe_customer.id
        self.save()
        return self.stripe_customer_id

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        """Create stripe customer for user."""
        super().save(*args, **kwargs)
        if not self.stripe_customer_id:
            from .tasks import create_stripe_customer
            transaction.on_commit(lambda x: create_stripe_customer(self.id))

    def __str__(self):
        """Return username."""
        return self.username
