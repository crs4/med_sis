#Django 4.2.24 on 2025-10-22 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("backoffice", "0002_sqlview"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.TextField(
                        db_comment="Photo identifier ",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "caption",
                    models.TextField(blank=True, db_comment="Description", null=True),
                ),
                (
                    "type",
                    models.TextField(
                        blank=True,
                        choices=[
                            ("pit", "photo of the pit "),
                            ("site", "photo of the site"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "point",
                    models.ForeignKey(
                        db_comment="Foreign Key field: point",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photo_point_set",
                        to="backoffice.pointgeneral",
                    ),
                ),
            ],
            options={
                "db_table": "photos",
                "db_table_comment": "projects descriptor",
                "permissions": (("view", "can view data"), ("write", "can write data")),
                "managed": True,
            },
        ),
    ]
