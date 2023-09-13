import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone

import biocrust_app.datasets.models


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name="datasets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date created"
                    ),
                ),
                (
                    "dataset_name",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Name of Data Set"
                    ),
                ),
            ],
            options={
                "verbose_name": "dataset",
                "verbose_name_plural": "datasets",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
