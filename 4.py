
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_auto_20160123_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='transaction_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 23, 9, 9, 6, 511254)),
        ),
    ]
