from django.db import models


ORDER_CHOICES = (
    ('awaiting_payment', 'Awaiting payment'),
    ('paid', 'Paid'),
    ('expired', 'Expired'),
    ('cancelled', 'Cancelled'),
)


class Order(models.Model):
    full_price = models.DecimalField(decimal_places=2, max_digits=12)
    discount = models.DecimalField(decimal_places=2, max_digits=12)
    status = models.CharField(choices=ORDER_CHOICES, default='awaiting_payment', max_length=255)
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.price)

    @property
    def price(self):
        return self.full_price - self.discount
