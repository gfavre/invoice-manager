from collections import namedtuple
from django.utils.translation import gettext_lazy as _


Product = namedtuple('Product', 'name, code, price, description')

MONTHLY_PLAN = 'prod_LqTgExyg7L3CCh'
YEARLY_PLAN = 'prod_LqTixak7nB0k5n'
# Prices on stripe are in cents
PRODUCTS = {
    MONTHLY_PLAN: Product(name=_("Monthly plan"), code=MONTHLY_PLAN, price=600,
                          description=_('Recurring subscription, renewed every month')),
    YEARLY_PLAN: Product(name=_("Yearly plan"), code='prod_LqTixak7nB0k5n', price=6000,
                         description=_('Recurring subscription, renewed every year'))
}
