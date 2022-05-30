
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_auto_20160123_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='expiry_time_of_credited_amount',
            field=models.DateTimeField(default=datetime.datetime(2030, 1, 1, 0, 0)),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='transaction_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 23, 8, 56, 27, 543468)),
        ),
    ]
