# Generated by Django 4.1.4 on 2023-02-07 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_bookrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookcopy',
            options={'ordering': ('book',)},
        ),
        migrations.AlterModelOptions(
            name='bookrequest',
            options={'ordering': ('book',)},
        ),
    ]
