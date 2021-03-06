# Generated by Django 4.0.2 on 2022-02-28 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('framework', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action',
            field=models.CharField(choices=[('DE', 'Deposit'), ('VA', 'Validated'), ('NA', 'Not Assessed'), ('WI', 'Withdrawal')], default='NA', max_length=2),
        ),
        migrations.AlterField(
            model_name='action',
            name='state',
            field=models.CharField(choices=[('DO', 'Done'), ('ER', 'Error'), ('IT', 'In Transit'), ('WA', 'Waiting')], default='WA', max_length=2),
        ),
        migrations.AlterField(
            model_name='locker',
            name='state',
            field=models.CharField(choices=[('ON', 'In Service'), ('ERR', 'Error'), ('OFF', 'Offline')], default='ON', max_length=3),
        ),
        migrations.AlterField(
            model_name='mission',
            name='state',
            field=models.CharField(choices=[('AR', 'Archived'), ('IP', 'In Process'), ('CF', 'Conflict'), ('CO', 'Completed'), ('IQ', 'In Queue'), ('FA', 'Failed'), ('NA', 'Not Attributed'), ('PA', 'Paused')], default='NA', max_length=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='comment',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='state',
            field=models.CharField(choices=[('ON', 'In Service'), ('ERR', 'Error'), ('OFF', 'Offline')], default='ON', max_length=3),
        ),
    ]
