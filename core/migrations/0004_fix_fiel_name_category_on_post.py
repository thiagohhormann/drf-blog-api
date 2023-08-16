# Generated by Django 4.2.4 on 2023-08-16 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_make_field_birthday_mandatory_on_profile"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.RenameField(
            model_name="post",
            old_name="categories",
            new_name="category",
        ),
        migrations.AlterField(
            model_name="post",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]