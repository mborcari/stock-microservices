from datetime import timedelta, date
from django.db import models #pylint: disable=import-error
from django.core.exceptions import ValidationError #pylint: disable=import-error
from django.contrib.auth import get_user_model #pylint: disable=import-error
from django.urls import reverse #pylint: disable=import-error
from django.core.validators import MaxValueValidator, MinValueValidator #pylint: disable=import-error
from .utils import get_validate_business_data

from .choices import (
                    LIST_DATA_SOURCE,
                    LIST_CATEGORY,
                    )

class Stock(models.Model):
    """
    Stock model
    """

    code = models.SlugField(max_length=20, unique=True, verbose_name="Código")
    name = models.CharField(max_length=200, blank=False, verbose_name="Nome")
    category = models.CharField(max_length=200, choices=LIST_CATEGORY, verbose_name="Categoria")
    data_source = models.CharField(max_length=20, choices=LIST_DATA_SOURCE, verbose_name="Fonte de dados")

    last_close = models.CharField(
        max_length=10, verbose_name="Ultimo fechamento", default=0
    )

    last_change = models.CharField(
        max_length=10, verbose_name="Ultima variação", default=0
    )

    last_change_7_days = models.CharField(
        max_length=10, verbose_name="Variação 7 dias", default=0
    )

    last_change_30_days = models.CharField(
        max_length=10, verbose_name="Variação 30 dias", default=0
    )

    last_change_90_days = models.CharField(
        max_length=10, verbose_name="Variação 90 dias", default=0
    )

    last_change_180_days = models.CharField(
        max_length=10, verbose_name="Variação 180 dias", default=0
    )

    year_change = models.CharField(
        max_length=10, verbose_name="Variação Ano", default=0
    )

    def get_absolute_url(self):
        return reverse("core:stock-detail", args=[str(self.code)])

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Ativos financerios"
        constraints = [
            models.UniqueConstraint(
                fields=["code"], name="unique_code"
            )
        ]


class HistoricalStock(models.Model):
    """
        Historical Stocks
    """

    # date from stock records
    date = models.DateField(verbose_name="Data")
    # Stock relational
    stock_pk = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # May be null because dataset failed from datasource
    open_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor abertura",
        blank=True,
        null=True,
    )

    close_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor fechamento",
        blank=True,
        null=True,
    )

    high_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor máxima",
        blank=True,
        null=True,
    )

    low_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor mínima",
        blank=True,
        null=True,
    )

    volume_dialy = models.IntegerField()

    change_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Variação do dia",
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse("core:stock-detail", args=[str(self.id)])

    def __str__(self):
        return self.stock_pk.code + str(self.date)

    class Meta:
        verbose_name = "Histórico do ativo"
        constraints = [
            models.UniqueConstraint(
                fields=["stock_pk", "date"], name="unique_date_by_stock"
            )
        ]
