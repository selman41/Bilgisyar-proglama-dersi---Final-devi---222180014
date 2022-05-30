from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'debit_or_credit', 'transaction_amount', 'curr_available_amount_if_credit_row',
                  'remarks','transaction_method_record_unique_id','transaction_time','expiry_time_of_credited_amount',
                  'wallet_debit_record2wallet_credit_record','wallet2store_details','hmac_or_checksum','is_deleted')

        field = ('id','curr_available_amount_if_credit_row')
