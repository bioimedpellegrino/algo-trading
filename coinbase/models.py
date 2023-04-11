from django.db import models


class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol

class TradingSettings(models.Model):
    is_active = models.BooleanField(default=True)
    sell_threshold = models.DecimalField(max_digits=5, decimal_places=4, default=0.05)  # 5% profit threshold
    stop_loss_threshold = models.DecimalField(max_digits=5, decimal_places=4, default=0.05)  # 5% stop-loss threshold
    initial_investment = models.DecimalField(max_digits=20, decimal_places=8)
    investment_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0.05)  # 5% investment per trade
    base_currency = models.CharField(max_length=10, default='EUR')
    quote_currency = models.ManyToManyField(Cryptocurrency)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def trading_symbols(self):
        return [f"{quote_currency.symbol}/{self.base_currency}" for quote_currency in self.quote_currencies.all()]
    
class Trade(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    symbol = models.CharField(max_length=10)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default=OPEN)
    investment_amount = models.DecimalField(max_digits=20, decimal_places=8)
    purchase_price = models.DecimalField(max_digits=20, decimal_places=8)
    sale_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    profit_loss = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)