# Generated by Django 4.1.7 on 2023-04-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_alter_gradelevel_gradelevel_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subjects",
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
                ("name", models.CharField(max_length=250)),
                ("is_deleted", models.BooleanField()),
            ],
        ),
    ]