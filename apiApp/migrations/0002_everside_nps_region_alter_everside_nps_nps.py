# Generated by Django 4.0.3 on 2022-06-10 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='everside_nps',
            name='REGION',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='everside_nps',
            name='NPS',
            field=models.IntegerField(),
        ),
    ]
