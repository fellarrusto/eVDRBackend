# Generated by Django 5.0.1 on 2024-01-27 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eVDR_api', '0004_userstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstats',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eVDR_api.chat'),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='latest_puzzle_solved',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
