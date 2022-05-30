
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit_or_credit', models.CharField(default='debit', max_length=20)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('curr_available_amount_if_credit_row', models.DecimalField(decimal_places=2, max_digits=20)),
                ('transaction_method_name', models.CharField(default=None, max_length=45)),
                ('transaction_method_remarks', models.CharField(default=None, max_length=90)),
                ('transaction_method_record_unique_id', models.CharField(max_length=200)),
                ('transaction_time', models.DateTimeField()),
                ('expiry_time_of_credited_amount', models.DateTimeField()),
                ('wallet_debit_record2wallet_credit_record', models.BigIntegerField(max_length=20)),
                ('wallet2user_details', models.BigIntegerField(max_length=20)),
                ('hmac_or_checksum', models.CharField(max_length=200)),
                ('is_deleted', models.CharField(max_length=45)),
            ],
        ),
    ]
