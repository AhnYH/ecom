from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class Invoice(TimeStampedModel):
    NOT_PAID, PAID = 'Not Paid', 'Paid'
    state_choices = (
        (NOT_PAID, _('Not Paid')),
        (PAID, _('Paid')),
    )
    PREPAID, POSTPAID, NA = 'Prepaid', 'Postpaid', 'Not applicable'
    type_choices = (
        (PREPAID, _('Prepaid')),
        (POSTPAID, _('Postpaid')),
        (NA, _('Not applicable'))
    )
    PERCENTAGE, FIXED = 'Percentage', 'Fixed'
    discount_type_choices = (
        (PERCENTAGE, _('Percentage')),
        (FIXED, _('Fixed'))
    )
    basket = models.ForeignKey('basket.Basket', null=True, blank=True)
    order = models.ForeignKey('order.Order', null=True, blank=False)
    business_client = models.ForeignKey('core.BusinessClient', null=True, blank=False)
    state = models.CharField(max_length=255, default=NOT_PAID, choices=state_choices)

    number = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, default=PREPAID, choices=type_choices, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    discount_type = models.CharField(
        max_length=255, default=PERCENTAGE, choices=discount_type_choices, null=True, blank=True
    )
    discount_value = models.PositiveIntegerField(null=True, blank=True)
    tax_deducted_source = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        null=True, blank=True
    )

    history = HistoricalRecords()

    @property
    def total(self):
        """Total amount paid for this Invoice"""
        return self.order.total_incl_tax

    @property
    def client(self):
        """Client for this invoice"""
        return self.business_client
