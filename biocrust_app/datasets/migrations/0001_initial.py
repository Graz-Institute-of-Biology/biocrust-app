import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone

import biocrust_app.datasets.models


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name="Dataset_Model",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dataset_name", models.CharField(blank=True, max_length=255)),
                ("slug", models.SlugField()),
                ("dataset_created", models.DateTimeField(auto_now_add=True)),
                ("coordinates", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("dataset_type", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "ordering": ("-dataset_created",),
            },
        ),
        migrations.CreateModel(
            name="Image_Model",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=255)),
                ("slug", models.SlugField()),
                ("description", models.TextField(blank=True, null=True)),
                ("img", models.ImageField(upload_to="images/")),
                ("thumbnail", models.ImageField(blank=True, null=True, upload_to="images/")),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dataset",
                        to="datasets.dataset_model",
                    ),
                ),
            ],
            options={
                "ordering": ("-date_added",),
            },
        ),
    ]