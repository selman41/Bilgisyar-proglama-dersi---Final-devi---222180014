from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
from decimal import Decimal
# Modellerinizi burada oluşturun.

class Wallet(models.Model):
    debit_or_credit = models.BooleanField(default=False)
    transaction_amount = models.FloatField(default=0.0)
    curr_available_amount_if_credit_row = models.FloatField(default=0.0)
    remarks = models.CharField(max_length=90,default=None)
    transaction_method_record_unique_id = models.CharField(max_length = 200)
    transaction_time = models.DateTimeField(default=datetime.datetime.now)
    expiry_time_of_credited_amount = models.DateTimeField(default=datetime.datetime(year=2030, month=1, day=1, hour=00, minute=00,second=00),blank=True)
    wallet_debit_record2wallet_credit_record = models.ForeignKey('self',default = None,null=True)
    wallet2store_details = models.BigIntegerField(default=0)
    hmac_or_checksum = models.CharField(max_length=200,default='temp_HMAC',blank=True, null=True)
    is_deleted = models.CharField(max_length=45)

    def __str__(self):
        return self.id
    def __unicode__(self):
            return str(self.id)
