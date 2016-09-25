from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from konfera.models import Order
from konfera.models.speaker import TITLE_UNSET, TITLE_CHOICES


TICKET_STATUS = (
    ('requested', 'Requested'),
    ('registered', 'Registered'),
    ('checked-in', 'Checked-in'),
    ('cancelled', 'Cancelled'),
)


class Ticket(models.Model):
    type = models.ForeignKey('TicketType')
    discount_code = models.ForeignKey('DiscountCode', blank=True, null=True)
    status = models.CharField(choices=TICKET_STATUS, max_length=32)
    title = models.CharField(choices=TITLE_CHOICES, max_length=4, default=TITLE_UNSET)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField()
    order = models.ForeignKey('Order', null=True, blank=True)

    def __str__(self):
        return '{title} {first_name} {last_name}'.format(
            title=dict(TITLE_CHOICES)[self.title],
            first_name=self.first_name,
            last_name=self.last_name
        ).strip()


@receiver(post_save, sender=Ticket, dispatch_uid='konfera.models.Ticket.post_save_contact')
def post_save_ticket(sender, instance, created, **kwargs):
    if created:
        price = instance.type.price
        discount = 0
        if instance.discount_code:
            discount = price / 100 * instance.discount_code.discount
        order = Order(full_price=price, discount=discount)
        order.save()

        instance.order = order
        instance.save()
