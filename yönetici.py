from django.contrib import admin
from .models import Wallet
# Modellerinizi buraya kaydedin.
class WalletAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Transaction Type:',{'fields':['debit_or_credit']}),
        ('Transaction Amount:',{'fields':['transaction_amount']}),
        ('Current Amount(only Credit):',{'fields':['curr_available_amount_if_credit_row']}),
        ('Remarks:',{'fields':['remarks']}),
        ('Transaction Unique ID:',{'fields':['transaction_method_record_unique_id']}),
        ('Transaction Time:',{'fields':['transaction_time']}),
        ('Expiry Time:',{'fields':['expiry_time_of_credited_amount']}),
        ('Linked Record ID',{'fields':['wallet_debit_record2wallet_credit_record']}),
        ('Store ID:',{'fields':['wallet2store_details']}),
        ('HMAC/CHECKSUM:',{'fields':['hmac_or_checksum']}),
        ('Status(0 --> Not deleted, 1 --> Deleted ):',{'fields':['is_deleted']}),

    ]

admin.site.register(Wallet,WalletAdmin)
